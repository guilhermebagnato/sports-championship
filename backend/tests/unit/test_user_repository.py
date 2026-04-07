import pytest
from sqlmodel import Session

from app.adapters.repositories import UserRepository
from app.domain.entities import User as UserEntity


@pytest.mark.asyncio
class TestUserRepository:
    """Unit tests for UserRepository."""

    async def test_get_by_id_not_found(self, session: Session) -> None:
        """Test get_by_id when user does not exist."""
        repository = UserRepository(session)
        user = await repository.get_by_id("non-existent-id")
        assert user is None

    async def test_update_user_success(
        self, session: Session, test_user_in_db: UserEntity
    ) -> None:
        """Test updating an existing user."""
        repository = UserRepository(session)

        # Modify fields
        test_user_in_db.full_name = "Updated Name"
        test_user_in_db.is_active = False

        updated_user = await repository.update(test_user_in_db)

        assert updated_user.full_name == "Updated Name"
        assert updated_user.is_active is False

        # Verify in DB
        db_user = await repository.get_by_id(test_user_in_db.id)
        assert db_user.full_name == "Updated Name"

    async def test_update_user_not_found(self, session: Session) -> None:
        """Test updating a non-existent user."""
        repository = UserRepository(session)
        user = UserEntity("none", "none@none.com", "None", "hash")

        with pytest.raises(ValueError, match="not found"):
            await repository.update(user)
