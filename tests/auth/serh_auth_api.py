"""SERH Authentication API – endpoint wrapper (page-object layer).

Each method maps 1-to-1 with a /api/auth/* route from the Postman collection.
Tests call these methods instead of calling the HTTP client directly, keeping
request construction in one place.
"""

import json
from typing import Optional

import requests

from config.http_client import APIClient


class SERHAuthAPI:
    """Thin wrapper around all SERH /api/auth/* endpoints."""

    _BASE = "/api/auth"

    def __init__(self, client: APIClient):
        self.client = client

    # ------------------------------------------------------------------ #
    # Authentication                                                        #
    # ------------------------------------------------------------------ #

    def login(self, payload: Optional[dict] = None) -> requests.Response:
        """POST /api/auth/login"""
        return self.client.post(f"{self._BASE}/login", json=payload)

    def refresh_token(self, payload: Optional[dict] = None) -> requests.Response:
        """POST /api/auth/refresh"""
        return self.client.post(f"{self._BASE}/refresh", json=payload)

    def uae_pass_start(self) -> requests.Response:
        """GET /api/auth/uae-pass/start  — allow_redirects=False to capture 302."""
        return self.client.get(f"{self._BASE}/uae-pass/start", allow_redirects=False)

    def uae_pass_callback(self, payload: Optional[dict] = None) -> requests.Response:
        """POST /api/auth/uae-pass/callback"""
        return self.client.post(f"{self._BASE}/uae-pass/callback", json=payload)

    # ------------------------------------------------------------------ #
    # Password management                                                   #
    # ------------------------------------------------------------------ #

    def forgot_otp_initiate(self, payload: Optional[dict] = None) -> requests.Response:
        """POST /api/auth/password/forgot-otp/initiate"""
        return self.client.post(f"{self._BASE}/password/forgot-otp/initiate", json=payload)

    def forgot_otp_verify(self, payload: Optional[dict] = None) -> requests.Response:
        """POST /api/auth/password/forgot-otp/verify"""
        return self.client.post(f"{self._BASE}/password/forgot-otp/verify", json=payload)

    def password_reset(self, payload: Optional[dict] = None) -> requests.Response:
        """POST /api/auth/password/reset"""
        return self.client.post(f"{self._BASE}/password/reset", json=payload)

    def forgot_email(self, payload: Optional[dict] = None) -> requests.Response:
        """POST /api/auth/password/forgot-email"""
        return self.client.post(f"{self._BASE}/password/forgot-email", json=payload)

    # ------------------------------------------------------------------ #
    # Account management                                                    #
    # ------------------------------------------------------------------ #

    def account_unlock(self, payload: Optional[dict] = None) -> requests.Response:
        """POST /api/auth/account/unlock"""
        return self.client.post(f"{self._BASE}/account/unlock", json=payload)

    # ------------------------------------------------------------------ #
    # Generic helpers for header-manipulation tests                        #
    # ------------------------------------------------------------------ #

    def post_plain_text(self, path: str, payload: dict) -> requests.Response:
        """POST with Content-Type: text/plain – used by TC_*_invalid_content_type tests."""
        return self.client.post(
            path,
            data=json.dumps(payload),
            headers={"Content-Type": "text/plain", "Accept": "application/json"},
        )

    def get_on_post_endpoint(self, path: str) -> requests.Response:
        """Sends GET to a POST-only endpoint – used by TC_*_wrong_http_method tests."""
        return self.client.get(path)

