import importlib
import os

from app import database
from app.database import create_db_and_tables, get_session


def test_database_session_generation() -> None:
    """Test the get_session generator explicitly."""
    generator = get_session()
    session = next(generator)
    assert session is not None
    # We don't need to do much, just ensure it yields a session
    # Cleanup (normally handled by FastAPI/generator termination)
    try:
        next(generator)
    except StopIteration:
        pass


def test_create_tables() -> None:
    """Test create_db_and_tables function."""
    # This should run without error using the default engine (SQLite in memory for tests if configured)
    # Even if it uses the real engine, it should be fine as it's idempotent.
    create_db_and_tables()
    assert True


def test_postgres_engine_config() -> None:
    """Test that Postgres engine configurations are handled (covers the else block)."""
    # Save original
    original_url = os.environ.get("DATABASE_URL")

    try:
        # Mock Postgres URL
        postgres_url = "postgresql://user:pass@host:5432/db"
        os.environ["DATABASE_URL"] = postgres_url

        # Reset the singleton and reload module
        database._engine = None
        importlib.reload(database)

        # Call get_engine to trigger the logic
        engine = database.get_engine()

        # Verify URL (SQLAlchemy URL object string representation)
        assert engine.url.render_as_string(hide_password=False) == postgres_url
    finally:
        # Restore original and reload to keep tests stable
        if original_url:
            os.environ["DATABASE_URL"] = original_url
        else:
            del os.environ["DATABASE_URL"]
        database._engine = None
        importlib.reload(database)
