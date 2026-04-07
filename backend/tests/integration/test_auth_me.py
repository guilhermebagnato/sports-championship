import pytest
from fastapi.testclient import TestClient


class TestAuthMe:
    """Test suite for GET /api/auth/me endpoint."""

    @pytest.mark.asyncio
    async def test_get_me_success(self, client: TestClient, test_user_in_db) -> None:
        """Test successful retrieval of current user profile.

        Scenario: POST /api/auth/token then GET /api/auth/me with access_token.
        Expected: 200 OK, returns user profile (email, full_name, etc).
        """
        # 1. Login to get token
        login_res = client.post(
            "/api/auth/token",
            json={
                "email": test_user_in_db.email,
                "password": "password123",
            },
        )
        assert login_res.status_code == 200
        access_token = login_res.json()["access_token"]

        # 2. Get profile
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_in_db.email
        assert data["full_name"] == test_user_in_db.full_name
        assert data["id"] == test_user_in_db.id
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_get_me_unauthorized(self, client: TestClient) -> None:
        """Test GET /api/auth/me without token.

        Scenario: GET /api/auth/me without Authorization header.
        Expected: 401 Unauthorized.
        """
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_me_invalid_token(self, client: TestClient) -> None:
        """Test GET /api/auth/me with invalid token.

        Scenario: GET /api/auth/me with garbage token.
        Expected: 401 Unauthorized.
        """
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid-token"},
        )
        assert response.status_code == 401
