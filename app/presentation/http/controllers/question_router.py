from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from app.infrastructure.dependencies import get_question_service
from app.domain.services.question_service import QuestionService
from app.presentation.http.schemas.question_schemas import (
    CreateQuestionRequest,
    QuestionResponse,
    UpdateQuestionRequest,
)

router = APIRouter(
    prefix="/question",
)


@router.post(
    "/",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new question",
    description="""
    Create a new question with type-specific validation.
    
    **Required fields vary by question type:**
    
    - **TEXT**: question_text, question_type, correct_text
    - **YES_NO**: question_text, question_type, correct_boolean
    - **SINGLE_CHOICE**: question_text, question_type, options, correct_option_index
    - **MULTI_CHOICE**: question_text, question_type, options, correct_option_indices
    
    The API validates that only relevant fields are provided for each type.
    """,
)
def createQuestion(
    request: CreateQuestionRequest,
    service: QuestionService = Depends(get_question_service),
):
    """Create a new question with automatic validation based on question type."""
    try:
        result = service.create(
            request.question_text,
            request.question_type,
            request.options,
            request.correct_text,
            request.correct_boolean,
            request.correct_option_index,
            request.correct_option_indices,
            request.following_question_id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get(
    "/{question_id}",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a question by ID",
    description="Retrieve a specific question by its unique identifier.",
)
def getQuestion(
    question_id: int, service: QuestionService = Depends(get_question_service)
):
    """Get a question by its ID with all type-specific fields."""
    try:
        result = service.get_by_id(question_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Question with id {question_id} not found",
            )
        return result
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put(
    "/{question_id}",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a question",
    description="""
    Update an existing question with type-specific validation.
    
    **Required fields vary by question type:**
    
    - **TEXT**: question_text, question_type, correct_text
    - **YES_NO**: question_text, question_type, correct_boolean
    - **SINGLE_CHOICE**: question_text, question_type, options, correct_option_index
    - **MULTI_CHOICE**: question_text, question_type, options, correct_option_indices
    
    The API validates that only relevant fields are provided for each type.
    """,
)
def updateQuestion(
    question_id: int,
    request: UpdateQuestionRequest,
    service: QuestionService = Depends(get_question_service),
):
    """Update a question with automatic validation based on question type."""
    try:
        result = service.update(
            question_id,
            request.question_text,
            request.question_type,
            request.options,
            request.correct_text,
            request.correct_boolean,
            request.correct_option_index,
            request.correct_option_indices,
            request.following_question_id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a question",
    description="Delete a question by its unique identifier.",
)
def deleteQuestion(
    question_id: int, service: QuestionService = Depends(get_question_service)
):
    """Delete a question by its ID."""
    try:
        service.delete(question_id)
        return {"message": f"Question with id: {question_id} deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
