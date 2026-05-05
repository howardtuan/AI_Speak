import json
import tempfile
import asyncio
import time

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings

from ai_services.stt_service import STTService
from ai_services.llm_service import LLMService
from ai_services.tts_service import TTSService
from rag.retriever import Retriever
from chat.models import Conversation, Message


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time voice conversation.

    Flow: receive audio → STT → (RAG) → LLM → TTS → send audio back
    """

    async def connect(self):
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.messages_history = []
        self.mode = "chat"
        self.start_time = time.time()
        self.time_limit = settings.CONVERSATION_TIME_LIMIT_MINUTES * 60

        # Verify conversation belongs to user
        conversation = await self._get_conversation()
        if conversation is None:
            await self.close()
            return

        self.mode = conversation.mode
        self.user_id = conversation.user_id

        # Load existing messages into history
        existing = await self._load_messages()
        self.messages_history = existing

        await self.accept()
        await self.send(text_data=json.dumps({
            "type": "connected",
            "mode": self.mode,
            "time_limit": self.time_limit,
        }))

    async def receive(self, text_data=None, bytes_data=None):
        # Check time limit
        elapsed = time.time() - self.start_time
        if elapsed > self.time_limit:
            await self.send(text_data=json.dumps({
                "type": "time_up",
                "message": "對話時間已達 20 分鐘上限",
            }))
            return

        # Text message (config updates)
        if text_data:
            data = json.loads(text_data)
            if data.get("type") == "config":
                self.mode = data.get("mode", self.mode)
            return

        # Binary message (audio data)
        if bytes_data:
            await self._process_audio(bytes_data)

    async def _process_audio(self, audio_bytes):
        """Process audio: STT → RAG → LLM → TTS."""
        # 1. STT: Speech → Text
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
            f.write(audio_bytes)
            audio_path = f.name

        user_text = await asyncio.to_thread(STTService.transcribe, audio_path)

        await self.send(text_data=json.dumps({
            "type": "user_text",
            "text": user_text,
        }))

        # Save user message
        await self._save_message("user", user_text)

        # 2. RAG retrieval (interview mode only)
        context = ""
        if self.mode == "interview":
            chunks = await asyncio.to_thread(
                Retriever.search, user_text, self.user_id
            )
            context = "\n".join(chunks)

        # 3. LLM: Generate response (streaming)
        self.messages_history.append({"role": "user", "content": user_text})
        full_response = ""

        for token in await asyncio.to_thread(
            lambda: list(LLMService.chat_stream(
                self.messages_history, self.mode, context
            ))
        ):
            full_response += token
            await self.send(text_data=json.dumps({
                "type": "ai_token",
                "token": token,
            }))

        self.messages_history.append({"role": "assistant", "content": full_response})

        await self.send(text_data=json.dumps({
            "type": "ai_complete",
            "text": full_response,
        }))

        # Save assistant message
        await self._save_message("assistant", full_response)

        # 4. TTS: Text → Speech
        audio_data = await asyncio.to_thread(TTSService.synthesize, full_response)
        await self.send(bytes_data=audio_data)

    @database_sync_to_async
    def _get_conversation(self):
        try:
            return Conversation.objects.get(
                id=self.conversation_id, is_active=True
            )
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def _load_messages(self):
        msgs = Message.objects.filter(
            conversation_id=self.conversation_id,
            role__in=["user", "assistant"],
        ).values("role", "content")
        return [{"role": m["role"], "content": m["content"]} for m in msgs]

    @database_sync_to_async
    def _save_message(self, role, content):
        Message.objects.create(
            conversation_id=self.conversation_id,
            role=role,
            content=content,
        )
