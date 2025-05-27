import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from urllib.parse import urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from app.api import app
from app.db import get_db, Base
from app.infrastructure.dependencies import get_db_session

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost/challenge_db_test"
)

# Safety check: Ensure we're not using production database
PRODUCTION_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/challenge_db"
)

parsed_test = urlparse(TEST_DATABASE_URL)
parsed_prod = urlparse(PRODUCTION_DATABASE_URL)
test_db_name = parsed_test.path[1:] if parsed_test.path.startswith('/') else parsed_test.path
prod_db_name = parsed_prod.path[1:] if parsed_prod.path.startswith('/') else parsed_prod.path

if test_db_name == prod_db_name:
    raise ValueError(
        f"E2E tests cannot use production database '{prod_db_name}'!\n"
        f"TEST_DATABASE_URL: {TEST_DATABASE_URL}\n"
        f"DATABASE_URL: {PRODUCTION_DATABASE_URL}\n"
        f"Set TEST_DATABASE_URL environment variable to a different database."
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
            print(f"[E2E] Created test database: {database_name}")
        else:
            print(f"[E2E] Test database already exists: {database_name}")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[E2E] Error creating test database: {e}")
        raise


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create test database and tables once at the start of the test session"""
    parsed = urlparse(TEST_DATABASE_URL)
    database_name = parsed.path[1:]
    
    print(f"\n[E2E Tests] Using TEST database: {database_name}")
    
    create_test_database_if_not_exists()

    engine = create_engine(TEST_DATABASE_URL)
    try:
        Base.metadata.create_all(bind=engine)
        print(f"[E2E] Created test database tables in: {database_name}")
    except Exception as e:
        print(f"[E2E] Error creating tables: {e}")
        raise
    finally:
        engine.dispose()

    yield

    # Clean up: drop tables after all tests complete
    try:
        engine = create_engine(TEST_DATABASE_URL)
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
        print(f"[E2E] Dropped test database tables from: {database_name}")
    except Exception as e:
        print(f"[E2E] Error dropping tables: {e}")


# Create test database engine and session factory (reused across tests)
_test_engine = None
_TestSessionLocal = None


def get_test_session_factory():
    """Get or create test database session factory"""
    global _test_engine, _TestSessionLocal
    
    if _test_engine is None:
        _test_engine = create_engine(TEST_DATABASE_URL)
        _TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)
    
    return _TestSessionLocal


def override_get_db():
    """Override get_db to use test database instead of production"""
    TestingSessionLocal = get_test_session_factory()
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_db_session():
    """Override get_db_session to use test database instead of production"""
    TestingSessionLocal = get_test_session_factory()
    return TestingSessionLocal()


@pytest.fixture(autouse=True)
def override_database_dependency():
    """Override database dependencies to use test database for each test"""
    # Override both get_db and get_db_session to ensure test database is used
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_db_session] = override_get_db_session
    
    # Print which database we're using
    parsed = urlparse(TEST_DATABASE_URL)
    db_name = parsed.path[1:] if parsed.path.startswith('/') else parsed.path
    print(f"[E2E] Using test database: {db_name}")
    
    yield
    
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    """Create test client with test database override"""
    return TestClient(app)

