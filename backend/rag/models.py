from django.db import models
from django.conf import settings
from pgvector.django import VectorField


class Document(models.Model):
    """Uploaded document (resume, cover letter, etc.)."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="documents"
    )
    filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10)  # pdf, docx
    file_path = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "documents"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.filename} ({self.user.username})"


class DocumentChunk(models.Model):
    """A chunk of text from a document, with its vector embedding."""
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="chunks"
    )
    content = models.TextField()
    embedding = VectorField(dimensions=384)  # all-MiniLM-L6-v2 outputs 384-dim
    chunk_index = models.IntegerField(default=0)

    class Meta:
        db_table = "document_chunks"
        ordering = ["chunk_index"]

    def __str__(self):
        return f"Chunk {self.chunk_index} of {self.document.filename}"
