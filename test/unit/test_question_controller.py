import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from datetime import datetime
from app.api import app
from app.domain.entities.question import Question, QuestionType
from app.domain.services.question_service import QuestionService
from app.infrastructure.dependencies import get_question_service


@pytest.fixture(autouse=True)
def clear_overrides():
    """Automatically clear dependency overrides after each test"""
    yield
    app.dependency_overrides.clear()


class TestQuestionController:
    """Unit tests for Question Router/Controller"""

    @pytest.fixture
    def client(self):
        """Create a test client"""
        return TestClient(app)

    @pytest.fixture
    def mock_service(self):
        """Create a mock question service"""
        return Mock(spec=QuestionService)

    def test_create_text_question_success(
        self, client, mock_service, sample_text_question_data
    ):
        """Test successful creation of text question"""
        mock_question = Question(
            id=1,
            question_text=sample_text_question_data["question_text"],
            question_type=QuestionType.TEXT,
            correct_text=sample_text_question_data["correct_text"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_service.create.return_value = mock_question
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.post("/question/", json=sample_text_question_data)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["question_text"] == sample_text_question_data["question_text"]
        assert data["question_type"] == "text"

    def test_create_yes_no_question_success(
        self, client, mock_service, sample_yes_no_question_data
    ):
        """Test successful creation of yes/no question"""
        mock_question = Question(
            id=2,
            question_text=sample_yes_no_question_data["question_text"],
            question_type=QuestionType.YES_NO,
            correct_boolean=sample_yes_no_question_data["correct_boolean"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_service.create.return_value = mock_question
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.post("/question/", json=sample_yes_no_question_data)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 2
        assert data["correct_boolean"] == True

    def test_create_single_choice_question_success(
        self, client, mock_service, sample_single_choice_question_data
    ):
        """Test successful creation of single choice question"""
        mock_question = Question(
            id=3,
            question_text=sample_single_choice_question_data["question_text"],
            question_type=QuestionType.SINGLE_CHOICE,
            options=sample_single_choice_question_data["options"],
            correct_option_index=sample_single_choice_question_data[
                "correct_option_index"
            ],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_service.create.return_value = mock_question
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.post("/question/", json=sample_single_choice_question_data)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 3
        assert len(data["options"]) == 4

    def test_create_multi_choice_question_success(
        self, client, mock_service, sample_multi_choice_question_data
    ):
        """Test successful creation of multi choice question"""
        mock_question = Question(
            id=4,
            question_text=sample_multi_choice_question_data["question_text"],
            question_type=QuestionType.MULTI_CHOICE,
            options=sample_multi_choice_question_data["options"],
            correct_option_indices=sample_multi_choice_question_data[
                "correct_option_indices"
            ],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_service.create.return_value = mock_question
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.post("/question/", json=sample_multi_choice_question_data)

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 4
        assert data["correct_option_indices"] == [0, 2]

    def test_create_question_validation_error(self, client, mock_service):
        """Test creation with validation error returns 400"""
        mock_service.create.side_effect = ValueError(
            "text questions require: correct_text"
        )
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.post(
            "/question/",
            json={"question_text": "Question without answer", "question_type": "text"},
        )

        assert response.status_code == 400
        assert "correct_text" in response.json()["detail"]

    def test_create_question_with_wrong_field_returns_400(self, client, mock_service):
        """Test creation with field from wrong type returns 400"""
        mock_service.create.side_effect = ValueError(
            "text questions cannot use: correct_boolean"
        )
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.post(
            "/question/",
            json={
                "question_text": "Question",
                "question_type": "text",
                "correct_text": "Answer",
                "correct_boolean": True,
            },
        )

        assert response.status_code == 400
        assert "correct_boolean" in response.json()["detail"]

    def test_get_question_by_id_success(
        self, client, mock_service, sample_text_question_data
    ):
        """Test successfully getting a question by ID"""
        mock_question = Question(
            id=1,
            question_text=sample_text_question_data["question_text"],
            question_type=QuestionType.TEXT,
            correct_text=sample_text_question_data["correct_text"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_service.get_by_id.return_value = mock_question
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.get("/question/1")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["question_text"] == sample_text_question_data["question_text"]

    def test_get_question_by_id_not_found(self, client, mock_service):
        """Test getting non-existent question returns 404"""
        mock_service.get_by_id.return_value = None
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.get("/question/99999")

        assert response.status_code == 404
        detail = response.json()["detail"].lower()
        assert "not found" in detail or "99999" in detail

    def test_update_question_success(
        self, client, mock_service, sample_text_question_data
    ):
        """Test successfully updating a question"""
        updated_question = Question(
            id=1,
            question_text="Updated question",
            question_type=QuestionType.TEXT,
            correct_text="Updated answer",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        mock_service.update.return_value = updated_question
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.put(
            "/question/1",
            json={
                "question_text": "Updated question",
                "question_type": "text",
                "correct_text": "Updated answer",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["question_text"] == "Updated question"
        assert data["correct_text"] == "Updated answer"

    def test_update_question_validation_error(self, client, mock_service):
        """Test update with validation error returns 400"""
        mock_service.update.side_effect = ValueError("Question not found")
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.put(
            "/question/99999",
            json={
                "question_text": "Updated",
                "question_type": "text",
                "correct_text": "Answer",
            },
        )

        assert response.status_code == 400
        assert "not found" in response.json()["detail"]

    def test_delete_question_success(self, client, mock_service):
        """Test successfully deleting a question"""
        mock_service.delete.return_value = None
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.delete("/question/1")

        assert response.status_code == 200
        data = response.json()
        assert "deleted successfully" in data["message"]

    def test_delete_question_not_found(self, client, mock_service):
        """Test deleting non-existent question returns 400"""
        mock_service.delete.side_effect = ValueError("Question not found")
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.delete("/question/99999")

        assert response.status_code == 400
        assert "not found" in response.json()["detail"]

    def test_create_question_server_error(self, client, mock_service):
        """Test that unexpected errors return 500"""
        mock_service.create.side_effect = Exception("Database connection failed")
        app.dependency_overrides[get_question_service] = lambda: mock_service

        response = client.post(
            "/question/",
            json={
                "question_text": "Question",
                "question_type": "text",
                "correct_text": "Answer",
            },
        )

        assert response.status_code == 500
        assert "Database connection failed" in response.json()["detail"]

    def test_invalid_question_type(self, client):
        """Test that invalid question type is rejected by Pydantic"""
        response = client.post(
            "/question/",
            json={
                "question_text": "Question",
                "question_type": "invalid_type",
                "correct_text": "Answer",
            },
        )

        assert response.status_code == 422  # Pydantic validation error
