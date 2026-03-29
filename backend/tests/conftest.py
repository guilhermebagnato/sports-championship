"""Pytest Configuration and Fixtures."""
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.adapters.repositories import UserRepository
from app.application.services import AuthService
from app.database import get_session
from app.domain.entities import User as UserEntity
from app.main import app

# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(name="engine")
def engine_fixture():
    """Create test database engine."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=None,
    )
    # Create all tables (metadata is populated by imports above)
    SQLModel.metadata.create_all(engine)
    yield engine


@pytest.fixture(name="session")
def session_fixture(engine) -> Generator[Session, None, None]:
    """Create test database session with transaction isolation."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(
        bind=connection,
        expire_on_commit=False,
    )
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(name="client")
def client_fixture(session: Session) -> TestClient:
    """Create FastAPI TestClient with test database session."""

    def get_session_override() -> Generator[Session, None, None]:
        """Override get_session to use test session."""
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="auth_service")
def auth_service_fixture() -> AuthService:
    """Create AuthService for testing."""
    return AuthService(
        secret_key="test-secret-key",
        algorithm="HS256",
        expire_minutes=30,
    )


@pytest.fixture(name="test_user_entity")
def test_user_entity_fixture() -> UserEntity:
    """Create a test user entity."""
    return UserEntity(
        id="test-user-1",
        email="test@example.com",
        full_name="Test User",
        hashed_password="$2b$12$hashedpassword",
        is_active=True,
    )


@pytest.fixture(name="test_user_in_db")
async def test_user_in_db_fixture(session: Session, test_user_entity: UserEntity) -> UserEntity:
    """Create and persist a test user."""
    repository = UserRepository(session)
    user = await repository.create(test_user_entity)
    return user


@pytest.fixture(name="test_token")
def test_token_fixture(auth_service: AuthService, test_user_entity: UserEntity) -> str:
    """Create a test JWT token."""
    return auth_service.create_access_token(test_user_entity.id)
