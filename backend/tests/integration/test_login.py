import pytest
from fastapi.testclient import TestClient
from jose import jwt

from app.auth import ALGORITHM, SECRET_KEY


class TestUserLogin:
    """Test suite for User Login endpoint."""

    @pytest.mark.asyncio
    async def test_login_success(self, client: TestClient, test_user_in_db) -> None:
        """Test successful login.

        Scenario: POST /api/auth/token with valid user credentials.
        Expected: 200 OK, returns 'access_token' and 'token_type' == 'bearer'.
        """
        response = client.post(
            "/api/auth/token",
            json={
                "email": test_user_in_db.email,
                "password": "password123",
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_invalid_email(self, client: TestClient) -> None:
        """Test login with non-existent email.

        Scenario: POST /api/auth/token with unknown email.
        Expected: 401 Unauthorized.
        """
        response = client.post(
            "/api/auth/token",
            json={
                "email": "nonexistent@example.com",
                "password": "any_password",
            },
        )

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_login_wrong_password(
        self, client: TestClient, test_user_in_db
    ) -> None:
        """Test login with correct email but wrong password.

        Scenario: POST /api/auth/token with valid email but wrong password.
        Expected: 401 Unauthorized.
        """
        response = client.post(
            "/api/auth/token",
            json={
                "email": test_user_in_db.email,
                "password": "wrong_password",
            },
        )

        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_login_token_format(
        self, client: TestClient, test_user_in_db
    ) -> None:
        """Test that the returned token is a valid JWT.

        Scenario: POST /api/auth/token successful.
        Expected: The access_token can be decoded and contains 'sub' (user_id).
        """
        response = client.post(
            "/api/auth/token",
            json={
                "email": test_user_in_db.email,
                "password": "password123",
            },
        )

        assert response.status_code == 200
        token = response.json()["access_token"]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == test_user_in_db.id
