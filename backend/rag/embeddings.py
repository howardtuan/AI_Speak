"""Embedding service using sentence-transformers (local)."""
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Singleton wrapper around sentence-transformers model."""
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading embedding model: all-MiniLM-L6-v2")
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("Embedding model loaded")
        return cls._model

    @classmethod
    def embed(cls, text: str) -> list[float]:
        """Generate embedding vector for a text string."""
        model = cls.get_model()
        return model.encode(text).tolist()

    @classmethod
    def embed_batch(cls, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts."""
        model = cls.get_model()
        return model.encode(texts).tolist()
