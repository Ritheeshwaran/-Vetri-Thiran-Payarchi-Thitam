from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=500)


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=20, max_length=30000)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=10, max_length=30000)


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    answer: str

    @field_validator("answer")
    @classmethod
    def answer_must_be_an_option(cls, value: str, info):
        options = info.data.get("options", [])
        if options and value not in options:
            raise ValueError("The correct answer must exactly match one of the options.")
        return value


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)
