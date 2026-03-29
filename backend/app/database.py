import os
from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine


# Build DATABASE_URL from individual environment variables
def _build_database_url() -> str:
    """Build DATABASE_URL from environment variables or defaults."""
    user = os.getenv("POSTGRES_USER", "sports_user")
    password = os.getenv("POSTGRES_PASSWORD", "sports_pass")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "sports_championship")

    # Allow override with DATABASE_URL for backward compatibility
    return os.getenv(
        "DATABASE_URL",
        f"postgresql://{user}:{password}@{host}:{port}/{db}",
    )


DATABASE_URL = _build_database_url()

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,
    max_overflow=20,
)


def create_db_and_tables() -> None:
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session.

    Yields:
        SQLModel Session for database operations
    """
    with Session(engine) as session:
        yield session
