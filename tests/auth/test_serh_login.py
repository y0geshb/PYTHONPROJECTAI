"""SERH Auth – Login endpoint tests.

CSV Reference: TC_LOGIN_001 – TC_LOGIN_014
Endpoint     : POST /api/auth/login
"""

import os

import pytest

from tests.auth.auth_test_helpers import (
    ENDPOINTS,
    assert_has_common_field,
    assert_negative_status,
    assert_non_server_error,
    live_positive_enabled,
    response_json,
)

LOGIN_PATH = ENDPOINTS["login"]


class TestSERHLogin:

    # ------------------------------------------------------------------ #
    # TC_LOGIN_001 – Valid login (happy path)                              #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.positive
    def test_TC_LOGIN_001_valid_credentials(self, serh_api, serh_payloads):
        """TC_LOGIN_001: POST /api/auth/login with valid email, password, captchaToken.

        Precondition : SERH_ENABLE_LIVE_POSITIVE=true and environment variables
                       API_USER_EMAIL / API_USER_PASSWORD / SERH_CAPTCHA_TOKEN set.
        Expected     : 200 with accessToken + refreshToken in body.
        """
        if not live_positive_enabled():
            pytest.skip("Set SERH_ENABLE_LIVE_POSITIVE=true to run live positive login test")

        payload = dict(serh_payloads["login"])
        for field, env_key in {
            "email": "API_USER_EMAIL",
            "password": "API_USER_PASSWORD",
            "captchaToken": "SERH_CAPTCHA_TOKEN",
        }.items():
            env_val = os.getenv(env_key)
            if env_val:
                payload[field] = env_val

        # Act
        response = serh_api.login(payload)

        # Assert
        assert response.status_code == 200, (
            f"TC_LOGIN_001: Expected 200 but got {response.status_code}. Body: {response.text}"
        )
        body = response_json(response)
        assert body is not None, "TC_LOGIN_001: Expected JSON body"
        token_keys = {"token", "accessToken", "access_token"}
        assert any(k in body or k in body.get("data", {}) for k in token_keys), (
            f"TC_LOGIN_001: Expected token field in response. Body: {body}"
        )

    # ------------------------------------------------------------------ #
    # TC_LOGIN_002 – Invalid email format                                  #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_LOGIN_002_invalid_email_format(self, serh_api):
        """TC_LOGIN_002: Malformed email address (not-an-email) → 400."""
        payload = {
            "email": "not-an-email",
            "password": "Password@1234",
            "captchaToken": "captcha-ok",
        }
        response = serh_api.login(payload)

        assert_negative_status(response, "TC_LOGIN_002")
        assert_has_common_field(response, "TC_LOGIN_002")

    # ------------------------------------------------------------------ #
    # TC_LOGIN_003 – Wrong password                                        #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_LOGIN_003_wrong_password(self, serh_api, serh_payloads):
        """TC_LOGIN_003: Correct email + wrong password → 401."""
        payload = dict(serh_payloads["login"])
        payload["password"] = "WrongPass@999"

        response = serh_api.login(payload)

        assert response.status_code == 401, (
            f"TC_LOGIN_003: Expected 401 but got {response.status_code}. Body: {response.text}"
        )
        body = response_json(response)
        # Server must NOT expose which field is wrong (security)
        if body:
            text_lower = str(body).lower()
            assert "password" not in text_lower or "invalid" in text_lower, (
                "TC_LOGIN_003: Error message should not explicitly reveal the wrong field"
            )

    # ------------------------------------------------------------------ #
    # TC_LOGIN_004 – Missing email field                                   #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_LOGIN_004_missing_email(self, serh_api):
        """TC_LOGIN_004: Payload without email → 400."""
        payload = {"password": "Password@1234", "captchaToken": "captcha-ok"}
        response = serh_api.login(payload)

        assert_negative_status(response, "TC_LOGIN_004")
        assert_has_common_field(response, "TC_LOGIN_004")

    # ------------------------------------------------------------------ #
    # TC_LOGIN_005 – Missing password field                                #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_LOGIN_005_missing_password(self, serh_api):
        """TC_LOGIN_005: Payload without password → 400."""
        payload = {"email": "kajal.gupta@kellton.com", "captchaToken": "captcha-ok"}
        response = serh_api.login(payload)

        assert_negative_status(response, "TC_LOGIN_005")
        assert_has_common_field(response, "TC_LOGIN_005")

    # ------------------------------------------------------------------ #
    # TC_LOGIN_006 – Missing captchaToken field                            #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_LOGIN_006_missing_captcha_token(self, serh_api):
        """TC_LOGIN_006: Payload without captchaToken → 400."""
        payload = {"email": "kajal.gupta@kellton.com", "password": "Password@1234"}
        response = serh_api.login(payload)

        assert_negative_status(response, "TC_LOGIN_006")
        assert_has_common_field(response, "TC_LOGIN_006")

    # ------------------------------------------------------------------ #
    # TC_LOGIN_007 – Empty payload {}                                      #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_LOGIN_007_empty_payload(self, serh_api):
        """TC_LOGIN_007: Empty JSON body → 400 with all required-field errors."""
        response = serh_api.login({})

        assert_negative_status(response, "TC_LOGIN_007")
        assert_has_common_field(response, "TC_LOGIN_007")

    # ------------------------------------------------------------------ #
    # TC_LOGIN_008 – Null email                                            #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_LOGIN_008_null_email(self, serh_api):
        """TC_LOGIN_008: email set to null → 400."""
        payload = {"email": None, "password": "Password@1234", "captchaToken": "captcha-ok"}
        response = serh_api.login(payload)

        assert_negative_status(response, "TC_LOGIN_008")
        assert_has_common_field(response, "TC_LOGIN_008")

    # ------------------------------------------------------------------ #
    # TC_LOGIN_009 – Null password                                         #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_LOGIN_009_null_password(self, serh_api):
        """TC_LOGIN_009: password set to null → 400."""
        payload = {"email": "kajal.gupta@kellton.com", "password": None, "captchaToken": "captcha-ok"}
        response = serh_api.login(payload)

        assert_negative_status(response, "TC_LOGIN_009")
        assert_has_common_field(response, "TC_LOGIN_009")

    # ------------------------------------------------------------------ #
    # TC_LOGIN_010 – Non-existent email                                    #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_LOGIN_010_nonexistent_email(self, serh_api):
        """TC_LOGIN_010: Unregistered email → 401 with generic error (no user enumeration)."""
        payload = {
            "email": "notregistered_xyz@example.com",
            "password": "Password@1234",
            "captchaToken": "captcha-ok",
        }
        response = serh_api.login(payload)

        # Should return 401 – server must not expose whether the user exists
        assert response.status_code == 401, (
            f"TC_LOGIN_010: Expected 401 but got {response.status_code}. Body: {response.text}"
        )
        assert_has_common_field(response, "TC_LOGIN_010")

    # ------------------------------------------------------------------ #
    # TC_LOGIN_011 – Invalid Content-Type header                           #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_LOGIN_011_invalid_content_type(self, serh_api, serh_payloads):
        """TC_LOGIN_011: Content-Type: text/plain → 415 Unsupported Media Type."""
        response = serh_api.post_plain_text(LOGIN_PATH, serh_payloads["login"])

        assert_non_server_error(response, "TC_LOGIN_011")
        assert response.status_code == 415, (
            f"TC_LOGIN_011: Expected 415 but got {response.status_code}. Body: {response.text}"
        )

    # ------------------------------------------------------------------ #
    # TC_LOGIN_012 – SQL injection in email                                #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.security
    def test_TC_LOGIN_012_sql_injection_email(self, serh_api):
        """TC_LOGIN_012: SQL injection in email field → 400 (must not crash or expose data)."""
        payload = {
            "email": "' OR '1'='1",
            "password": "Password@1234",
            "captchaToken": "captcha-ok",
        }
        response = serh_api.login(payload)

        assert_non_server_error(response, "TC_LOGIN_012")
        # Must be rejected – not return 200
        assert response.status_code != 200, (
            f"TC_LOGIN_012: SQL injection must not succeed. Got {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_has_common_field(response, "TC_LOGIN_012")

    # ------------------------------------------------------------------ #
    # TC_LOGIN_013 – Unknown extra field injection                         #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_LOGIN_013_unknown_field_injection(self, serh_api, serh_payloads):
        """TC_LOGIN_013: Extra unknown field in payload → must not cause 5xx."""
        payload = dict(serh_payloads["login"])
        payload["unknownField"] = "mutation-injection"

        response = serh_api.login(payload)

        assert_non_server_error(response, "TC_LOGIN_013")
        # Unknown fields must not yield a successful login
        assert response.status_code != 200, (
            f"TC_LOGIN_013: Unknown field injection must not return 200. "
            f"Got {response.status_code}. Body: {response.text}"
        )

    # ------------------------------------------------------------------ #
    # TC_LOGIN_014 – Wrong HTTP method (GET)                               #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_LOGIN_014_wrong_http_method_get(self, serh_api):
        """TC_LOGIN_014: GET /api/auth/login → 405 Method Not Allowed."""
        response = serh_api.get_on_post_endpoint(LOGIN_PATH)

        assert_non_server_error(response, "TC_LOGIN_014")
        assert response.status_code == 405, (
            f"TC_LOGIN_014: Expected 405 but got {response.status_code}. Body: {response.text}"
        )

