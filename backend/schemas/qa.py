from typing import Optional

from pydantic import BaseModel


class QuestionCreate(BaseModel):
    contract_id: int
    question: str


class QuestionOut(BaseModel):
    id: int
    contract_id: int
    user_id: int
    question_text: str
    answer_text: Optional[str] = None
    retrieved_snippets: Optional[str] = None

    class Config:
        from_attributes = True
        