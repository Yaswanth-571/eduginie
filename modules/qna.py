"""
Q&A Module – powered by Google Gemini API.

Receives a student question and returns a clear, educational answer.
"""
from __future__ import annotations

from schemas.qa import QARequest, QAResponse
from services.gemini_service import generate_text


def answer_question(request: QARequest) -> QAResponse:
    """
    Build a prompt tailored for educational Q&A and call Gemini.
    """
    prompt = (
        "You are EduGenie, a helpful educational assistant. "
        "Answer the following student question clearly and concisely. "
        "Your answer should:\n"
        "- Directly address the question.\n"
        "- Be understandable to students of all levels.\n"
        "- Avoid unnecessary jargon or complexity.\n"
        "- Use simple, relatable examples where helpful.\n\n"
        f"Question: {request.question}\n\n"
        "Answer:"
    )

    answer = generate_text(prompt)
    return QAResponse(question=request.question, answer=answer)
