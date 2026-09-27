"""Pydantic schemas for the Q&A endpoint."""
from pydantic import BaseModel, field_validator


class QARequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def question_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("question must not be empty.")
        return v.strip()


class QAResponse(BaseModel):
    question: str
    answer: str
