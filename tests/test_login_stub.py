from __future__ import annotations

import requests

BASE_URL = "http://127.0.0.1:4010"
LOGIN_URL = f"{BASE_URL}/api/auth/login"


def test_login_stub_success_response_structure() -> None:
    response = requests.post(
        LOGIN_URL,
        json={
            "email": "kajal.gupta@kellton.com",
            "password": "Amazing@432!",
            "captchaToken": "captcha-ok"
        },
        timeout=5,
    )

    assert response.status_code == 200

    body = response.json()
    assert body["success"] is True
    assert "message" in body and isinstance(body["message"], dict)
    assert "en" in body["message"] and isinstance(body["message"]["en"], str)
    assert "ar" in body["message"] and isinstance(body["message"]["ar"], str)

    assert "data" in body and isinstance(body["data"], dict)
    assert body["data"].get("mfaRequired") is True

    mfa_session_token = body["data"].get("mfaSessionToken")
    assert isinstance(mfa_session_token, str)
    assert len(mfa_session_token.split(".")) == 3

    assert isinstance(body.get("traceId"), str)
    assert isinstance(body.get("requestId"), str)


def test_login_stub_missing_required_fields_returns_400() -> None:
    response = requests.post(
        LOGIN_URL,
        json={"email": "kajal.gupta@kellton.com"},
        timeout=5,
    )

    assert response.status_code == 400

    body = response.json()
    assert body["success"] is False
    assert "message" in body and isinstance(body["message"], dict)
    assert "error" in body and isinstance(body["error"], dict)
    assert body["error"].get("code") == "AUTH_400_VALIDATION_ERROR"
    assert "fields" in body["error"] and body["error"]["fields"].get("password") == "required"
    assert isinstance(body.get("traceId"), str)
    assert isinstance(body.get("requestId"), str)
