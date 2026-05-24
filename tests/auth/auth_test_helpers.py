"""Shared assertion utilities and constants for all SERH auth test modules.

Import these helpers directly in each test file to avoid code duplication.
"""

import os
from typing import Optional

# Status codes that represent expected negative/error responses
NEGATIVE_STATUSES = frozenset({400, 401, 403, 404, 405, 406, 409, 415, 422, 429})

# Endpoint path constants matching the Postman collection
ENDPOINTS = {
    "login": "/api/auth/login",
    "refresh_token": "/api/auth/refresh",
    "uae_pass_start": "/api/auth/uae-pass/start",
    "uae_pass_callback": "/api/auth/uae-pass/callback",
    "forgot_otp_initiate": "/api/auth/password/forgot-otp/initiate",
    "forgot_otp_verify": "/api/auth/password/forgot-otp/verify",
    "password_reset": "/api/auth/password/reset",
    "forgot_email": "/api/auth/password/forgot-email",
    "account_unlock": "/api/auth/account/unlock",
}


def live_positive_enabled() -> bool:
    """Return True when caller has set SERH_ENABLE_LIVE_POSITIVE=true/1/yes."""
    return os.getenv("SERH_ENABLE_LIVE_POSITIVE", "false").strip().lower() in {"1", "true", "yes"}


def response_json(response) -> Optional[dict]:
    """Return parsed JSON body or None on decode failure."""
    try:
        return response.json()
    except (ValueError, AttributeError):
        return None


def assert_non_server_error(response, context: str = "") -> None:
    """Assert that the response is not a 5xx server error."""
    prefix = f"[{context}] " if context else ""
    assert response.status_code < 500, (
        f"{prefix}Expected non-5xx status code but got {response.status_code}. "
        f"Body: {response.text}"
    )


def assert_negative_status(response, context: str = "") -> None:
    """Assert response has a controlled client-error status code (4xx)."""
    assert_non_server_error(response, context)
    prefix = f"[{context}] " if context else ""
    assert response.status_code in NEGATIVE_STATUSES, (
        f"{prefix}Expected one of {sorted(NEGATIVE_STATUSES)} but got "
        f"{response.status_code}. Body: {response.text}"
    )


def assert_has_common_field(response, context: str = "") -> None:
    """Assert that the JSON body contains at least one standard envelope field."""
    body = response_json(response)
    if body is None:
        return  # Non-JSON body – skip field check
    prefix = f"[{context}] " if context else ""
    assert isinstance(body, dict), (
        f"{prefix}Expected JSON object response but got {type(body)}. Body: {body}"
    )
    standard_keys = {"message", "status", "success", "errors", "data", "error"}
    assert any(k in body for k in standard_keys), (
        f"{prefix}Expected at least one of {standard_keys} in response body. Body: {body}"
    )

