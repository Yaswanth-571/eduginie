"""
Quiz Module – powered by Google Gemini API.

Receives educational text and generates a 3-question multiple-choice quiz.
Each question has exactly 4 options and 1 correct answer.
"""
from __future__ import annotations

from pydantic import ValidationError

from schemas.quiz import QuizRequest, QuizResponse
from services.gemini_service import generate_text
from utils.json_utils import safe_parse_json


_QUIZ_PROMPT_TEMPLATE = """\
You are EduGenie, an expert quiz creator for students.

Read the educational text below and generate a multiple-choice quiz.

STRICT REQUIREMENTS:
1. Generate EXACTLY 3 questions — no more, no fewer.
2. Each question must have EXACTLY 4 answer options labeled in a list.
3. Provide the correct answer as the EXACT text of one of the 4 options.
4. Return ONLY valid JSON — no markdown, no prose, no code fences.
5. The JSON must follow this exact structure:

{{
  "questions": [
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correct_answer": "..."
    }},
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correct_answer": "..."
    }},
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "correct_answer": "..."
    }}
  ]
}}

Educational text:
{text}
"""


def generate_quiz(request: QuizRequest) -> QuizResponse:
    """
    Generate a 3-question MCQ quiz from the provided educational text.

    Raises:
        ValueError: if Gemini returns malformed or invalid quiz JSON.
    """
    prompt = _QUIZ_PROMPT_TEMPLATE.format(text=request.text)
    raw = generate_text(prompt)

    try:
        data = safe_parse_json(raw)
    except ValueError as exc:
        raise ValueError(f"Quiz generation failed — could not parse JSON: {exc}") from exc

    try:
        quiz = QuizResponse.model_validate(data)
    except ValidationError as exc:
        raise ValueError(f"Quiz validation failed: {exc}") from exc

    return quiz
