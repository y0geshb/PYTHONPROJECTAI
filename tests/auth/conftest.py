"""Auth test fixtures and runtime guards."""

import json
import socket
from pathlib import Path
from urllib.parse import urlparse

import pytest

from config.http_client import APIClient
from tests.auth.serh_auth_api import SERHAuthAPI


@pytest.fixture(scope="session", autouse=True)
def ensure_auth_api_is_reachable(base_url):
    parsed = urlparse(base_url)
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    if not host:
        pytest.skip("SERH auth suite skipped: API_BASE_URL has no hostname")
    try:
        with socket.create_connection((host, port), timeout=2):
            pass
    except OSError as exc:
        pytest.skip(f"SERH auth suite skipped: cannot connect to {host}:{port} ({exc})")


@pytest.fixture(scope="session")
def serh_payloads() -> dict:
    payload_file = Path(__file__).resolve().parents[2] / "test_data" / "serh_auth_payloads.json"
    with payload_file.open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


@pytest.fixture(scope="session")
def serh_api(base_url):
    client = APIClient(base_url=base_url)
    return SERHAuthAPI(client=client)

