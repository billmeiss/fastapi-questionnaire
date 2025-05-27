from typing import List, Optional
from app.domain.entities.question import Question, QuestionType
from app.infrastructure.repositories.question_repository import QuestionRepository


class QuestionService:
    """Domain service for question operations"""

    def __init__(self, repository: QuestionRepository):
        self.repository = repository

    def create(
        self,
        question_text: str,
        question_type: QuestionType,
        options: Optional[List[str]] = None,
        correct_text: Optional[str] = None,
        correct_boolean: Optional[bool] = None,
        correct_option_index: Optional[int] = None,
        correct_option_indices: Optional[List[int]] = None,
        following_question_id: Optional[int] = None,
    ) -> Question:
        """Create a new question"""
        question = Question(
            id=None,
            question_text=question_text,
            question_type=question_type,
            options=options,
            correct_text=correct_text,
            correct_boolean=correct_boolean,
            correct_option_index=correct_option_index,
            correct_option_indices=correct_option_indices,
            following_question_id=following_question_id,
        )

        return self.repository.create(question)

    def get_by_id(self, question_id: int) -> Question:
        """Get a question by its ID"""
        return self.repository.get_by_id(question_id)

    def get_all(self) -> List[Question]:
        """Get all questions"""
        return self.repository.get_all()

    def update(
        self,
        question_id: int,
        question_text: str,
        question_type: QuestionType,
        options: Optional[List[str]] = None,
        correct_text: Optional[str] = None,
        correct_boolean: Optional[bool] = None,
        correct_option_index: Optional[int] = None,
        correct_option_indices: Optional[List[int]] = None,
        following_question_id: Optional[int] = None,
    ) -> Question:
        """Update a question with domain validation and type change handling
        
        When updating:
        - If question type changes, invalid fields are automatically cleared
        - If question type stays the same, only provided fields are updated
        - All updates are validated before saving
        """
        existing = self.get_by_id(question_id)
        if not existing:
            raise ValueError(f"Question with id {question_id} not found")

        merged_data = self._merge_update_data(
            existing=existing,
            question_id=question_id,
            question_text=question_text,
            question_type=question_type,
            options=options,
            correct_text=correct_text,
            correct_boolean=correct_boolean,
            correct_option_index=correct_option_index,
            correct_option_indices=correct_option_indices,
            following_question_id=following_question_id,
        )

        # Validate the merged data by creating a Question object
        # This ensures all type-specific validation rules are enforced
        validated_question = Question(**merged_data)
        
        return self.repository.update(
            question_id=question_id,
            question_text=merged_data["question_text"],
            question_type=merged_data["question_type"],
            options=merged_data["options"],
            correct_text=merged_data["correct_text"],
            correct_boolean=merged_data["correct_boolean"],
            correct_option_index=merged_data["correct_option_index"],
            correct_option_indices=merged_data["correct_option_indices"],
            following_question_id=merged_data["following_question_id"],
        )

    def _merge_update_data(
        self,
        existing: Question,
        question_id: int,
        question_text: str,
        question_type: QuestionType,
        options: Optional[List[str]],
        correct_text: Optional[str],
        correct_boolean: Optional[bool],
        correct_option_index: Optional[int],
        correct_option_indices: Optional[List[int]],
        following_question_id: Optional[int],
    ) -> dict:
        """
        Merge update data with existing question, handling type changes.
        
        When the question type changes, only fields relevant to the new type are kept.
        Fields from the old type are automatically cleared (set to None).
        """
        type_is_changing = question_type is not None and question_type != existing.question_type

        if type_is_changing:
            return self._build_data_for_new_type(
                question_id=question_id,
                question_text=question_text if question_text is not None else existing.question_text,
                question_type=question_type,
                options=options,
                correct_text=correct_text,
                correct_boolean=correct_boolean,
                correct_option_index=correct_option_index,
                correct_option_indices=correct_option_indices,
                following_question_id=following_question_id,
            )
        else:
            return {
                "id": question_id,
                "question_text": question_text if question_text is not None else existing.question_text,
                "question_type": question_type if question_type is not None else existing.question_type,
                "options": options if options is not None else existing.options,
                "correct_text": correct_text if correct_text is not None else existing.correct_text,
                "correct_boolean": correct_boolean if correct_boolean is not None else existing.correct_boolean,
                "correct_option_index": correct_option_index if correct_option_index is not None else existing.correct_option_index,
                "correct_option_indices": correct_option_indices if correct_option_indices is not None else existing.correct_option_indices,
                "following_question_id": following_question_id if following_question_id is not None else existing.following_question_id,
            }

    def _build_data_for_new_type(
        self,
        question_id: int,
        question_text: str,
        question_type: QuestionType,
        options: Optional[List[str]],
        correct_text: Optional[str],
        correct_boolean: Optional[bool],
        correct_option_index: Optional[int],
        correct_option_indices: Optional[List[int]],
        following_question_id: Optional[int],
    ) -> dict:
        """
        Build question data with only fields relevant to the new type.
        
        When changing question types, invalid fields are set to None to ensure
        data consistency. Only fields allowed for the new type are preserved.
        """
        data = {
            "id": question_id,
            "question_text": question_text,
            "question_type": question_type,
        }
        
        if question_type == QuestionType.TEXT:
            data["options"] = None
            data["correct_text"] = correct_text
            data["correct_boolean"] = None
            data["correct_option_index"] = None
            data["correct_option_indices"] = None
            data["following_question_id"] = None
            
        elif question_type == QuestionType.YES_NO:
            data["options"] = None
            data["correct_text"] = None
            data["correct_boolean"] = correct_boolean
            data["correct_option_index"] = None
            data["correct_option_indices"] = None
            data["following_question_id"] = following_question_id
            
        elif question_type == QuestionType.SINGLE_CHOICE:
            data["options"] = options
            data["correct_text"] = None
            data["correct_boolean"] = None
            data["correct_option_index"] = correct_option_index
            data["correct_option_indices"] = None
            data["following_question_id"] = None
            
        elif question_type == QuestionType.MULTI_CHOICE:
            data["options"] = options
            data["correct_text"] = None
            data["correct_boolean"] = None
            data["correct_option_index"] = None
            data["correct_option_indices"] = correct_option_indices
            data["following_question_id"] = None
        
        return data

    def delete(self, question_id: int) -> None:
        """Delete a question"""
        return self.repository.delete(question_id)
