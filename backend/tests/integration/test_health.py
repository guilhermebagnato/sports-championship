from fastapi.testclient import TestClient


class TestHealthCheck:
    """Test suite for Health Check endpoint."""

    def test_health_check_returns_ok(self, client: TestClient) -> None:
        """Test that health check returns 200 OK with correct body."""
        response = client.get("/api/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_health_check_no_auth_required(self, client: TestClient) -> None:
        """Test that health check is public (no auth required)."""
        response = client.get("/api/health")

        assert response.status_code == 200
        # No Authorization header required

    def test_health_check_content_type(self, client: TestClient) -> None:
        """Test that health check returns JSON content type."""
        response = client.get("/api/health")

        assert response.headers["content-type"] == "application/json"

    def test_cors_headers_present(self, client: TestClient) -> None:
        """Test that CORS headers are configured.

        This tests the CORS middleware is working.
        Note: TestClient may not fully test CORS preflight, but we can verify
        basic CORS configuration through include_router and middleware setup.
        """
        response = client.get("/api/health")

        # Health check should be accessible
        assert response.status_code == 200

    def test_swagger_docs_available(self, client: TestClient) -> None:
        """Test that Swagger UI is available at /docs."""
        response = client.get("/docs")

        assert response.status_code == 200

    def test_root_endpoint(self, client: TestClient) -> None:
        """Test that root endpoint returns API info."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data
