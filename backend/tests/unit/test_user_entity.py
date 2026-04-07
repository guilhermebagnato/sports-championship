from datetime import datetime

from app.domain.entities import User


class TestUserEntity:
    """Unit tests for User domain entity."""

    def test_user_initialization(self) -> None:
        """Test user creation with default and explicit values."""
        user = User(
            id="user-1",
            email="test@example.com",
            full_name="Test User",
            hashed_password="hash",
        )
        assert user.id == "user-1"
        assert user.is_active is True
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_user_equality(self) -> None:
        """Test user equality comparison."""
        user1 = User("1", "a@a.com", "A", "h")
        user2 = User("1", "b@b.com", "B", "h")
        user3 = User("2", "a@a.com", "A", "h")

        assert user1 == user2
        assert user1 != user3
        assert user1 != "not a user"  # Tests the NotImplemented case

    def test_user_hash(self) -> None:
        """Test user hashing."""
        user1 = User("1", "a@a.com", "A", "h")
        assert hash(user1) == hash("1")

    def test_user_repr(self) -> None:
        """Test user string representation."""
        user = User("1", "test@test.com", "Test", "h")
        representation = repr(user)
        assert "User(id='1'" in representation
        assert "email='test@test.com'" in representation
