"""Vector similarity search using pgvector."""
import logging
from pgvector.django import CosineDistance

from .models import DocumentChunk
from .embeddings import EmbeddingService

logger = logging.getLogger(__name__)


class Retriever:
    @staticmethod
    def search(query: str, user_id: int, top_k: int = 5) -> list[str]:
        """Find the most relevant document chunks for a query."""
        query_embedding = EmbeddingService.embed(query)

        chunks = (
            DocumentChunk.objects
            .filter(document__user_id=user_id)
            .order_by(CosineDistance("embedding", query_embedding))
            [:top_k]
        )

        results = [chunk.content for chunk in chunks]
        logger.debug("Retrieved %d chunks for query: %s...", len(results), query[:50])
        return results
