from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.domain.entities.question import QuestionType


class CreateQuestionRequest(BaseModel):
    """
    Create a new question.
    
    ## Required Fields by Question Type:
    
    ### TEXT
    - `question_text`: The question text
    - `question_type`: "text"
    - `correct_text`: The correct answer (string)
    
    ### YES_NO
    - `question_text`: The question text
    - `question_type`: "yes_no"
    - `correct_boolean`: The correct answer (true/false)
    - `following_question_id`: (Optional) ID of parent YES_NO question for conditional logic
    
    ### SINGLE_CHOICE
    - `question_text`: The question text
    - `question_type`: "single_choice"
    - `options`: List of answer options (min 2)
    - `correct_option_index`: Index of the correct option (0-based)
    
    ### MULTI_CHOICE
    - `question_text`: The question text
    - `question_type`: "multi_choice"
    - `options`: List of answer options (min 2)
    - `correct_option_indices`: List of indices for correct options (0-based)
    """
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "description": "TEXT Question Example",
                    "question_text": "What is to?",
                    "question_type": "text",
                    "correct_text": "Paris"
                },
                {
                    "description": "YES_NO Question Example",
                    "question_text": "Is Python a programming language?",
                    "question_type": "yes_no",
                    "correct_boolean": True
                },
                {
                    "description": "SINGLE_CHOICE Question Example",
                    "question_text": "What is 2 + 2?",
                    "question_type": "single_choice",
                    "options": ["3", "4", "5", "6"],
                    "correct_option_index": 1
                },
                {
                    "description": "MULTI_CHOICE Question Example",
                    "question_text": "Select all prime numbers:",
                    "question_type": "multi_choice",
                    "options": ["2", "4", "7", "9", "11"],
                    "correct_option_indices": [0, 2, 4]
                }
            ]
        }
    )

    question_text: str = Field(
        ...,
        description="The question text (1-500 characters)",
        min_length=1,
        max_length=500,
        examples=["What is the capital of France?"]
    )
    
    question_type: QuestionType = Field(
        ...,
        description="Type of question: 'text', 'yes_no', 'single_choice', or 'multi_choice'",
        examples=["text"]
    )
    
    options: Optional[List[str]] = Field(
        None,
        description="Required for SINGLE_CHOICE and MULTI_CHOICE. List of answer options (min 2).",
        examples=[["Option A", "Option B", "Option C"]]
    )
    
    correct_text: Optional[str] = Field(
        None,
        description="Required for TEXT questions. The correct answer as a string.",
        examples=["Paris"]
    )
    
    correct_boolean: Optional[bool] = Field(
        None,
        description="Required for YES_NO questions. The correct answer (true or false).",
        examples=[True]
    )
    
    correct_option_index: Optional[int] = Field(
        None,
        description="Required for SINGLE_CHOICE. Zero-based index of the correct option.",
        examples=[1]
    )
    
    correct_option_indices: Optional[List[int]] = Field(
        None,
        description="Required for MULTI_CHOICE. List of zero-based indices for all correct options.",
        examples=[[0, 2]]
    )
    
    following_question_id: Optional[int] = Field(
        None,
        description="Optional for YES_NO questions only. ID of parent question for conditional logic.",
        examples=[1]
    )

    @field_validator("question_type")
    @classmethod
    def validate_question_type(cls, question_type: QuestionType) -> QuestionType:
        if question_type not in QuestionType:
            raise ValueError("Invalid question type")
        return question_type


class QuestionResponse(BaseModel):
    """
    Question response schema.
    
    Contains the complete question data including all type-specific fields.
    Only the fields relevant to the question_type will have values.
    """

    id: int = Field(..., description="Unique question ID")
    question_text: str = Field(..., description="The question text")
    question_type: QuestionType = Field(..., description="Type of question")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    options: Optional[List[str]] = Field(
        None,
        description="Answer options (populated for SINGLE_CHOICE and MULTI_CHOICE)"
    )
    correct_text: Optional[str] = Field(
        None,
        description="Correct answer text (populated for TEXT questions)"
    )
    correct_boolean: Optional[bool] = Field(
        None,
        description="Correct boolean answer (populated for YES_NO questions)"
    )
    correct_option_index: Optional[int] = Field(
        None,
        description="Index of correct option (populated for SINGLE_CHOICE)"
    )
    correct_option_indices: Optional[List[int]] = Field(
        None,
        description="Indices of correct options (populated for MULTI_CHOICE)"
    )
    following_question_id: Optional[int] = Field(
        None,
        description="Parent question ID for conditional logic (YES_NO only)"
    )


class UpdateQuestionRequest(BaseModel):
    """
    Update an existing question.
    
    ## Required Fields by Question Type:
    
    ### TEXT
    - `question_text`: The question text
    - `question_type`: "text"
    - `correct_text`: The correct answer (string)
    
    ### YES_NO
    - `question_text`: The question text
    - `question_type`: "yes_no"
    - `correct_boolean`: The correct answer (true/false)
    - `following_question_id`: (Optional) ID of parent YES_NO question
    
    ### SINGLE_CHOICE
    - `question_text`: The question text
    - `question_type`: "single_choice"
    - `options`: List of answer options (min 2)
    - `correct_option_index`: Index of the correct option (0-based)
    
    ### MULTI_CHOICE
    - `question_text`: The question text
    - `question_type`: "multi_choice"
    - `options`: List of answer options (min 2)
    - `correct_option_indices`: List of indices for correct options (0-based)
    """
    
    question_text: Optional[str] = Field(
        None,
        description="The question text (1-500 characters)",
        min_length=1,
        max_length=500
    )
    
    question_type: Optional[QuestionType] = Field(
        None,
        description="Type of question: 'text', 'yes_no', 'single_choice', or 'multi_choice'"
    )
    
    options: Optional[List[str]] = Field(
        None,
        description="Required for SINGLE_CHOICE and MULTI_CHOICE. List of answer options (min 2)."
    )
    
    correct_text: Optional[str] = Field(
        None,
        description="Required for TEXT questions. The correct answer as a string."
    )
    
    correct_boolean: Optional[bool] = Field(
        None,
        description="Required for YES_NO questions. The correct answer (true or false)."
    )
    
    correct_option_index: Optional[int] = Field(
        None,
        description="Required for SINGLE_CHOICE. Zero-based index of the correct option."
    )
    
    correct_option_indices: Optional[List[int]] = Field(
        None,
        description="Required for MULTI_CHOICE. List of zero-based indices for all correct options."
    )
    
    following_question_id: Optional[int] = Field(
        None,
        description="Optional for YES_NO questions only. ID of parent question for conditional logic."
    )

    @field_validator("question_type")
    @classmethod
    def validate_question_type_update(cls, question_type: QuestionType) -> QuestionType:
        if question_type not in QuestionType:
            raise ValueError("Invalid question type")
        return question_type
