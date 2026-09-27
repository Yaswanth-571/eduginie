"""
Learning Path Module – powered by Google Gemini API.

Receives a topic and learning level and returns a structured learning
path with beginner → intermediate → advanced progression.
"""
from __future__ import annotations

from schemas.learning_path import LearningPathRequest, LearningPathResponse
from services.gemini_service import generate_text


def get_recommendations(request: LearningPathRequest) -> LearningPathResponse:
    """
    Build a learning-path prompt and call Gemini.
    """
    prompt = (
        "You are EduGenie, a world-class learning advisor. "
        f"A student at the '{request.level}' level wants to learn '{request.topic}'.\n\n"
        "Create a detailed, structured learning path that includes:\n"
        "1. **Beginner Topics** – foundational concepts to start with.\n"
        "2. **Intermediate Topics** – skills to build after mastering the basics.\n"
        "3. **Advanced Topics** – expert-level concepts for deeper mastery.\n"
        "4. **Suggested Study Order** – a step-by-step sequence to follow.\n"
        "5. **Practical Learning Suggestions** – hands-on projects, exercises, or challenges.\n"
        "6. **Useful Resources** – books, websites, courses, or tools where applicable.\n\n"
        "Format the response clearly with headings and bullet points. "
        "Tailor the depth and starting point based on the student's current level "
        f"('{request.level}').\n\n"
        "Learning Path:"
    )

    recommendations = generate_text(prompt)
    return LearningPathResponse(
        topic=request.topic,
        level=request.level,
        recommendations=recommendations,
    )
