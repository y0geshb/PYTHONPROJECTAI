"""Auth endpoint handlers for the local mock server."""

from __future__ import annotations

import base64
import json
import os
import re
import time
from typing import Any

from config.environments import ensure_environment_loaded
from handlers.stub_loader import load_stub_response

RouteResult = tuple[int, dict[str, str], dict[str, Any]]

_AUTH_BASE = "/api/auth"
_JSON_HEADERS = {"Content-Type": "application/json; charset=utf-8"}
_REDIRECT_LOCATION = "https://mock-uae-pass.local/authorize"
_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_PATTERN = re.compile(r"^\+?[0-9]{8,15}$")
_UUID_PATTERN = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)
_JWT_PATTERN = re.compile(r"^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$")
_EMIRATES_ID_PATTERN = re.compile(r"^784\d{12}$")
_KNOWN_EMAIL = "kajal.gupta@kellton.com"
_KNOWN_MOBILE = "+971500000000"
_KNOWN_UNLOCK_TOKEN = "27284cab-fa56-464d-9c62-a0dc66f0aed3"
_KNOWN_OTP = "294792"
_KNOWN_SESSION_TOKEN = "1b43faa3-45c8-4d1b-82aa-e732bdda1a0a"
_KNOWN_UAE_PASS_STATE = "612d972e-e0bb-4228-83f9-d76e055a2539"
_EXPIRED_TOKEN_PREFIX = "aaaaaaaa-bbbb-cccc-dddd-"
_POST_SPECS = {
    f"{_AUTH_BASE}/login": {
        "required_fields": {"email", "password", "captchaToken"},
        "response_file": "login-success",
    },
    f"{_AUTH_BASE}/refresh": {
        "required_fields": {"refreshToken"},
        "response_file": "refresh-success",
    },
    f"{_AUTH_BASE}/uae-pass/callback": {
        "required_fields": {"state", "code", "emiratesId"},
        "response_file": "uae-pass-callback-success",
    },
    f"{_AUTH_BASE}/password/forgot-otp/initiate": {
        "required_fields": {"email", "mobile"},
        "response_file": "forgot-otp-initiate-success",
    },
    f"{_AUTH_BASE}/password/forgot-otp/verify": {
        "required_fields": {"otp", "sessionToken"},
        "response_file": "forgot-otp-verify-success",
    },
    f"{_AUTH_BASE}/password/reset": {
        "required_fields": {"resetToken", "newPassword"},
        "response_file": "password-reset-success",
    },
    f"{_AUTH_BASE}/password/forgot-email": {
        "required_fields": {"email"},
        "response_file": "forgot-email-success",
    },
    f"{_AUTH_BASE}/account/unlock": {
        "required_fields": {"email", "unlockToken"},
        "response_file": "account-unlock-success",
    },
}


def handle_auth_request(method: str, path: str, headers: dict[str, str], body_text: str) -> RouteResult | None:
    """Return a mock response for supported auth routes or None if unmatched."""
    if path == f"{_AUTH_BASE}/uae-pass/start":
        if method != "GET":
            return _method_not_allowed(["GET"])
        return 302, {**_JSON_HEADERS, "Location": _REDIRECT_LOCATION}, {
            "message": "Redirecting to UAE Pass",
            "redirectUrl": _REDIRECT_LOCATION,
        }

    spec = _POST_SPECS.get(path)
    if spec is None:
        return None

    if method != "POST":
        return _method_not_allowed(["POST"])

    header_error = _validate_request_headers(headers)
    if header_error is not None:
        return header_error

    payload, parse_error = _parse_json_body(body_text)
    if parse_error is not None:
        return parse_error

    validation_error = _validate_payload(payload, spec["required_fields"])
    if validation_error is not None:
        return validation_error

    request_error = _validate_auth_request(path, payload)
    if request_error is not None:
        return request_error

    if path == f"{_AUTH_BASE}/login":
        credentials_error = _validate_login_credentials(payload)
        if credentials_error is not None:
            return credentials_error

    if path == f"{_AUTH_BASE}/refresh" and _looks_invalid_secret(payload.get("refreshToken")):
        return _error_response(401, "Invalid refresh token", error="AUTH_INVALID_TOKEN")

    if path == f"{_AUTH_BASE}/password/reset" and _looks_invalid_secret(payload.get("resetToken")):
        return _error_response(400, "Reset token is invalid", error="RESET_TOKEN_INVALID")

    if path == f"{_AUTH_BASE}/account/unlock" and _looks_invalid_secret(payload.get("unlockToken")):
        return _error_response(400, "Unlock token is invalid", error="UNLOCK_TOKEN_INVALID")

    response_body = load_stub_response("auth", spec["response_file"])
    return 200, dict(_JSON_HEADERS), response_body


