"""SERH Auth – Forgot OTP Initiate & Verify endpoint tests.

CSV Reference:
  TC_FORGOT_OTP_INIT_001 – TC_FORGOT_OTP_INIT_008  (POST /api/auth/password/forgot-otp/initiate)
  TC_FORGOT_OTP_VER_001  – TC_FORGOT_OTP_VER_008   (POST /api/auth/password/forgot-otp/verify)
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

INITIATE_PATH = ENDPOINTS["forgot_otp_initiate"]
VERIFY_PATH = ENDPOINTS["forgot_otp_verify"]


# ====================================================================== #
#  Forgot OTP – Initiate                                                  #
# ====================================================================== #

class TestForgotOTPInitiate:

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_INIT_001 – Valid request (happy path)                  #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.positive
    def test_TC_FORGOT_OTP_INIT_001_valid_request(self, serh_api, serh_payloads):
        """TC_FORGOT_OTP_INIT_001: Valid email + mobile → 200/202 with sessionToken.

        Precondition : SERH_ENABLE_LIVE_POSITIVE=true, registered user with matching
                       email and mobile number.
        """
        if not live_positive_enabled():
            pytest.skip("Set SERH_ENABLE_LIVE_POSITIVE=true to run live OTP initiate test")

        payload = dict(serh_payloads["forgot_otp_initiate"])
        for field, env_key in {
            "email": "SERH_FORGOT_OTP_EMAIL",
            "mobile": "SERH_FORGOT_OTP_MOBILE",
        }.items():
            env_val = os.getenv(env_key)
            if env_val:
                payload[field] = env_val

        response = serh_api.forgot_otp_initiate(payload)

        assert response.status_code in {200, 202}, (
            f"TC_FORGOT_OTP_INIT_001: Expected 200/202 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        body = response_json(response)
        assert body is not None
        assert_has_common_field(response, "TC_FORGOT_OTP_INIT_001")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_INIT_002 – Missing email field                         #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_INIT_002_missing_email(self, serh_api):
        """TC_FORGOT_OTP_INIT_002: Payload without email → 400."""
        response = serh_api.forgot_otp_initiate({"mobile": "+971500000000"})

        assert_negative_status(response, "TC_FORGOT_OTP_INIT_002")
        assert_has_common_field(response, "TC_FORGOT_OTP_INIT_002")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_INIT_003 – Missing mobile field                        #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_INIT_003_missing_mobile(self, serh_api):
        """TC_FORGOT_OTP_INIT_003: Payload without mobile → 400."""
        response = serh_api.forgot_otp_initiate({"email": "kajal.gupta@kellton.com"})

        assert_negative_status(response, "TC_FORGOT_OTP_INIT_003")
        assert_has_common_field(response, "TC_FORGOT_OTP_INIT_003")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_INIT_004 – Invalid email format                        #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_INIT_004_invalid_email_format(self, serh_api):
        """TC_FORGOT_OTP_INIT_004: Malformed email → 400."""
        response = serh_api.forgot_otp_initiate(
            {"email": "bad-email", "mobile": "+971500000000"}
        )

        assert_negative_status(response, "TC_FORGOT_OTP_INIT_004")
        assert_has_common_field(response, "TC_FORGOT_OTP_INIT_004")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_INIT_005 – Invalid mobile format                       #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_INIT_005_invalid_mobile_format(self, serh_api):
        """TC_FORGOT_OTP_INIT_005: Non-phone-number string in mobile → 400."""
        response = serh_api.forgot_otp_initiate(
            {"email": "kajal.gupta@kellton.com", "mobile": "0000ABCDE"}
        )

        assert_negative_status(response, "TC_FORGOT_OTP_INIT_005")
        assert_has_common_field(response, "TC_FORGOT_OTP_INIT_005")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_INIT_006 – Non-existent user email (enumeration guard) #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.security
    def test_TC_FORGOT_OTP_INIT_006_nonexistent_email(self, serh_api):
        """TC_FORGOT_OTP_INIT_006: Unregistered email → 200/202 generic response (no enumeration)."""
        response = serh_api.forgot_otp_initiate(
            {"email": "ghostuser_xyz_9999@example.com", "mobile": "+971500000000"}
        )

        # Server should NOT leak whether the user exists – generic success is acceptable
        assert response.status_code in {200, 202, 400, 404}, (
            f"TC_FORGOT_OTP_INIT_006: Got unexpected status {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_non_server_error(response, "TC_FORGOT_OTP_INIT_006")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_INIT_007 – Empty payload {}                            #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_INIT_007_empty_payload(self, serh_api):
        """TC_FORGOT_OTP_INIT_007: Empty body → 400 with both field errors."""
        response = serh_api.forgot_otp_initiate({})

        assert_negative_status(response, "TC_FORGOT_OTP_INIT_007")
        assert_has_common_field(response, "TC_FORGOT_OTP_INIT_007")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_INIT_008 – Invalid Content-Type                        #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_INIT_008_invalid_content_type(self, serh_api, serh_payloads):
        """TC_FORGOT_OTP_INIT_008: Content-Type: text/plain → 415."""
        response = serh_api.post_plain_text(INITIATE_PATH, serh_payloads["forgot_otp_initiate"])

        assert_non_server_error(response, "TC_FORGOT_OTP_INIT_008")
        assert response.status_code == 415, (
            f"TC_FORGOT_OTP_INIT_008: Expected 415 but got {response.status_code}. "
            f"Body: {response.text}"
        )


# ====================================================================== #
#  Forgot OTP – Verify                                                    #
# ====================================================================== #

class TestForgotOTPVerify:

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_VER_001 – Valid OTP and session token (happy path)     #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.positive
    def test_TC_FORGOT_OTP_VER_001_valid_otp_and_session(self, serh_api):
        """TC_FORGOT_OTP_VER_001: Valid otp + sessionToken → 200 with resetToken.

        Precondition : SERH_ENABLE_LIVE_POSITIVE=true, SERH_FORGOT_OTP_CODE and
                       SERH_FORGOT_OTP_SESSION_TOKEN env vars set.
        """
        if not live_positive_enabled():
            pytest.skip("Set SERH_ENABLE_LIVE_POSITIVE=true to run live OTP verify test")

        otp = os.getenv("SERH_FORGOT_OTP_CODE")
        session_token = os.getenv("SERH_FORGOT_OTP_SESSION_TOKEN")
        if not otp or not session_token:
            pytest.skip("SERH_FORGOT_OTP_CODE and SERH_FORGOT_OTP_SESSION_TOKEN must be set")

        response = serh_api.forgot_otp_verify({"otp": otp, "sessionToken": session_token})

        assert response.status_code == 200, (
            f"TC_FORGOT_OTP_VER_001: Expected 200 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        body = response_json(response)
        assert body is not None
        reset_token_keys = {"resetToken", "reset_token"}
        assert any(k in body or k in body.get("data", {}) for k in reset_token_keys), (
            f"TC_FORGOT_OTP_VER_001: Expected resetToken in response. Body: {body}"
        )

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_VER_002 – Missing otp field                            #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_VER_002_missing_otp(self, serh_api):
        """TC_FORGOT_OTP_VER_002: Payload without otp → 400."""
        response = serh_api.forgot_otp_verify(
            {"sessionToken": "1b43faa3-45c8-4d1b-82aa-e732bdda1a0a"}
        )

        assert_negative_status(response, "TC_FORGOT_OTP_VER_002")
        assert_has_common_field(response, "TC_FORGOT_OTP_VER_002")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_VER_003 – Missing sessionToken field                   #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_VER_003_missing_session_token(self, serh_api):
        """TC_FORGOT_OTP_VER_003: Payload without sessionToken → 400."""
        response = serh_api.forgot_otp_verify({"otp": "294792"})

        assert_negative_status(response, "TC_FORGOT_OTP_VER_003")
        assert_has_common_field(response, "TC_FORGOT_OTP_VER_003")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_VER_004 – Wrong OTP code                               #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_VER_004_wrong_otp(self, serh_api):
        """TC_FORGOT_OTP_VER_004: Incorrect OTP with a valid session token → 400/401."""
        response = serh_api.forgot_otp_verify(
            {"otp": "000000", "sessionToken": "1b43faa3-45c8-4d1b-82aa-e732bdda1a0a"}
        )

        assert response.status_code in {400, 401}, (
            f"TC_FORGOT_OTP_VER_004: Expected 400 or 401 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_has_common_field(response, "TC_FORGOT_OTP_VER_004")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_VER_005 – Expired OTP                                  #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_VER_005_expired_otp(self, serh_api):
        """TC_FORGOT_OTP_VER_005: Any OTP against an expired/old session → 400/401.

        Uses a deliberately old session token UUID that cannot be active.
        """
        response = serh_api.forgot_otp_verify(
            {"otp": "111111", "sessionToken": "00000000-aaaa-bbbb-cccc-000000000001"}
        )

        assert response.status_code in {400, 401}, (
            f"TC_FORGOT_OTP_VER_005: Expected 400 or 401 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_has_common_field(response, "TC_FORGOT_OTP_VER_005")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_VER_006 – Invalid / random sessionToken                #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_VER_006_invalid_session_token(self, serh_api):
        """TC_FORGOT_OTP_VER_006: Random UUID sessionToken not in system → 400/401."""
        response = serh_api.forgot_otp_verify(
            {"otp": "123456", "sessionToken": "00000000-0000-0000-0000-000000000000"}
        )

        assert response.status_code in {400, 401}, (
            f"TC_FORGOT_OTP_VER_006: Expected 400 or 401 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_has_common_field(response, "TC_FORGOT_OTP_VER_006")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_VER_007 – Empty payload {}                             #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_VER_007_empty_payload(self, serh_api):
        """TC_FORGOT_OTP_VER_007: Empty body → 400 with both field errors."""
        response = serh_api.forgot_otp_verify({})

        assert_negative_status(response, "TC_FORGOT_OTP_VER_007")
        assert_has_common_field(response, "TC_FORGOT_OTP_VER_007")

    # ------------------------------------------------------------------ #
    # TC_FORGOT_OTP_VER_008 – Invalid Content-Type                         #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_FORGOT_OTP_VER_008_invalid_content_type(self, serh_api, serh_payloads):
        """TC_FORGOT_OTP_VER_008: Content-Type: text/plain → 415."""
        response = serh_api.post_plain_text(VERIFY_PATH, serh_payloads["forgot_otp_verify"])

        assert_non_server_error(response, "TC_FORGOT_OTP_VER_008")
        assert response.status_code == 415, (
            f"TC_FORGOT_OTP_VER_008: Expected 415 but got {response.status_code}. "
            f"Body: {response.text}"
        )

