from rest_framework import serializers
from .models import Conversation, Message, SessionReport, MessageCorrection, ReviewItem


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "role", "content", "audio_url", "created_at")
        read_only_fields = fields


class ConversationListSerializer(serializers.ModelSerializer):
    message_count = serializers.IntegerField(source="messages.count", read_only=True)
    has_report = serializers.BooleanField(source="report", read_only=True, default=False)

    class Meta:
        model = Conversation
        fields = (
            "id", "mode", "title", "is_active",
            "started_at", "ended_at", "message_count", "has_report",
        )


class ConversationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ("mode", "title")


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = (
            "id", "mode", "title", "is_active",
            "started_at", "ended_at", "messages",
        )


class MessageCorrectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageCorrection
        fields = (
            "id", "original_text", "corrected_text",
            "error_type", "explanation",
        )


class ReviewItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewItem
        fields = ("id", "item_type", "content", "example_sentence", "translation")


class SessionReportSerializer(serializers.ModelSerializer):
    corrections = MessageCorrectionSerializer(many=True, read_only=True)
    review_items = ReviewItemSerializer(many=True, read_only=True)

    class Meta:
        model = SessionReport
        fields = (
            "id", "fluency_score", "grammar_score", "vocabulary_score",
            "overall_score", "summary", "corrections", "review_items",
            "created_at",
        )
