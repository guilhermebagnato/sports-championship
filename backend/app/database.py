import os
from collections.abc import Generator
from typing import Any

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


_engine = None


def get_engine() -> Any:
    """Get or create the database engine (Lazy initialization).

    Returns:
        SQLModel engine instance
    """
    global _engine
    if _engine is None:
        database_url = _build_database_url()

        # Connection pooling arguments (Postgres only)
        connect_args = {}
        engine_kwargs: dict[str, Any] = {
            "echo": False,
            "future": True,
        }

        if database_url.startswith("sqlite"):
            connect_args["check_same_thread"] = False
        else:
            engine_kwargs.update(
                {
                    "pool_pre_ping": True,
                    "pool_size": 10,
                    "max_overflow": 20,
                }
            )

        # Create engine
        _engine = create_engine(
            database_url,
            connect_args=connect_args,
            **engine_kwargs,
        )

    return _engine


def create_db_and_tables() -> None:
    """Create all database tables."""
    SQLModel.metadata.create_all(get_engine())


def get_session() -> Generator[Session, None, None]:
    """Get database session.

    Yields:
        SQLModel Session for database operations
    """
    with Session(get_engine()) as session:
        yield session
