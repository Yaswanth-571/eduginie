"""Pydantic schemas for the Learning Path endpoint."""
from typing import Literal
from pydantic import BaseModel, field_validator


class LearningPathRequest(BaseModel):
    topic: str
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"

    @field_validator("topic")
    @classmethod
    def topic_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("topic must not be empty.")
        return v.strip()


class LearningPathResponse(BaseModel):
    topic: str
    level: str
    recommendations: str