def _validate_request_headers(headers: dict[str, str]) -> RouteResult | None:
    accept_header = headers.get("Accept", "application/json")
    if "application/json" not in accept_header and "*/*" not in accept_header:
        return _error_response(406, "Accept header must allow application/json", error="NOT_ACCEPTABLE")

    content_type = headers.get("Content-Type", "application/json")
    if "application/json" not in content_type:
        return _error_response(415, "Content-Type must be application/json", error="UNSUPPORTED_MEDIA_TYPE")

    return None


def _parse_json_body(body_text: str) -> tuple[dict[str, Any], RouteResult | None]:
    if not body_text.strip():
        return {}, _error_response(400, "Request body must not be empty", error="EMPTY_BODY")

    try:
        payload = json.loads(body_text)
    except json.JSONDecodeError:
        return {}, _error_response(400, "Malformed JSON body", error="MALFORMED_JSON")

    if not isinstance(payload, dict):
        return {}, _error_response(400, "JSON body must be an object", error="INVALID_BODY")

    return payload, None


def _validate_payload(payload: dict[str, Any], required_fields: set[str]) -> RouteResult | None:
    missing_fields = sorted(
        field
        for field in required_fields
        if field not in payload or payload[field] is None or str(payload[field]).strip() == ""
    )
    if missing_fields:
        return _error_response(
            400,
            "Request validation failed",
            error="VALIDATION_ERROR",
            errors={"missingFields": missing_fields},
        )

    unexpected_fields = sorted(field for field in payload if field not in required_fields)
    if unexpected_fields:
        return _error_response(
            400,
            "Request contains unexpected fields",
            error="UNEXPECTED_FIELDS",
            errors={"unexpectedFields": unexpected_fields},
        )

    return None


def _validate_login_credentials(payload: dict[str, Any]) -> RouteResult | None:
    ensure_environment_loaded()
    expected_email = os.getenv("API_USER_EMAIL", "mockuser@example.com")
    expected_password = os.getenv("API_USER_PASSWORD", "mock-password")

    if payload["email"] != expected_email or payload["password"] != expected_password:
        return _error_response(401, "Invalid credentials", error="AUTH_INVALID_CREDENTIALS")

    return None


def _validate_auth_request(path: str, payload: dict[str, Any]) -> RouteResult | None:
    if path == f"{_AUTH_BASE}/login":
        if not _is_valid_email(payload["email"]):
            return _error_response(401, "Invalid credentials", error="AUTH_INVALID_CREDENTIALS")
        return None

    if path == f"{_AUTH_BASE}/refresh":
        token = payload["refreshToken"]
        if not _is_jwt(token):
            return _error_response(401, "Invalid refresh token", error="AUTH_INVALID_TOKEN")
        if _is_expired_token(token):
            return _error_response(401, "Refresh token expired", error="AUTH_TOKEN_EXPIRED")
        return None

    if path == f"{_AUTH_BASE}/uae-pass/callback":
        if not _is_valid_emirates_id(payload["emiratesId"]):
            return _error_response(400, "Emirates ID format is invalid", error="VALIDATION_ERROR")
        if payload["state"] != _KNOWN_UAE_PASS_STATE:
            return _error_response(401, "State token is invalid", error="AUTH_INVALID_STATE")
        return None

    if path == f"{_AUTH_BASE}/password/forgot-email":
        if not _is_valid_email(payload["email"]):
            return _error_response(400, "Email address is invalid", error="VALIDATION_ERROR")
        return None

    if path == f"{_AUTH_BASE}/password/forgot-otp/initiate":
        if not _is_valid_email(payload["email"]):
            return _error_response(400, "Email address is invalid", error="VALIDATION_ERROR")
        if not _is_valid_mobile(payload["mobile"]):
            return _error_response(400, "Mobile number is invalid", error="VALIDATION_ERROR")
        return None

    if path == f"{_AUTH_BASE}/password/forgot-otp/verify":
        if payload["sessionToken"] != _KNOWN_SESSION_TOKEN:
            return _error_response(401, "Session token is invalid", error="AUTH_INVALID_TOKEN")
        if payload["otp"] != _KNOWN_OTP:
            return _error_response(401, "OTP is invalid or expired", error="AUTH_INVALID_OTP")
        return None

    if path == f"{_AUTH_BASE}/password/reset":
        password = str(payload["newPassword"])
        if len(password) < 8:
            return _error_response(400, "Password does not meet policy requirements", error="WEAK_PASSWORD")
        if payload["resetToken"] != _KNOWN_SESSION_TOKEN.replace("1b43faa3", "00000000"):
            if _looks_invalid_secret(payload["resetToken"]) or _is_expired_token(payload["resetToken"]):
                return _error_response(401, "Reset token is invalid or expired", error="RESET_TOKEN_INVALID")
            return _error_response(401, "Reset token is invalid or expired", error="RESET_TOKEN_INVALID")
        return None

    if path == f"{_AUTH_BASE}/account/unlock":
        email = str(payload["email"])
        token = str(payload["unlockToken"])
        if not _is_valid_email(email):
            return _error_response(400, "Email address is invalid", error="VALIDATION_ERROR")
        if email != _KNOWN_EMAIL:
            return _error_response(404, "Account unlock request is invalid", error="ACCOUNT_NOT_FOUND")
        if token == _KNOWN_UNLOCK_TOKEN:
            return _error_response(409, "Account is already active", error="ACCOUNT_ALREADY_ACTIVE")
        if token != _KNOWN_UNLOCK_TOKEN:
            if _looks_invalid_secret(token) or _is_expired_token(token) or _is_uuid(token):
                return _error_response(401, "Unlock token is invalid or expired", error="UNLOCK_TOKEN_INVALID")
            return _error_response(401, "Unlock token is invalid or expired", error="UNLOCK_TOKEN_INVALID")
        return None

    return None


def _looks_invalid_secret(value: Any) -> bool:
    if not isinstance(value, str):
        return True

    normalized = value.strip().lower()
    return not normalized or normalized.startswith("replace-with-") or normalized.startswith("invalid")


def _is_valid_email(value: Any) -> bool:
    return isinstance(value, str) and bool(_EMAIL_PATTERN.match(value.strip()))


def _is_valid_mobile(value: Any) -> bool:
    return isinstance(value, str) and bool(_PHONE_PATTERN.match(value.strip()))


def _is_uuid(value: Any) -> bool:
    return isinstance(value, str) and bool(_UUID_PATTERN.match(value.strip()))


def _is_jwt(value: Any) -> bool:
    return isinstance(value, str) and bool(_JWT_PATTERN.match(value.strip()))


def _is_valid_emirates_id(value: Any) -> bool:
    return isinstance(value, str) and bool(_EMIRATES_ID_PATTERN.match(value.strip()))


def _is_expired_token(value: Any) -> bool:
    if not isinstance(value, str):
        return False

    normalized = value.strip()
    if normalized.lower().startswith(_EXPIRED_TOKEN_PREFIX):
        return True

    if not _is_jwt(normalized):
        return False

    try:
        payload_segment = normalized.split(".")[1]
        padded_segment = payload_segment + "=" * (-len(payload_segment) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded_segment.encode("ascii")))
    except (OSError, ValueError, json.JSONDecodeError):
        return False

    exp = payload.get("exp")
    return isinstance(exp, (int, float)) and exp < time.time()


def _method_not_allowed(allowed_methods: list[str]) -> RouteResult:
    return 405, {**_JSON_HEADERS, "Allow": ", ".join(allowed_methods)}, {
        "message": "Method not allowed",
        "error": "METHOD_NOT_ALLOWED",
        "allowedMethods": allowed_methods,
    }


def _error_response(
    status_code: int,
    message: str,
    *,
    error: str,
    errors: dict[str, Any] | None = None,
) -> RouteResult:
    body: dict[str, Any] = {"message": message, "error": error, "success": False}
    if errors:
        body["errors"] = errors
    return status_code, dict(_JSON_HEADERS), body