from fastapi import APIRouter, Depends, HTTPException, status
from app.presentation.http.schemas.questionnaire_schemas import (
    QuestionnaireCreate,
    QuestionnaireResponse,
)
from app.domain.services.questionnaire_service import QuestionnaireService
from app.infrastructure.dependencies import get_questionnaire_service


router = APIRouter(prefix="/questionnaire", tags=["questionnaire"])


@router.post(
    "/",
    response_model=QuestionnaireResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new questionnaire",
)
def create_questionnaire(
    request: QuestionnaireCreate,
    service: QuestionnaireService = Depends(get_questionnaire_service),
):
    """
    Create a new questionnaire with an ordered list of question IDs.

    The order of question_ids in the array determines the order of questions.
    """
    try:
        questionnaire = service.create_questionnaire(
            title=request.title,
            description=request.description,
            question_ids=request.question_ids,
        )

        return QuestionnaireResponse(
            id=questionnaire.id,
            title=questionnaire.title,
            description=questionnaire.description,
            question_ids=questionnaire.question_ids,
            created_at=questionnaire.created_at,
            updated_at=questionnaire.updated_at,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )
