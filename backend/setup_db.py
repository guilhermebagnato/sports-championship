"""
Database initialization and seed data script.

This script creates tables and populates initial data for development/testing.
To be run after database connection is verified.
"""

import logging

from sqlmodel import SQLModel

from app.database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables() -> None:
    """Create all tables in the database."""
    logger.info("Creating tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Tables created successfully")


def seed_data() -> None:
    """Seed initial data to database.

    To be implemented with initial users, championships, etc.
    """
    logger.info("Seed data not implemented yet")


if __name__ == "__main__":
    create_tables()
    seed_data()
    logger.info("Database setup completed")
