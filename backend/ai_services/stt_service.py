"""Speech-to-Text service using faster-whisper (local GPU inference)."""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class STTService:
    """Singleton wrapper around faster-whisper model."""
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            from faster_whisper import WhisperModel
            logger.info("Loading Whisper model: %s", settings.WHISPER_MODEL_SIZE)
            cls._instance = WhisperModel(
                settings.WHISPER_MODEL_SIZE,
                device=settings.WHISPER_DEVICE,
                compute_type=settings.WHISPER_COMPUTE_TYPE,
            )
            logger.info("Whisper model loaded successfully")
        return cls._instance

    @classmethod
    def transcribe(cls, audio_path: str, language: str = "en") -> str:
        """Transcribe an audio file to text."""
        model = cls.get_instance()
        segments, info = model.transcribe(audio_path, language=language)
        text = " ".join(segment.text.strip() for segment in segments)
        logger.debug("Transcribed (%.1fs audio): %s", info.duration, text)
        return text
