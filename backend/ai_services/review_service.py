"""Post-conversation review and scoring service."""
import json
import logging
import ollama
from django.conf import settings

from chat.models import SessionReport, MessageCorrection, ReviewItem

logger = logging.getLogger(__name__)

REVIEW_PROMPT = """You are an English language tutor analyzing a practice conversation.
The user is a non-native English speaker practicing their English speaking skills.

Analyze the user's messages in this conversation and provide feedback.

IMPORTANT: Respond ONLY with valid JSON matching this exact schema:
{{
  "fluency_score": <1-10>,
  "grammar_score": <1-10>,
  "vocabulary_score": <1-10>,
  "overall_score": <1-10>,
  "summary": "<2-3 sentences of encouraging feedback in Traditional Chinese>",
  "corrections": [
    {{
      "original_text": "<what the user said>",
      "corrected_text": "<corrected version>",
      "error_type": "<grammar|vocabulary|expression>",
      "explanation": "<brief explanation in Traditional Chinese>"
    }}
  ],
  "review_items": [
    {{
      "item_type": "<word|phrase|grammar>",
      "content": "<English word/phrase/grammar point>",
      "example_sentence": "<example sentence using it correctly>",
      "translation": "<Traditional Chinese translation>"
    }}
  ]
}}

Conversation:
{conversation_text}
"""


class ReviewService:
    @staticmethod
    def generate_report(messages: list[dict]) -> dict:
        """Analyze conversation and return structured feedback."""
        conversation_text = "\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in messages
        )

        try:
            response = ollama.chat(
                model=settings.OLLAMA_MODEL,
                messages=[{
                    "role": "user",
                    "content": REVIEW_PROMPT.format(
                        conversation_text=conversation_text
                    ),
                }],
                format="json",
            )
            result = json.loads(response["message"]["content"])
            logger.info("Review report generated: score=%s", result.get("overall_score"))
            return result
        except Exception as e:
            logger.error("Failed to generate review: %s", e)
            return {
                "fluency_score": 0,
                "grammar_score": 0,
                "vocabulary_score": 0,
                "overall_score": 0,
                "summary": "報告生成失敗，請稍後再試。",
                "corrections": [],
                "review_items": [],
            }

    @staticmethod
    def save_report(conversation, report_data: dict):
        """Save the generated report to database."""
        report = SessionReport.objects.create(
            conversation=conversation,
            fluency_score=report_data.get("fluency_score", 0),
            grammar_score=report_data.get("grammar_score", 0),
            vocabulary_score=report_data.get("vocabulary_score", 0),
            overall_score=report_data.get("overall_score", 0),
            summary=report_data.get("summary", ""),
        )

        for correction in report_data.get("corrections", []):
            MessageCorrection.objects.create(
                report=report,
                original_text=correction.get("original_text", ""),
                corrected_text=correction.get("corrected_text", ""),
                error_type=correction.get("error_type", "grammar"),
                explanation=correction.get("explanation", ""),
            )

        for item in report_data.get("review_items", []):
            ReviewItem.objects.create(
                report=report,
                item_type=item.get("item_type", "word"),
                content=item.get("content", ""),
                example_sentence=item.get("example_sentence", ""),
                translation=item.get("translation", ""),
            )

        return report
