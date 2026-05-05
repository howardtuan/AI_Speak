"""Text-to-Speech service using Kokoro TTS (local CPU inference)."""
import io
import logging
import soundfile as sf

logger = logging.getLogger(__name__)


class TTSService:
    """Singleton wrapper around Kokoro TTS model."""
    _pipeline = None

    @classmethod
    def get_pipeline(cls):
        if cls._pipeline is None:
            from kokoro import KPipeline
            logger.info("Loading Kokoro TTS pipeline...")
            cls._pipeline = KPipeline(lang_code="a")  # American English
            logger.info("Kokoro TTS loaded successfully")
        return cls._pipeline

    @classmethod
    def synthesize(cls, text: str, voice: str = "af_heart", speed: float = 1.0) -> bytes:
        """Convert text to WAV audio bytes."""
        pipeline = cls.get_pipeline()
        
        # Generate audio using Kokoro pipeline
        audio_segments = []
        for _, _, audio in pipeline(text, voice=voice, speed=speed):
            audio_segments.append(audio)
        
        if not audio_segments:
            return b""
        
        # Concatenate all segments
        import numpy as np
        full_audio = np.concatenate(audio_segments)
        
        # Convert to WAV bytes
        buffer = io.BytesIO()
        sf.write(buffer, full_audio, samplerate=24000, format="WAV")
        buffer.seek(0)
        return buffer.read()
