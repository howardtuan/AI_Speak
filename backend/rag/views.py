import os
from rest_framework import views, generics, parsers, permissions, status
from rest_framework.response import Response
from django.conf import settings

from .models import Document, DocumentChunk
from .parser import parse_document, chunk_text
from .embeddings import EmbeddingService


class DocumentSerializer:
    """Inline serializer for document responses."""
    @staticmethod
    def to_dict(doc):
        return {
            "id": doc.id,
            "filename": doc.filename,
            "file_type": doc.file_type,
            "chunk_count": doc.chunks.count(),
            "uploaded_at": doc.uploaded_at.isoformat(),
        }


class DocumentUploadView(views.APIView):
    """Upload a document (PDF/DOCX) for RAG processing."""
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.MultiPartParser,)

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"detail": "請上傳檔案"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Determine file type
        ext = file.name.rsplit(".", 1)[-1].lower()
        if ext not in ("pdf", "docx"):
            return Response(
                {"detail": "僅支援 PDF 和 DOCX 格式"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save file
        upload_dir = os.path.join(settings.MEDIA_ROOT, "documents", str(request.user.id))
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.name)

        with open(file_path, "wb+") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        # Create document record
        doc = Document.objects.create(
            user=request.user,
            filename=file.name,
            file_type=ext,
            file_path=file_path,
        )

        # Parse, chunk, embed, and store
        try:
            text = parse_document(file_path, ext)
            chunks = chunk_text(text)
            embeddings = EmbeddingService.embed_batch(chunks)

            for i, (chunk_text_content, embedding) in enumerate(zip(chunks, embeddings)):
                DocumentChunk.objects.create(
                    document=doc,
                    content=chunk_text_content,
                    embedding=embedding,
                    chunk_index=i,
                )

            return Response(
                {
                    "detail": f"已成功處理 {file.name}，共 {len(chunks)} 個文字段落",
                    "document": DocumentSerializer.to_dict(doc),
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            doc.delete()
            return Response(
                {"detail": f"文件處理失敗: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DocumentListView(views.APIView):
    """List and delete user documents."""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        docs = Document.objects.filter(user=request.user)
        return Response([DocumentSerializer.to_dict(d) for d in docs])

    def delete(self, request, pk=None):
        try:
            doc = Document.objects.get(id=pk, user=request.user)
            # Remove file from disk
            if os.path.exists(doc.file_path):
                os.remove(doc.file_path)
            doc.delete()
            return Response({"detail": "文件已刪除"})
        except Document.DoesNotExist:
            return Response(
                {"detail": "文件不存在"}, status=status.HTTP_404_NOT_FOUND
            )
