"""
Summary Module – powered by Google Gemini API.

Receives a long educational passage and returns a concise, accurate summary.
"""
from __future__ import annotations

from schemas.summary import SummaryRequest, SummaryResponse
from services.gemini_service import generate_text


def summarize_text(request: SummaryRequest) -> SummaryResponse:
    """
    Build a summarisation prompt and call Gemini.
    """
    prompt = (
        "You are EduGenie, an expert at summarising educational content. "
        "Summarise the following passage for a student reader.\n\n"
        "Your summary should:\n"
        "- Be concise — capture only the most important points.\n"
        "- Preserve the key ideas and facts from the original text.\n"
        "- Use clear, easy-to-understand language.\n"
        "- Avoid unnecessary repetition.\n"
        "- Be no longer than one-third of the original length.\n\n"
        "Passage to summarise:\n"
        f"{request.text}\n\n"
        "Summary:"
    )

    summary = generate_text(prompt)
    return SummaryResponse(summary=summary)
