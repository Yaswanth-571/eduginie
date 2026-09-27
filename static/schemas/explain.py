"""Pydantic schemas for the Explain endpoint."""
from pydantic import BaseModel, field_validator


class ExplainRequest(BaseModel):
    topic: str

    @field_validator("topic")
    @classmethod
    def topic_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("topic must not be empty.")
        return v.strip()


class ExplainResponse(BaseModel):
    topic: str
    explanation: str
