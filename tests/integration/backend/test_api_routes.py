"""Integration tests for API routes."""

import pytest
from fastapi.testclient import TestClient

from src.backend.main import app


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client: TestClient) -> None:
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "tradingbotagent-api"


# TODO: Add more integration tests for mandate and agent routes
# Note: These will require proper database setup and mocking
