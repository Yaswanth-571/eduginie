"""Pydantic schemas for the Summarize endpoint."""
from pydantic import BaseModel, field_validator


class SummaryRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be empty.")
        return v.strip()


class SummaryResponse(BaseModel):
    summary: str
