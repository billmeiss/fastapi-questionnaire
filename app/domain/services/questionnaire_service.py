from typing import List, Optional
from app.domain.entities.questionnaire import Questionnaire
from app.infrastructure.repositories.questionnaire_repository import (
    QuestionnaireRepository,
)
from app.infrastructure.repositories.question_repository import QuestionRepository


class QuestionnaireService:
    """Domain service for questionnaire business logic"""

    def __init__(
        self,
        questionnaire_repository: QuestionnaireRepository,
        question_repository: QuestionRepository,
    ):
        self.questionnaire_repository = questionnaire_repository
        self.question_repository = question_repository

    def create_questionnaire(
        self, title: str, description: Optional[str], question_ids: List[int]
    ) -> Questionnaire:
        """Create a questionnaire after validating questions exist"""
        self._validate_questions_exist(question_ids)

        questionnaire = Questionnaire(
            id=None, title=title, description=description, question_ids=question_ids
        )
        return self.questionnaire_repository.create(questionnaire)

    def _validate_questions_exist(self, question_ids: List[int]):
        """Validate all question IDs exist in database"""
        for question_id in question_ids:
            question = self.question_repository.get_by_id(question_id)
            if not question:
                raise ValueError(f"Question with id {question_id} does not exist")
