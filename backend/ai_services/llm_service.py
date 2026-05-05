"""LLM service using Ollama (local inference)."""
import logging
import ollama
from django.conf import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPTS = {
    "chat": (
        "You are a friendly and patient English conversation partner. "
        "Your goal is to help the user practice spoken English naturally. "
        "Keep responses conversational and at an appropriate level. "
        "If the user makes grammar or vocabulary mistakes, gently continue "
        "the conversation using the correct form without explicitly correcting them. "
        "Ask follow-up questions to keep the conversation flowing. "
        "Respond in English only. Keep responses concise (2-4 sentences) "
        "to maintain a natural conversation pace."
    ),
    "interview": (
        "You are a professional job interviewer conducting a mock interview. "
        "Use the provided resume/document context to ask relevant, realistic "
        "interview questions. Start with introductory questions, then move to "
        "behavioral and technical questions based on the candidate's background. "
        "Provide brief, professional responses. Ask one question at a time. "
        "Respond in English only. Keep responses concise."
    ),
}


class LLMService:
    """Interface to Ollama local LLM."""

    @staticmethod
    def chat_stream(messages: list, mode: str = "chat", context: str = ""):
        """Stream chat completion tokens from Ollama."""
        system_content = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["chat"])

        if context:
            system_content += (
                f"\n\nRelevant document context about the candidate:\n"
                f"---\n{context}\n---"
            )

        full_messages = [
            {"role": "system", "content": system_content}
        ] + messages

        try:
            stream = ollama.chat(
                model=settings.OLLAMA_MODEL,
                messages=full_messages,
                stream=True,
            )
            for chunk in stream:
                token = chunk.get("message", {}).get("content", "")
                if token:
                    yield token
        except Exception as e:
            logger.error("Ollama error: %s", e)
            yield "I'm sorry, I'm having trouble responding right now."

    @staticmethod
    def chat_sync(messages: list, mode: str = "chat", context: str = "") -> str:
        """Non-streaming chat completion."""
        tokens = list(LLMService.chat_stream(messages, mode, context))
        return "".join(tokens)
