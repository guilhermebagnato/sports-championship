from datetime import UTC
from typing import cast

from app.application.ports import IAuthService


class AuthService(IAuthService):
    """Auth service implementation.

    Encapsulates authentication use cases: token creation, password hashing, verification.
    """

    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int) -> None:
        """Initialize AuthService.

        Args:
            secret_key: JWT secret key
            algorithm: JWT algorithm (e.g., 'HS256')
            expire_minutes: Token expiration time in minutes
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def hash_password(self, password: str) -> str:
        """Hash a plain text password using bcrypt via passlib.

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        from passlib.context import CryptContext  # type: ignore[import-untyped]

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return cast(str, pwd_context.hash(password))

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against hashed password.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Previously hashed password

        Returns:
            True if password matches, False otherwise
        """
        from passlib.context import CryptContext  # type: ignore[import-untyped]

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        try:
            return cast(bool, pwd_context.verify(plain_password, hashed_password))
        except Exception:
            return False

    def create_access_token(self, user_id: str, expires_delta: int | None = None) -> str:
        """Create JWT access token for user.

        Args:
            user_id: User ID to encode in token
            expires_delta: Expiration time in minutes (uses default if None)

        Returns:
            JWT token string
        """
        from datetime import datetime, timedelta

        from jose import jwt  # type: ignore[import-untyped]

        if expires_delta is None:
            expires_delta = self.expire_minutes

        expire = datetime.now(UTC) + timedelta(minutes=expires_delta)
        to_encode = {"sub": user_id, "exp": expire}

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return cast(str, encoded_jwt)

    def decode_token(self, token: str) -> str | None:
        """Decode JWT token and return user_id if valid.

        Args:
            token: JWT token to decode

        Returns:
            User ID if token is valid, None otherwise
        """
        try:
            from jose import jwt

            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return user_id
        except Exception:
            return None
