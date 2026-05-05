from django.utils import timezone
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Conversation, SessionReport
from .serializers import (
    ConversationListSerializer,
    ConversationCreateSerializer,
    ConversationDetailSerializer,
    SessionReportSerializer,
)
from ai_services.review_service import ReviewService


class ConversationViewSet(viewsets.ModelViewSet):
    """CRUD for conversations + end session + get report."""
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return ConversationCreateSerializer
        if self.action == "retrieve":
            return ConversationDetailSerializer
        return ConversationListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def end(self, request, pk=None):
        """End a conversation and trigger AI analysis."""
        conversation = self.get_object()
        if not conversation.is_active:
            return Response(
                {"detail": "對話已結束"}, status=status.HTTP_400_BAD_REQUEST
            )

        conversation.is_active = False
        conversation.ended_at = timezone.now()
        conversation.save()

        # Generate session report via LLM
        messages = list(
            conversation.messages.filter(role__in=["user", "assistant"]).values(
                "role", "content"
            )
        )
        if messages:
            report_data = ReviewService.generate_report(messages)
            ReviewService.save_report(conversation, report_data)

        return Response({"detail": "對話已結束，報告生成中"})

    @action(detail=True, methods=["get"])
    def report(self, request, pk=None):
        """Get session report for a conversation."""
        conversation = self.get_object()
        try:
            report = conversation.report
        except SessionReport.DoesNotExist:
            return Response(
                {"detail": "報告尚未生成"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(SessionReportSerializer(report).data)
