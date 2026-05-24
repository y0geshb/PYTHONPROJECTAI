"""
Smoke tests to validate framework setup and core API behavior.

Run instruction:
    pytest tests/smoke/ -v -m smoke
"""

import pytest

from config.http_client import APIClient


class TestFrameworkHealth:
    """Framework health smoke suite."""

    @pytest.mark.smoke
    def test_api_is_reachable(self, base_url):
        """Verify health endpoint is reachable and responds within 5000ms."""
        client = APIClient(base_url=base_url)
        response = client.get("/api/health", timeout=10)

        assert response.status_code == 200, (
            f"Expected 200 but got {response.status_code}. Body: {response.text}"
        )
        elapsed_ms = int(response.elapsed.total_seconds() * 1000)
        assert elapsed_ms < 5000, (
            f"Expected response time < 5000ms but got {elapsed_ms}ms."
        )

    @pytest.mark.smoke
    def test_login_returns_token(self, auth_token):
        """Verify auth_token fixture returns a non-empty token string."""
        assert isinstance(auth_token, str), (
            f"Expected token type str but got {type(auth_token)}"
        )
        assert auth_token.strip() != "", "Expected non-empty token but got empty string"
        assert len(auth_token) > 10, f"Expected token length > 10 but got {len(auth_token)}"

    @pytest.mark.smoke
    def test_authenticated_endpoint_works(self, base_url, auth_headers):
        """Verify protected endpoint returns 200 with valid bearer token."""
        client = APIClient(base_url=base_url, headers=auth_headers)
        response = client.get("/api/v1/users", timeout=10)

        assert response.status_code == 200, (
            f"Expected 200 but got {response.status_code}. Body: {response.text}"
        )

    @pytest.mark.smoke
    def test_unauthenticated_request_is_rejected(self, base_url):
        """Verify protected endpoint returns 401 when no auth header is provided."""
        client = APIClient(base_url=base_url)
        response = client.get("/api/v1/users", timeout=10)

        assert response.status_code == 401, (
            f"Expected 401 but got {response.status_code}. Body: {response.text}"
        )

    @pytest.mark.smoke
    def test_invalid_token_is_rejected(self, base_url):
        """Verify protected endpoint returns 401 for a clearly invalid bearer token."""
        invalid_headers = {"Authorization": "Bearer INVALID_TOKEN_12345"}
        client = APIClient(base_url=base_url, headers=invalid_headers)
        response = client.get("/api/v1/users", timeout=10)

        assert response.status_code == 401, (
            f"Expected 401 but got {response.status_code}. Body: {response.text}"
        )
