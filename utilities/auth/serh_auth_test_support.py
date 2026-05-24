"""Shared helpers for SERH auth endpoint tests."""

import os

NEGATIVE_STATUSES = {400, 401, 403, 404, 405, 406, 409, 415, 422, 429}

ENV_OVERRIDE_MAP = {
    "login": {
        "email": "API_USER_EMAIL",
        "password": "API_USER_PASSWORD",
        "captchaToken": "SERH_CAPTCHA_TOKEN",
    },
    "refresh_token": {"refreshToken": "SERH_REFRESH_TOKEN"},
    "uae_pass_callback": {
        "state": "SERH_UAEPASS_STATE",
        "code": "SERH_UAEPASS_CODE",
        "emiratesId": "SERH_UAEPASS_EMIRATES_ID",
    },
    "forgot_otp_initiate": {
        "email": "SERH_FORGOT_OTP_EMAIL",
        "mobile": "SERH_FORGOT_OTP_MOBILE",
    },
    "forgot_otp_verify": {
        "otp": "SERH_FORGOT_OTP_CODE",
        "sessionToken": "SERH_FORGOT_OTP_SESSION_TOKEN",
    },
    "password_reset": {
        "resetToken": "SERH_RESET_TOKEN",
        "newPassword": "SERH_NEW_PASSWORD",
    },
    "forgot_email": {"email": "SERH_FORGOT_EMAIL"},
    "account_unlock": {
        "email": "SERH_UNLOCK_EMAIL",
        "unlockToken": "SERH_UNLOCK_TOKEN",
    },
}


def response_json_or_none(response):
    try:
        return response.json()
    except ValueError:
        return None


def assert_non_server_error(response, context: str) -> None:
    assert response.status_code < 500, (
        f"{context}: expected non-5xx response, got {response.status_code}. Body: {response.text}"
    )


def assert_negative_status(response, context: str) -> None:
    assert_non_server_error(response, context)
    assert response.status_code in NEGATIVE_STATUSES, (
        f"{context}: expected one of {sorted(NEGATIVE_STATUSES)} but got {response.status_code}. "
        f"Body: {response.text}"
    )


def assert_common_response_fields(response, context: str) -> None:
    body = response_json_or_none(response)
    if body is None:
        return
    assert isinstance(body, dict), f"{context}: expected JSON object response but got {type(body)}"
    has_common_field = any(k in body for k in ("message", "status", "success", "errors", "data"))
    assert has_common_field, (
        f"{context}: expected at least one common response field "
        f"(message/status/success/errors/data). Body: {body}"
    )


def resolve_positive_payload(endpoint_key: str, raw_payload: dict) -> dict:
    payload = dict(raw_payload)
    for field, env_key in ENV_OVERRIDE_MAP.get(endpoint_key, {}).items():
        env_value = os.getenv(env_key)
        if env_value:
            payload[field] = env_value
    return payload


def has_placeholder_values(payload: dict) -> bool:
    for value in payload.values():
        if isinstance(value, str) and value.startswith("replace-with-"):
            return True
    return False


def live_positive_enabled() -> bool:
    return os.getenv("SERH_ENABLE_LIVE_POSITIVE", "false").strip().lower() in {"1", "true", "yes"}


