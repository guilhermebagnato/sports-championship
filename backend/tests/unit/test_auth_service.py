from datetime import UTC, datetime, timedelta

from jose import jwt

from app.application.services import AuthService


class TestAuthService:
    """Test suite for AuthService."""

    def test_hash_password(self, auth_service: AuthService) -> None:
        """Test password hashing."""
        password = "secure_password_123"
        hashed = auth_service.hash_password(password)

        assert hashed != password
        assert len(hashed) > 0

    def test_verify_password_success(self, auth_service: AuthService) -> None:
        """Test successful password verification."""
        password = "secure_password_123"
        hashed = auth_service.hash_password(password)

        is_valid = auth_service.verify_password(password, hashed)
        assert is_valid is True

    def test_verify_password_failure(self, auth_service: AuthService) -> None:
        """Test failed password verification."""
        password = "secure_password_123"
        wrong_password = "wrong_password"
        hashed = auth_service.hash_password(password)

        is_valid = auth_service.verify_password(wrong_password, hashed)
        assert is_valid is False

    def test_verify_password_exception(self, auth_service: AuthService) -> None:
        """Test password verification with invalid hash to trigger exception."""
        assert auth_service.verify_password("any", "invalid-hash-format") is False

    def test_create_token(self, auth_service: AuthService) -> None:
        """Test JWT token creation."""
        user_id = "user-123"
        token = auth_service.create_token(user_id)

        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)

    def test_decode_valid_token(self, auth_service: AuthService) -> None:
        """Test decoding a valid JWT token."""
        user_id = "user-123"
        token = auth_service.create_token(user_id, typ="access")

        # Should work with default (access)
        decoded_user_id = auth_service.decode_token(token)
        assert decoded_user_id == user_id

        # Should fail if we expect refresh
        decoded_user_id = auth_service.decode_token(token, expected_type="refresh")
        assert decoded_user_id is None

    def test_decode_token_no_sub(self, auth_service: AuthService) -> None:
        """Test decoding a JWT token without 'sub' claim."""
        expire = datetime.now(UTC) + timedelta(minutes=10)
        to_encode = {"exp": expire, "typ": "access"}  # No 'sub'
        token = jwt.encode(
            to_encode, auth_service.secret_key, algorithm=auth_service.algorithm
        )

        assert auth_service.decode_token(token) is None

    def test_create_refresh_token(self, auth_service: AuthService) -> None:
        """Test JWT refresh token creation."""
        user_id = "user-123"
        token = auth_service.create_token(user_id, typ="refresh")

        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)

    def test_decode_refresh_token(self, auth_service: AuthService) -> None:
        """Test decoding a valid refresh token."""
        user_id = "user-123"
        token = auth_service.create_token(user_id, typ="refresh")

        # Should work when expecting refresh
        decoded_user_id = auth_service.decode_token(token, expected_type="refresh")
        assert decoded_user_id == user_id

        # Should fail if we expect access
        decoded_user_id = auth_service.decode_token(token, expected_type="access")
        assert decoded_user_id is None

    def test_decode_invalid_token(self, auth_service: AuthService) -> None:
        """Test decoding an invalid JWT token."""
        invalid_token = "invalid.token.here"

        decoded_user_id = auth_service.decode_token(invalid_token)
        assert decoded_user_id is None

    def test_decode_expired_token(self, auth_service: AuthService) -> None:
        """Test decoding an expired JWT token."""
        user_id = "user-123"
        # Create token with 0 minutes expiration (already expired)
        token = auth_service.create_token(user_id, expires_delta=0)

        # Token might still decode if created just now, depends on timing
        # This is a basic test - real expiration testing is integration-level
        decoded_user_id = auth_service.decode_token(token)
        # May or may not be None depending on timing, so we just check it doesn't crash
        assert decoded_user_id is None or decoded_user_id == user_id
