from typing import List, Optional
from app.domain.entities.question import Question, QuestionType
from app.infrastructure.models.question_model import QuestionModel
from sqlalchemy.orm import Session


class QuestionRepository:
    """Repository for question operations"""

    def __init__(self, db: Session):
        self.db = db

    def _model_to_entity(self, model: QuestionModel) -> Question:
        """Convert QuestionModel to Question domain entity"""
        return Question(
            id=model.id,
            question_text=model.question_text,
            question_type=QuestionType(model.question_type),
            options=model.options,
            correct_text=model.correct_text,
            correct_boolean=model.correct_boolean,
            correct_option_index=model.correct_option_index,
            correct_option_indices=model.correct_option_indices,
            following_question_id=model.following_question_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def create(self, question: Question) -> Question:
        """Create a new question"""
        try:
            question_model = QuestionModel(
                question_text=question.question_text,
                question_type=question.question_type.value,
                options=question.options,
                correct_text=question.correct_text,
                correct_boolean=question.correct_boolean,
                correct_option_index=question.correct_option_index,
                correct_option_indices=question.correct_option_indices,
                following_question_id=question.following_question_id,
            )
            self.db.add(question_model)
            self.db.commit()
            self.db.refresh(question_model)
            return self._model_to_entity(question_model)
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_id(self, question_id: int) -> Optional[Question]:
        """Get a question by its ID"""
        question_model = (
            self.db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
        )
        if not question_model:
            return None
        return self._model_to_entity(question_model)

    def get_all(self) -> List[Question]:
        """Get all questions"""
        question_models = self.db.query(QuestionModel).all()
        return [self._model_to_entity(model) for model in question_models]

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
        """Update a question with validation"""
        question_model = (
            self.db.query(QuestionModel)
            .filter(QuestionModel.id == question_id)
            .first()
        )
        if not question_model:
            raise ValueError(f"Question with id {question_id} not found")

        try:
            question_model.question_text = question_text
            question_model.question_type = question_type.value
            question_model.options = options
            question_model.correct_text = correct_text
            question_model.correct_boolean = correct_boolean
            question_model.correct_option_index = correct_option_index
            question_model.correct_option_indices = correct_option_indices
            question_model.following_question_id = following_question_id

            self.db.commit()
            self.db.refresh(question_model)

            return self._model_to_entity(question_model)
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, question_id: int) -> None:
        """Delete a question"""
        question_model = (
            self.db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
        )
        if not question_model:
            raise ValueError("Question not found")
        try:
            self.db.delete(question_model)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
