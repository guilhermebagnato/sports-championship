import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.adapters.repositories import UserRepository
from app.domain.entities import User as UserEntity


class TestAuthDeactivated:
    """Integration tests for deactivated user scenarios."""

    @pytest.mark.asyncio
    async def test_login_deactivated_user(
        self, client: TestClient, session: Session, test_user_in_db: UserEntity
    ) -> None:
        """Test login with a deactivated user."""
        # 1. Deactivate user directly in DB
        repository = UserRepository(session)
        test_user_in_db.is_active = False
        await repository.update(test_user_in_db)

        # 2. Try login
        response = client.post(
            "/api/auth/token",
            json={
                "email": test_user_in_db.email,
                "password": "password123",
            },
        )
        assert response.status_code == 401
        assert "disabled" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_refresh_deactivated_user(
        self, client: TestClient, session: Session, test_user_in_db: UserEntity
    ) -> None:
        """Test token refresh with a deactivated user."""
        # 1. Login normally first to get tokens
        login_res = client.post(
            "/api/auth/token",
            json={
                "email": test_user_in_db.email,
                "password": "password123",
            },
        )
        refresh_token = login_res.json()["refresh_token"]

        # 2. Deactivate user in DB
        repository = UserRepository(session)
        test_user_in_db.is_active = False
        await repository.update(test_user_in_db)

        # 3. Try refresh
        response = client.post(
            "/api/auth/refresh", json={"refresh_token": refresh_token}
        )
        assert response.status_code == 401
        assert "not found or disabled" in response.json()["detail"].lower()
