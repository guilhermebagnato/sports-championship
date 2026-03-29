from datetime import datetime


class User:
    """
    User entity.

    Domain entity representing a user in the system.
    Participants or administrators of championships.

    Attributes:
        id: Unique identifier (UUID)
        email: User email address (unique)
        full_name: User's full name
        hashed_password: Bcrypt hashed password
        is_active: Whether user account is active
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """

    def __init__(
        self,
        id: str,
        email: str,
        full_name: str,
        hashed_password: str,
        is_active: bool = True,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ) -> None:
        """Initialize User entity."""
        self.id = id
        self.email = email
        self.full_name = full_name
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __eq__(self, other: object) -> bool:
        """Compare users by id."""
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash user by id."""
        return hash(self.id)

    def __repr__(self) -> str:
        """String representation of User."""
        return (
            f"User(id={self.id!r}, email={self.email!r}, full_name={self.full_name!r})"
        )
