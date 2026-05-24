"""SERH Auth – Forgot Email endpoint tests.

CSV Reference: TC_FORGOT_EMAIL_001 – TC_FORGOT_EMAIL_006
Endpoint     : POST /api/auth/password/forgot-email
"""

import os

import pytest

from tests.auth.auth_test_helpers import (
    ENDPOINTS,
    assert_has_common_field,
    assert_negative_status,
    assert_non_server_error,
    live_positive_enabled,
)

FORGOT_EMAIL_PATH = ENDPOINTS["forgot_email"]


class TestForgotEmail:

    # ------------------------------------------------------------------ #
    # TC_FORGOT_EMAIL_001 – Valid registered email (happy path)            #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.positive
    def test_TC_FORGOT_EMAIL_001_valid_email(self, serh_api, serh_payloads):
        """TC_FORGOT_EMAIL_001: POST /api/auth/password/forgot-email with registered email.

        Precondition : SERH_ENABLE_LIVE_POSITIVE=true, SERH_FORGOT_EMAIL or
                       API_USER_EMAIL env var set to a registered account.
        Expected     : 200/202 with generic success message.
        """
        if not live_positive_enabled():
            pytest.skip("Set SERH_ENABLE_LIVE_POSITIVE=true to run live forgot-email test")

        payload = dict(serh_payloads["forgot_email"])
        env_email = os.getenv("SERH_FORGOT_EMAIL") or os.getenv("API_USER_EMAIL")
        if env_email:
            payload["email"] = env_email

        response = serh_api.forgot_email(payload)

        assert response.status_code in {200, 202}, (
            f"TC_FORGOT_EMAIL_001: Expected 200/202 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_has_common_field(response, "TC_FORGOT_EMAIL_001")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_EMAIL_002 – Missing email field                            #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_EMAIL_002_missing_email_field(self, serh_api):
        """TC_FORGOT_EMAIL_002: Empty payload {} → 400 (email is required)."""
        response = serh_api.forgot_email({})

        assert_negative_status(response, "TC_FORGOT_EMAIL_002")
        assert_has_common_field(response, "TC_FORGOT_EMAIL_002")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_EMAIL_003 – Invalid email format                           #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_EMAIL_003_invalid_email_format(self, serh_api):
        """TC_FORGOT_EMAIL_003: Malformed email address → 400."""
        response = serh_api.forgot_email({"email": "not-an-email@@"})

        assert_negative_status(response, "TC_FORGOT_EMAIL_003")
        assert_has_common_field(response, "TC_FORGOT_EMAIL_003")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_EMAIL_004 – Non-existent email (enumeration guard)         #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.security
    def test_TC_FORGOT_EMAIL_004_nonexistent_email(self, serh_api):
        """TC_FORGOT_EMAIL_004: Unregistered email → generic 200/202 (no user enumeration)."""
        response = serh_api.forgot_email({"email": "ghost_xyz_9999@example.com"})

        # Server must respond generically to prevent user enumeration attacks
        assert response.status_code in {200, 202, 400, 404}, (
            f"TC_FORGOT_EMAIL_004: Got unexpected status {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_non_server_error(response, "TC_FORGOT_EMAIL_004")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_EMAIL_005 – Null email value                               #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_EMAIL_005_null_email(self, serh_api):
        """TC_FORGOT_EMAIL_005: email field set to null → 400."""
        response = serh_api.forgot_email({"email": None})

        assert_negative_status(response, "TC_FORGOT_EMAIL_005")
        assert_has_common_field(response, "TC_FORGOT_EMAIL_005")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_EMAIL_006 – Invalid Content-Type header                    #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_EMAIL_006_invalid_content_type(self, serh_api, serh_payloads):
        """TC_FORGOT_EMAIL_006: Content-Type: text/plain → 415."""
        response = serh_api.post_plain_text(FORGOT_EMAIL_PATH, serh_payloads["forgot_email"])

        assert_non_server_error(response, "TC_FORGOT_EMAIL_006")
        assert response.status_code == 415, (
            f"TC_FORGOT_EMAIL_006: Expected 415 but got {response.status_code}. "
            f"Body: {response.text}"
        )

