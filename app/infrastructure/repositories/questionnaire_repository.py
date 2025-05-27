from typing import List, Optional
from sqlalchemy.orm import Session
from app.infrastructure.models.questionnaire_model import QuestionnaireModel
from app.domain.entities.questionnaire import Questionnaire


class QuestionnaireRepository:
    """Repository for questionnaire CRUD operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(
        self,
        title: str,
        description: Optional[str],
        question_ids: List[int]
    ) -> Questionnaire:
        """Create a new questionnaire"""
        try:            
            questionnaire_model = QuestionnaireModel(
                title=title,
                description=description,
                question_ids=question_ids
            )
            
            self.db.add(questionnaire_model)
            self.db.commit()
            self.db.refresh(questionnaire_model)
            
            return Questionnaire(id=questionnaire_model.id, title=questionnaire_model.title, description=questionnaire_model.description, question_ids=questionnaire_model.question_ids, created_at=questionnaire_model.created_at, updated_at=questionnaire_model.updated_at)
            
        except Exception as e:
            self.db.rollback()
            raise e

