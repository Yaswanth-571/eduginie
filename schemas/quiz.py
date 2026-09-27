"""Pydantic schemas for the Quiz endpoint."""
from typing import List
from pydantic import BaseModel, field_validator, model_validator


class QuizRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("text must not be empty.")
        return v.strip()


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

    @field_validator("options")
    @classmethod
    def exactly_four_options(cls, v: List[str]) -> List[str]:
        if len(v) != 4:
            raise ValueError(f"Each question must have exactly 4 options, got {len(v)}.")
        return v

    @model_validator(mode="after")
    def correct_answer_in_options(self) -> "QuizQuestion":
        if self.correct_answer not in self.options:
            raise ValueError(
                f"correct_answer '{self.correct_answer}' is not in options {self.options}."
            )
        return self


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]

    @field_validator("questions")
    @classmethod
    def exactly_three_questions(cls, v: List[QuizQuestion]) -> List[QuizQuestion]:
        if len(v) != 3:
            raise ValueError(f"Quiz must have exactly 3 questions, got {len(v)}.")
        return v
