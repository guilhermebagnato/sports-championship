from fastapi.testclient import TestClient

from app.main import app


def test_root_endpoint() -> None:
    """Test the API root endpoint."""
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Sports Championship API"
        assert "version" in data
        assert "docs" in data


def test_startup_event() -> None:
    """Test using context manager to trigger startup/shutdown events."""
    with TestClient(app) as client:
        # Just being in this block triggers the on_startup event
        response = client.get("/api/health")
        assert response.status_code == 200
