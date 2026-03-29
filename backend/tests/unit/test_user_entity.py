from app.domain.entities import User


class TestUserEntity:
    """Test suite for User entity."""

    def test_user_creation(self) -> None:
        """Test creating a User entity."""
        user = User(
            id="user-1",
            email="test@example.com",
            full_name="Test User",
            hashed_password="hashed_password_value",
        )

        assert user.id == "user-1"
        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.hashed_password == "hashed_password_value"
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_equality(self) -> None:
        """Test that users are equal by id."""
        user1 = User(
            id="user-1",
            email="test1@example.com",
            full_name="User 1",
            hashed_password="hash1",
        )
        user2 = User(
            id="user-1",
            email="test2@example.com",
            full_name="User 2",
            hashed_password="hash2",
        )

        assert user1 == user2

    def test_user_inequality(self) -> None:
        """Test that users with different ids are not equal."""
        user1 = User(
            id="user-1",
            email="test1@example.com",
            full_name="User 1",
            hashed_password="hash1",
        )
        user2 = User(
            id="user-2",
            email="test1@example.com",
            full_name="User 1",
            hashed_password="hash1",
        )

        assert user1 != user2

    def test_user_hash(self) -> None:
        """Test that users can be hashed by id."""
        user = User(
            id="user-1",
            email="test@example.com",
            full_name="Test User",
            hashed_password="hash",
        )

        # Should not raise
        hash(user)

    def test_user_repr(self) -> None:
        """Test string representation of User."""
        user = User(
            id="user-1",
            email="test@example.com",
            full_name="Test User",
            hashed_password="hash",
        )

        repr_str = repr(user)
        assert "user-1" in repr_str
        assert "test@example.com" in repr_str
        assert "Test User" in repr_str
