from datetime import datetime

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User database model.

    SQLModel table mapping User domain entity to database.
    """

    id: str | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    full_name: str
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """SQLModel config."""

        arbitrary_types_allowed = True
