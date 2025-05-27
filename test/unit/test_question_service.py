import pytest
from unittest.mock import Mock
from app.domain.services.question_service import QuestionService
from app.domain.entities.question import Question, QuestionType
from app.infrastructure.repositories.question_repository import QuestionRepository


class TestQuestionService:
    """Unit tests for QuestionService"""

    @pytest.fixture
    def mock_repository(self):
        """Create a mock repository"""
        return Mock(spec=QuestionRepository)

    @pytest.fixture
    def question_service(self, mock_repository):
        """Create a question service with the mock repository"""
        return QuestionService(mock_repository)

    def test_create_text_question(
        self, question_service, mock_repository, sample_text_question_data
    ):
        """Test creating a text question through service"""
        mock_question = Question(
            id=1,
            question_text=sample_text_question_data["question_text"],
            question_type=QuestionType.TEXT,
            correct_text=sample_text_question_data["correct_text"],
        )
        mock_repository.create.return_value = mock_question

        result = question_service.create(
            question_text=sample_text_question_data["question_text"],
            question_type=QuestionType.TEXT,
            correct_text=sample_text_question_data["correct_text"],
        )

        assert result.id == 1
        assert result.question_text == sample_text_question_data["question_text"]
        assert result.question_type == QuestionType.TEXT
        mock_repository.create.assert_called_once()

    def test_create_yes_no_question(
        self, question_service, mock_repository, sample_yes_no_question_data
    ):
        """Test creating a yes/no question through service"""
        mock_question = Question(
            id=2,
            question_text=sample_yes_no_question_data["question_text"],
            question_type=QuestionType.YES_NO,
            correct_boolean=sample_yes_no_question_data["correct_boolean"],
        )
        mock_repository.create.return_value = mock_question

        result = question_service.create(
            question_text=sample_yes_no_question_data["question_text"],
            question_type=QuestionType.YES_NO,
            correct_boolean=sample_yes_no_question_data["correct_boolean"],
        )

        assert result.id == 2
        assert result.question_type == QuestionType.YES_NO
        assert result.correct_boolean == True

    def test_create_single_choice_question(
        self, question_service, mock_repository, sample_single_choice_question_data
    ):
        """Test creating a single choice question through service"""
        mock_question = Question(
            id=3,
            question_text=sample_single_choice_question_data["question_text"],
            question_type=QuestionType.SINGLE_CHOICE,
            options=sample_single_choice_question_data["options"],
            correct_option_index=sample_single_choice_question_data[
                "correct_option_index"
            ],
        )
        mock_repository.create.return_value = mock_question

        result = question_service.create(
            question_text=sample_single_choice_question_data["question_text"],
            question_type=QuestionType.SINGLE_CHOICE,
            options=sample_single_choice_question_data["options"],
            correct_option_index=sample_single_choice_question_data[
                "correct_option_index"
            ],
        )

        assert result.id == 3
        assert result.question_type == QuestionType.SINGLE_CHOICE
        assert len(result.options) == 4

    def test_create_multi_choice_question(
        self, question_service, mock_repository, sample_multi_choice_question_data
    ):
        """Test creating a multi choice question through service"""
        mock_question = Question(
            id=4,
            question_text=sample_multi_choice_question_data["question_text"],
            question_type=QuestionType.MULTI_CHOICE,
            options=sample_multi_choice_question_data["options"],
            correct_option_indices=sample_multi_choice_question_data[
                "correct_option_indices"
            ],
        )
        mock_repository.create.return_value = mock_question

        result = question_service.create(
            question_text=sample_multi_choice_question_data["question_text"],
            question_type=QuestionType.MULTI_CHOICE,
            options=sample_multi_choice_question_data["options"],
            correct_option_indices=sample_multi_choice_question_data[
                "correct_option_indices"
            ],
        )

        assert result.id == 4
        assert result.question_type == QuestionType.MULTI_CHOICE
        assert result.correct_option_indices == [0, 2]

    def test_get_by_id(
        self, question_service, mock_repository, sample_text_question_data
    ):
        """Test getting a question by ID through service"""
        mock_question = Question(
            id=1,
            question_text=sample_text_question_data["question_text"],
            question_type=QuestionType.TEXT,
            correct_text=sample_text_question_data["correct_text"],
        )
        mock_repository.get_by_id.return_value = mock_question

        result = question_service.get_by_id(1)

        assert result.id == 1
        assert result.question_text == sample_text_question_data["question_text"]
        mock_repository.get_by_id.assert_called_once_with(1)

    def test_get_by_id_not_found(self, question_service, mock_repository):
        """Test getting a non-existent question"""
        mock_repository.get_by_id.return_value = None

        result = question_service.get_by_id(99999)

        assert result is None

    def test_get_all(self, question_service, mock_repository):
        """Test getting all questions through service"""
        mock_questions = [
            Question(
                id=1,
                question_text="Q1",
                question_type=QuestionType.TEXT,
                correct_text="A1",
            ),
            Question(
                id=2,
                question_text="Q2",
                question_type=QuestionType.YES_NO,
                correct_boolean=True,
            ),
        ]
        mock_repository.get_all.return_value = mock_questions

        result = question_service.get_all()

        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2
        mock_repository.get_all.assert_called_once()

    def test_update_question(
        self, question_service, mock_repository, sample_text_question_data
    ):
        """Test updating a question through service"""
        updated_question = Question(
            id=1,
            question_text="Updated question",
            question_type=QuestionType.TEXT,
            correct_text="Updated answer",
        )
        mock_repository.update.return_value = updated_question

        result = question_service.update(
            question_id=1,
            question_text="Updated question",
            question_type=QuestionType.TEXT,
            correct_text="Updated answer",
        )

        assert result.question_text == "Updated question"
        assert result.correct_text == "Updated answer"
        mock_repository.update.assert_called_once()

    def test_delete_question(self, question_service, mock_repository):
        """Test deleting a question through service"""
        mock_repository.delete.return_value = None

        result = question_service.delete(1)

        mock_repository.delete.assert_called_once_with(1)

    def test_create_propagates_validation_error(
        self, question_service, mock_repository
    ):
        """Test that validation errors from repository are propagated"""
        mock_repository.create.side_effect = ValueError(
            "text questions require: correct_text"
        )

        with pytest.raises(ValueError, match="text questions require: correct_text"):
            question_service.create(
                question_text="Question", question_type=QuestionType.TEXT
            )

    def test_update_question_type_change_text_to_yes_no(
        self, question_service, mock_repository
    ):
        """Test updating a TEXT question to YES_NO type"""
        existing_text_question = Question(
            id=1,
            question_text="Original text question",
            question_type=QuestionType.TEXT,
            correct_text="Answer",
        )
        mock_repository.get_by_id.return_value = existing_text_question

        updated_yes_no_question = Question(
            id=1,
            question_text="Updated question",
            question_type=QuestionType.YES_NO,
            correct_boolean=True,
            following_question_id=None,
        )
        mock_repository.update.return_value = updated_yes_no_question

        result = question_service.update(
            question_id=1,
            question_text="Updated question",
            question_type=QuestionType.YES_NO,
            correct_boolean=True,
        )

        assert result.question_type == QuestionType.YES_NO
        assert result.correct_boolean == True
        assert result.correct_text is None
        mock_repository.update.assert_called_once()

    def test_update_question_type_change_yes_no_to_text(
        self, question_service, mock_repository
    ):
        """Test updating a YES_NO question to TEXT type"""
        existing_yes_no_question = Question(
            id=1,
            question_text="Original yes/no question",
            question_type=QuestionType.YES_NO,
            correct_boolean=True,
            following_question_id=2,
        )
        mock_repository.get_by_id.return_value = existing_yes_no_question

        updated_text_question = Question(
            id=1,
            question_text="Updated question",
            question_type=QuestionType.TEXT,
            correct_text="Answer",
        )
        mock_repository.update.return_value = updated_text_question

        result = question_service.update(
            question_id=1,
            question_text="Updated question",
            question_type=QuestionType.TEXT,
            correct_text="Answer",
        )

        assert result.question_type == QuestionType.TEXT
        assert result.correct_text == "Answer"
        assert result.correct_boolean is None
        assert result.following_question_id is None 
        mock_repository.update.assert_called_once()

    def test_update_question_type_change_single_choice_to_multi_choice(
        self, question_service, mock_repository
    ):
        """Test updating a SINGLE_CHOICE question to MULTI_CHOICE type"""
        existing_single_question = Question(
            id=1,
            question_text="Original single choice question",
            question_type=QuestionType.SINGLE_CHOICE,
            options=["A", "B", "C"],
            correct_option_index=1,
        )
        mock_repository.get_by_id.return_value = existing_single_question

        updated_multi_question = Question(
            id=1,
            question_text="Updated question",
            question_type=QuestionType.MULTI_CHOICE,
            options=["A", "B", "C"],
            correct_option_indices=[0, 2],
        )
        mock_repository.update.return_value = updated_multi_question

        result = question_service.update(
            question_id=1,
            question_text="Updated question",
            question_type=QuestionType.MULTI_CHOICE,
            options=["A", "B", "C"],
            correct_option_indices=[0, 2],
        )

        assert result.question_type == QuestionType.MULTI_CHOICE
        assert result.correct_option_indices == [0, 2]
        assert result.correct_option_index is None
        mock_repository.update.assert_called_once()

    def test_update_question_same_type_preserves_fields(
        self, question_service, mock_repository
    ):
        """Test updating within same type preserves existing fields"""
        existing_text_question = Question(
            id=1,
            question_text="Original question",
            question_type=QuestionType.TEXT,
            correct_text="Old answer",
        )
        mock_repository.get_by_id.return_value = existing_text_question

        updated_text_question = Question(
            id=1,
            question_text="Updated question",
            question_type=QuestionType.TEXT,
            correct_text="New answer",
        )
        mock_repository.update.return_value = updated_text_question

        result = question_service.update(
            question_id=1,
            question_text="Updated question",
            question_type=QuestionType.TEXT,
            correct_text="New answer",
        )

        assert result.question_type == QuestionType.TEXT
        assert result.correct_text == "New answer"
        mock_repository.update.assert_called_once()

    def test_update_question_type_change_with_invalid_existing_data(
        self, question_service, mock_repository
    ):
        """Test that invalid existing question data causes validation error during retrieval"""
        mock_repository.get_by_id.side_effect = ValueError(
            "text questions cannot use: correct_boolean, following_question_id"
        )

        with pytest.raises(ValueError, match="text questions cannot use: correct_boolean"):
            question_service.update(
                question_id=1,
                question_text="Updated question",
                question_type=QuestionType.TEXT,
                correct_text="Answer",
            )
