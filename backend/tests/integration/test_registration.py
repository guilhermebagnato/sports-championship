from fastapi.testclient import TestClient


class TestUserRegistration:
    """Test suite for User Registration endpoint."""

    def test_register_user_success(self, client: TestClient) -> None:
        """Test successful user registration.

        Scenario: POST /api/auth/register with valid email, password, full_name
        Expected: 201 Created, returns UserPublic with id
        """
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "secure_password_123",
                "full_name": "New User",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["email"] == "newuser@example.com"
        assert data["full_name"] == "New User"
        assert "hashed_password" not in data  # Never return hashed password
        assert "created_at" in data

    def test_register_user_invalid_email(self, client: TestClient) -> None:
        """Test registration with invalid email format.

        Scenario: POST /api/auth/register with malformed email
        Expected: 422 Unprocessable Entity
        """
        response = client.post(
            "/api/auth/register",
            json={
                "email": "invalid-email",
                "password": "secure_password_123",
                "full_name": "New User",
            },
        )

        assert response.status_code == 422  # Validation error from Pydantic

    def test_register_user_duplicate_email(
        self, client: TestClient, test_user_in_db
    ) -> None:
        """Test registration with existing email.

        Scenario: POST /api/auth/register with email already in database
        Expected: 400 Bad Request
        """
        response = client.post(
            "/api/auth/register",
            json={
                "email": test_user_in_db.email,  # Email already exists
                "password": "secure_password_123",
                "full_name": "Another User",
            },
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_register_user_missing_fields(self, client: TestClient) -> None:
        """Test registration with missing required fields.

        Scenario: POST /api/auth/register without email
        Expected: 422 Unprocessable Entity
        """
        response = client.post(
            "/api/auth/register",
            json={
                "password": "secure_password_123",
                "full_name": "New User",
                # Missing 'email'
            },
        )

        assert response.status_code == 422

    def test_register_user_empty_password(self, client: TestClient) -> None:
        """Test registration with empty password.

        Scenario: POST /api/auth/register with empty password string
        Expected: 422 Unprocessable Entity
        """
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "",  # Empty password
                "full_name": "New User",
            },
        )

        assert response.status_code == 422

    def test_register_returns_no_password(self, client: TestClient) -> None:
        """Test that response never includes password or hashed_password.

        Scenario: POST /api/auth/register successful
        Expected: Response schema excludes password fields
        """
        response = client.post(
            "/api/auth/register",
            json={
                "email": "secure@example.com",
                "password": "password123",
                "full_name": "Test User",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert "password" not in data
        assert "hashed_password" not in data
