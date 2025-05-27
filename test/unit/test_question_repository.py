import pytest
from sqlalchemy import text
from app.infrastructure.repositories.question_repository import QuestionRepository
from app.domain.entities.question import Question, QuestionType
from app.infrastructure.models.question_model import QuestionModel


class TestQuestionRepository:
    """Unit tests for QuestionRepository"""

    def test_create_text_question(self, test_db, sample_text_question_data):
        """Test creating a text question"""
        repository = QuestionRepository(test_db)

        question_entity = Question(
            id=None,
            question_text=sample_text_question_data["question_text"],
            question_type=QuestionType.TEXT,
            correct_text=sample_text_question_data["correct_text"],
        )

        question = repository.create(question_entity)

        assert question.id is not None
        assert question.question_text == sample_text_question_data["question_text"]
        assert question.question_type == QuestionType.TEXT
        assert question.correct_text == sample_text_question_data["correct_text"]

    def test_create_yes_no_question(self, test_db, sample_yes_no_question_data):
        """Test creating a yes/no question"""
        repository = QuestionRepository(test_db)

        question_entity = Question(
            id=None,
            question_text=sample_yes_no_question_data["question_text"],
            question_type=QuestionType.YES_NO,
            correct_boolean=sample_yes_no_question_data["correct_boolean"],
        )

        question = repository.create(question_entity)

        assert question.id is not None
        assert question.question_type == QuestionType.YES_NO
        assert question.correct_boolean == True

    def test_create_single_choice_question(
        self, test_db, sample_single_choice_question_data
    ):
        """Test creating a single choice question"""
        repository = QuestionRepository(test_db)

        question_entity = Question(
            id=None,
            question_text=sample_single_choice_question_data["question_text"],
            question_type=QuestionType.SINGLE_CHOICE,
            options=sample_single_choice_question_data["options"],
            correct_option_index=sample_single_choice_question_data[
                "correct_option_index"
            ],
        )

        question = repository.create(question_entity)

        assert question.id is not None
        assert question.question_type == QuestionType.SINGLE_CHOICE
        assert question.options == sample_single_choice_question_data["options"]
        assert question.correct_option_index == 1

    def test_create_multi_choice_question(
        self, test_db, sample_multi_choice_question_data
    ):
        """Test creating a multi choice question"""
        repository = QuestionRepository(test_db)

        question_entity = Question(
            id=None,
            question_text=sample_multi_choice_question_data["question_text"],
            question_type=QuestionType.MULTI_CHOICE,
            options=sample_multi_choice_question_data["options"],
            correct_option_indices=sample_multi_choice_question_data[
                "correct_option_indices"
            ],
        )

        question = repository.create(question_entity)

        assert question.id is not None
        assert question.question_type == QuestionType.MULTI_CHOICE
        assert question.correct_option_indices == [0, 2]

    def test_get_by_id(self, test_db, sample_text_question_data):
        """Test getting a question by ID"""
        repository = QuestionRepository(test_db)

        question_entity = Question(
            id=None,
            question_text=sample_text_question_data["question_text"],
            question_type=QuestionType.TEXT,
            correct_text=sample_text_question_data["correct_text"],
        )

        created_question = repository.create(question_entity)

        retrieved_question = repository.get_by_id(created_question.id)

        assert retrieved_question is not None
        assert retrieved_question.id == created_question.id
        assert (
            retrieved_question.question_text
            == sample_text_question_data["question_text"]
        )

    def test_get_by_id_not_found(self, test_db):
        """Test getting a non-existent question"""
        repository = QuestionRepository(test_db)

        question = repository.get_by_id(99999)

        assert question is None

    def test_update_question(self, test_db, sample_text_question_data):
        """Test updating a question"""
        repository = QuestionRepository(test_db)

        question_entity = Question(
            id=None,
            question_text=sample_text_question_data["question_text"],
            question_type=QuestionType.TEXT,
            correct_text=sample_text_question_data["correct_text"],
        )

        created_question = repository.create(question_entity)

        updated_question = repository.update(
            question_id=created_question.id,
            question_text="Updated question text",
            question_type=QuestionType.TEXT,
            correct_text="Updated answer",
        )

        assert updated_question.question_text == "Updated question text"
        assert updated_question.correct_text == "Updated answer"

    def test_update_nonexistent_question(self, test_db):
        """Test updating a non-existent question"""
        repository = QuestionRepository(test_db)

        with pytest.raises(ValueError, match="Question with id .* not found"):
            repository.update(
                question_id=99999,
                question_text="Updated text",
                question_type=QuestionType.TEXT,
                correct_text="Answer",
            )

    def test_delete_question(self, test_db, sample_text_question_data):
        """Test deleting a question"""
        repository = QuestionRepository(test_db)

        question_entity = Question(
            id=None,
            question_text=sample_text_question_data["question_text"],
            question_type=QuestionType.TEXT,
            correct_text=sample_text_question_data["correct_text"],
        )

        created_question = repository.create(question_entity)

        repository.delete(created_question.id)

        deleted_question = repository.get_by_id(created_question.id)
        assert deleted_question is None

    def test_delete_nonexistent_question(self, test_db):
        """Test deleting a non-existent question"""
        repository = QuestionRepository(test_db)

        with pytest.raises(ValueError, match="Question not found"):
            repository.delete(99999)

