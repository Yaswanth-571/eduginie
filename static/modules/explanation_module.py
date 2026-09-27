"""
Explanation Module – powered by Google Gemini API.

Receives a topic and returns a beginner-friendly explanation with examples.
"""
from __future__ import annotations

from schemas.explain import ExplainRequest, ExplainResponse
from services.gemini_service import generate_text


def explain_topic(request: ExplainRequest) -> ExplainResponse:
    """
    Build a prompt that instructs Gemini to produce a clear explanation
    suitable for a beginner learner.
    """
    prompt = (
        "You are EduGenie, a patient and friendly educational tutor. "
        "Explain the following concept to someone with no prior knowledge of it.\n\n"
        "Your explanation should:\n"
        "- Use simple, everyday language — avoid heavy technical jargon.\n"
        "- Assume the reader is a complete beginner.\n"
        "- Break the concept into smaller, easy-to-digest parts.\n"
        "- Provide at least one concrete, real-world example.\n"
        "- End with a short summary (2–3 sentences) of the key takeaway.\n\n"
        f"Concept to explain: {request.topic}\n\n"
        "Explanation:"
    )

    explanation = generate_text(prompt)
    return ExplainResponse(topic=request.topic, explanation=explanation)
