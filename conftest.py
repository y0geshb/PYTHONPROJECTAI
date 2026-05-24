"""
conftest.py
Shared pytest fixtures for the entire test suite.
"""

import logging
import os

import pytest

from config.environments import ensure_environment_loaded, get_auth_headers, get_base_url
from config.http_client import APIClient

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment variables for the active framework mode once per session."""
    mode = ensure_environment_loaded()
    logger.info("Environment variables loaded for API mode: %s", mode)


@pytest.fixture(scope="session")
def base_url(load_env):
    """Return API_BASE_URL from environment variables."""
    url = get_base_url()
    if not url:
        raise ValueError("API_BASE_URL is not set. Please add it to your .env file.")
    return url.rstrip("/")


@pytest.fixture(scope="session")
def auth_token(base_url):
    """Login once and return a JWT token from response.json()[\"token\"]."""
    login_endpoint = os.getenv("API_LOGIN_ENDPOINT")
    if not login_endpoint:
        raise ValueError("API_LOGIN_ENDPOINT is not set. Please add it to your .env file.")

    client = APIClient(base_url=base_url)
    login_payload = {
        "email": os.getenv("API_USER_EMAIL"),
        "password": os.getenv("API_USER_PASSWORD"),
        "captchaToken": os.getenv("API_CAPTCHA_TOKEN", "captcha-ok"),
    }

    response = client.post(login_endpoint, json=login_payload, timeout=10)
    assert response.status_code == 200, (
        f"Login failed. Expected 200 but got {response.status_code}. Body: {response.text}"
    )

    token = response.json()["token"]
    return token


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    """Return bearer auth headers for protected endpoints."""
    return get_auth_headers(auth_token)


@pytest.fixture(scope="session")
def api_client(base_url, auth_headers):
    """Authenticated API client."""
    return APIClient(base_url=base_url, headers=auth_headers)


@pytest.fixture(scope="session")
def unauth_client(base_url):
    """Unauthenticated API client."""
    return APIClient(base_url=base_url)
