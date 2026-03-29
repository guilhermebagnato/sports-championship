"""Application Layer: Ports (Abstract Base Classes)."""
from abc import ABC, abstractmethod

from app.domain.entities import User


class IUserRepository(ABC):
    """Port: User Repository Interface.

    Abstraction for user persistence. Implemented by adapters.
    """

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Retrieve user by email address."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None:
        """Retrieve user by ID."""
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create new user."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update existing user."""
        pass


class IAuthService(ABC):
    """Port: Auth Service Interface.

    Abstraction for authentication operations.
    """

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash a plain text password."""
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against hashed password."""
        pass

    @abstractmethod
    def create_access_token(self, user_id: str, expires_delta: int | None = None) -> str:
        """Create JWT access token for user."""
        pass

    @abstractmethod
    def decode_token(self, token: str) -> str | None:
        """Decode JWT token and return user_id if valid."""
        pass
