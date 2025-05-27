import pytest
import sys
import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from urllib.parse import urlparse, urlunparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.db import Base, get_db
from app.infrastructure.models.question_model import QuestionModel
from app.infrastructure.models.questionnaire_model import QuestionnaireModel

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost/challenge_db_test"
)

def create_test_database_if_not_exists():
    """Create the test database if it doesn't exist using psycopg2 directly"""
    parsed = urlparse(TEST_DATABASE_URL)
    database_name = parsed.path[1:]  # Remove leading '/'

    user = parsed.username or "postgres"
    password = parsed.password or ""
    host = parsed.hostname or "localhost"
    port = parsed.port or 5432

    try:
        conn = psycopg2.connect(
            dbname="postgres", user=user, password=password, host=host, port=port
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (database_name,))
        exists = cursor.fetchone() is not None

        if not exists:
            cursor.execute(
                f"""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = %s
                AND pid <> pg_backend_pid()
                """,
                (database_name,),
            )
            cursor.execute(f'CREATE DATABASE "{database_name}"')
            print(f"Created test database: {database_name}")
        else:
            print(f"Test database already exists: {database_name}")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creating test database: {e}")
        raise


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create test database and tables once at the start of the test session"""
    create_test_database_if_not_exists()

    engine = create_engine(TEST_DATABASE_URL)
    try:
        Base.metadata.create_all(bind=engine)
        print("Created test database tables")
    except Exception as e:
        print(f"Error creating tables: {e}")
        raise
    finally:
        engine.dispose()

    yield

    # Optional: Clean up database after all tests
    # Uncomment if you want to drop the database after all tests complete
    # parsed = urlparse(TEST_DATABASE_URL)
    # database_name = parsed.path[1:]
    # try:
    #     conn = psycopg2.connect(
    #         dbname='postgres',
    #         user=parsed.username or 'postgres',
    #         password=parsed.password or '',
    #         host=parsed.hostname or 'localhost',
    #         port=parsed.port or 5432
    #     )
    #     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    #     cursor = conn.cursor()
    #     cursor.execute(f'DROP DATABASE IF EXISTS "{database_name}"')
    #     cursor.close()
    #     conn.close()
    # except Exception as e:
    #     print(f"Error dropping test database: {e}")


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database session for each test with transaction rollback"""
    engine = create_engine(TEST_DATABASE_URL)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        transaction.rollback()
        connection.close()
        session.close()
        engine.dispose()


@pytest.fixture
def sample_document_data():
    """Sample document data for testing"""
    return {
        "title": "Test Document",
        "filename": "test.pdf",
        "file_size": 1024,
        "description": "Test description",
    }


@pytest.fixture
def sample_document_data_without_description():
    """Sample document data without description for testing"""
    return {"title": "Test Document", "filename": "test.pdf", "file_size": 1024}


@pytest.fixture
def sample_text_question_data():
    """Sample text question data for testing"""
    return {
        "question_text": "What is the capital of France?",
        "question_type": "text",
        "correct_text": "Paris",
    }


@pytest.fixture
def sample_yes_no_question_data():
    """Sample yes/no question data for testing"""
    return {
        "question_text": "Is Python a programming language?",
        "question_type": "yes_no",
        "correct_boolean": True,
    }


@pytest.fixture
def sample_single_choice_question_data():
    """Sample single choice question data for testing"""
    return {
        "question_text": "What color is the sky?",
        "question_type": "single_choice",
        "options": ["Red", "Blue", "Green", "Yellow"],
        "correct_option_index": 1,
    }


@pytest.fixture
def sample_multi_choice_question_data():
    """Sample multi choice question data for testing"""
    return {
        "question_text": "Which are programming languages?",
        "question_type": "multi_choice",
        "options": ["Python", "HTML", "Java", "CSS"],
        "correct_option_indices": [0, 2],
    }
