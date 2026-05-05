from django.contrib import admin
from .models import Conversation, Message, SessionReport, MessageCorrection, ReviewItem


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "mode", "title", "is_active", "started_at")
    list_filter = ("mode", "is_active")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "role", "created_at")
    list_filter = ("role",)


@admin.register(SessionReport)
class SessionReportAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "overall_score", "created_at")


@admin.register(MessageCorrection)
class MessageCorrectionAdmin(admin.ModelAdmin):
    list_display = ("id", "error_type", "original_text")


@admin.register(ReviewItem)
class ReviewItemAdmin(admin.ModelAdmin):
    list_display = ("id", "item_type", "content")
