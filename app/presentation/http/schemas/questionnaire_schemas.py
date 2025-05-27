from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class QuestionnaireCreate(BaseModel):
    """Schema for creating a questionnaire"""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    question_ids: List[int] = Field(default_factory=list)

    @field_validator("question_ids")
    @classmethod
    def validate_unique_questions(cls, question_ids: List[int]) -> List[int]:
        """Ensure no duplicate question IDs"""
        unique_question_ids = list(set(question_ids))
        total_question_count = len(question_ids)

        if total_question_count != len(unique_question_ids):
            raise ValueError("Duplicate question IDs are not allowed")

        return unique_question_ids


class QuestionnaireResponse(BaseModel):
    """Schema for questionnaire response"""

    id: int
    title: str
    description: Optional[str]
    question_ids: List[int]
    created_at: datetime
    updated_at: datetime
