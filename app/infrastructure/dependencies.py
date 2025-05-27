from sqlalchemy.orm import Session
from fastapi import Depends
from ..infrastructure.repositories.question_repository import QuestionRepository
from ..infrastructure.repositories.questionnaire_repository import (
    QuestionnaireRepository,
)
from ..domain.services.question_service import QuestionService
from ..domain.services.questionnaire_service import QuestionnaireService
from ..db import get_db


def get_db_session() -> Session:
    """Get database session"""
    return next(get_db())


def get_question_repository(
    db: Session = Depends(get_db_session),
) -> QuestionRepository:
    """Get question repository with database session"""
    return QuestionRepository(db)


def get_question_service(
    repo: QuestionRepository = Depends(get_question_repository),
) -> QuestionService:
    """Get question service with repository"""
    return QuestionService(repo)


def get_questionnaire_repository(
    db: Session = Depends(get_db_session),
) -> QuestionnaireRepository:
    """Get questionnaire repository with database session"""
    return QuestionnaireRepository(db)


def get_questionnaire_service(
    questionnaire_repo: QuestionnaireRepository = Depends(get_questionnaire_repository),
    question_repo: QuestionRepository = Depends(get_question_repository),
) -> QuestionnaireService:
    """Get questionnaire service with repositories"""
    return QuestionnaireService(questionnaire_repo, question_repo)
