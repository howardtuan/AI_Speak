from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """A conversation session between user and AI."""
    MODE_CHOICES = [
        ("chat", "純聊天"),
        ("interview", "面試練習"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations"
    )
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default="chat")
    title = models.CharField(max_length=200, blank=True)
    system_prompt = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "conversations"
        ordering = ["-started_at"]

    def __str__(self):
        return f"[{self.mode}] {self.title or self.id} - {self.user.username}"


class Message(models.Model):
    """A single message in a conversation."""
    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
        ("system", "System"),
    ]

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    audio_url = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messages"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"


class SessionReport(models.Model):
    """Post-conversation analysis and scoring."""
    conversation = models.OneToOneField(
        Conversation, on_delete=models.CASCADE, related_name="report"
    )
    fluency_score = models.IntegerField(default=0)
    grammar_score = models.IntegerField(default=0)
    vocabulary_score = models.IntegerField(default=0)
    overall_score = models.IntegerField(default=0)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "session_reports"

    def __str__(self):
        return f"Report for conversation {self.conversation_id} - {self.overall_score}/10"


class MessageCorrection(models.Model):
    """Error annotations for individual messages."""
    ERROR_TYPE_CHOICES = [
        ("grammar", "文法錯誤"),
        ("vocabulary", "詞彙問題"),
        ("pronunciation", "發音問題"),
        ("expression", "表達不自然"),
    ]

    report = models.ForeignKey(
        SessionReport, on_delete=models.CASCADE, related_name="corrections"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, related_name="corrections",
        null=True, blank=True
    )
    original_text = models.TextField()
    corrected_text = models.TextField()
    error_type = models.CharField(max_length=50, choices=ERROR_TYPE_CHOICES)
    explanation = models.TextField()

    class Meta:
        db_table = "message_corrections"


class ReviewItem(models.Model):
    """Vocabulary / grammar items for post-session review."""
    ITEM_TYPE_CHOICES = [
        ("word", "單字"),
        ("phrase", "片語"),
        ("grammar", "文法"),
    ]

    report = models.ForeignKey(
        SessionReport, on_delete=models.CASCADE, related_name="review_items"
    )
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    content = models.TextField()
    example_sentence = models.TextField()
    translation = models.TextField(blank=True)

    class Meta:
        db_table = "review_items"
