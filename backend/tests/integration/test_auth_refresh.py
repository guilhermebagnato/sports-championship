import pytest
from fastapi.testclient import TestClient
from jose import jwt

from app.auth import ALGORITHM, SECRET_KEY


class TestAuthRefresh:
    """Test suite for Token Refresh endpoint."""

    @pytest.mark.asyncio
    async def test_refresh_success(self, client: TestClient, test_user_in_db) -> None:
        """Test successful token refresh.

        Scenario: POST /api/auth/token then POST /api/auth/refresh with refresh_token.
        Expected: 200 OK, returns new 'access_token' and same 'refresh_token'.
        """
        # 1. Login to get tokens
        login_res = client.post(
            "/api/auth/token",
            json={
                "email": test_user_in_db.email,
                "password": "password123",
            },
        )
        assert login_res.status_code == 200
        tokens = login_res.json()
        refresh_token = tokens["refresh_token"]

        # 2. Refresh tokens
        refresh_res = client.post(
            "/api/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert refresh_res.status_code == 200
        new_tokens = refresh_res.json()
        assert "access_token" in new_tokens
        assert new_tokens["refresh_token"] == refresh_token

        # 3. Verify new access token
        payload = jwt.decode(
            new_tokens["access_token"], SECRET_KEY, algorithms=[ALGORITHM]
        )
        assert payload["sub"] == test_user_in_db.id
        assert payload["typ"] == "access"

    @pytest.mark.asyncio
    async def test_refresh_invalid_token(self, client: TestClient) -> None:
        """Test refresh with invalid token.

        Scenario: POST /api/auth/refresh with garbage token.
        Expected: 401 Unauthorized.
        """
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": "not-a-valid-jwt"},
        )
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_refresh_with_access_token(
        self, client: TestClient, test_user_in_db
    ) -> None:
        """Test refresh using an access token instead of a refresh token.

        Scenario: POST /api/auth/refresh with access_token.
        Expected: 401 Unauthorized (typ mismatch).
        """
        # 1. Login to get tokens
        login_res = client.post(
            "/api/auth/token",
            json={
                "email": test_user_in_db.email,
                "password": "password123",
            },
        )
        access_token = login_res.json()["access_token"]

        # 2. Try to refresh using access_token
        refresh_res = client.post(
            "/api/auth/refresh",
            json={"refresh_token": access_token},
        )
        assert refresh_res.status_code == 401
        assert "invalid" in refresh_res.json()["detail"].lower()
