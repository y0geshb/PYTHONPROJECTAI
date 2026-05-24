"""SERH Auth – Password Reset endpoint tests.

CSV Reference: TC_PWD_RESET_001 – TC_PWD_RESET_009
Endpoint     : POST /api/auth/password/reset
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

RESET_PATH = ENDPOINTS["password_reset"]

# A placeholder reset token used for negative tests where the content is
# irrelevant – the server will reject it as invalid regardless.
_DUMMY_RESET_TOKEN = "00000000-0000-0000-0000-000000000000"


class TestPasswordReset:

    # ------------------------------------------------------------------ #
    # TC_PWD_RESET_001 – Valid reset token + strong password (happy path)  #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.positive
    def test_TC_PWD_RESET_001_valid_reset(self, serh_api):
        """TC_PWD_RESET_001: Valid resetToken + strong newPassword → 200/204.

        Precondition : SERH_ENABLE_LIVE_POSITIVE=true, SERH_RESET_TOKEN and
                       SERH_NEW_PASSWORD env vars set.
        """
        if not live_positive_enabled():
            pytest.skip("Set SERH_ENABLE_LIVE_POSITIVE=true to run live password reset test")

        reset_token = os.getenv("SERH_RESET_TOKEN")
        new_password = os.getenv("SERH_NEW_PASSWORD", "NewTestPass#2026")
        if not reset_token:
            pytest.skip("SERH_RESET_TOKEN env var not set")

        response = serh_api.password_reset(
            {"resetToken": reset_token, "newPassword": new_password}
        )

        assert response.status_code in {200, 204}, (
            f"TC_PWD_RESET_001: Expected 200/204 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_has_common_field(response, "TC_PWD_RESET_001")

    # ------------------------------------------------------------------ #
    # TC_PWD_RESET_002 – Missing resetToken field                          #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_PWD_RESET_002_missing_reset_token(self, serh_api):
        """TC_PWD_RESET_002: Payload without resetToken → 400."""
        response = serh_api.password_reset({"newPassword": "NewPassword@1234"})

        assert_negative_status(response, "TC_PWD_RESET_002")
        assert_has_common_field(response, "TC_PWD_RESET_002")

    # ------------------------------------------------------------------ #
    # TC_PWD_RESET_003 – Missing newPassword field                         #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_PWD_RESET_003_missing_new_password(self, serh_api):
        """TC_PWD_RESET_003: Payload without newPassword → 400."""
        response = serh_api.password_reset({"resetToken": _DUMMY_RESET_TOKEN})

        assert_negative_status(response, "TC_PWD_RESET_003")
        assert_has_common_field(response, "TC_PWD_RESET_003")

    # ------------------------------------------------------------------ #
    # TC_PWD_RESET_004 – Weak / short new password                         #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_PWD_RESET_004_weak_password(self, serh_api):
        """TC_PWD_RESET_004: newPassword too short → 400 (password policy violation)."""
        response = serh_api.password_reset(
            {"resetToken": _DUMMY_RESET_TOKEN, "newPassword": "123"}
        )

        assert_negative_status(response, "TC_PWD_RESET_004")
        assert_has_common_field(response, "TC_PWD_RESET_004")

    # ------------------------------------------------------------------ #
    # TC_PWD_RESET_005 – Expired reset token                               #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_PWD_RESET_005_expired_reset_token(self, serh_api):
        """TC_PWD_RESET_005: Well-formed but expired resetToken → 400/401."""
        response = serh_api.password_reset(
            {
                "resetToken": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeee0001",
                "newPassword": "NewPassword@1234",
            }
        )

        assert response.status_code in {400, 401}, (
            f"TC_PWD_RESET_005: Expected 400/401 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_has_common_field(response, "TC_PWD_RESET_005")

    # ------------------------------------------------------------------ #
    # TC_PWD_RESET_006 – Invalid / random UUID reset token                 #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_PWD_RESET_006_invalid_reset_token(self, serh_api):
        """TC_PWD_RESET_006: Random UUID never issued as resetToken → 400/401."""
        response = serh_api.password_reset(
            {"resetToken": _DUMMY_RESET_TOKEN, "newPassword": "NewPassword@1234"}
        )

        assert response.status_code in {400, 401}, (
            f"TC_PWD_RESET_006: Expected 400/401 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_has_common_field(response, "TC_PWD_RESET_006")

    # ------------------------------------------------------------------ #
    # TC_PWD_RESET_007 – Empty payload {}                                  #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_PWD_RESET_007_empty_payload(self, serh_api):
        """TC_PWD_RESET_007: Empty body → 400 with both field errors."""
        response = serh_api.password_reset({})

        assert_negative_status(response, "TC_PWD_RESET_007")
        assert_has_common_field(response, "TC_PWD_RESET_007")

    # ------------------------------------------------------------------ #
    # TC_PWD_RESET_008 – Invalid Content-Type                              #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_PWD_RESET_008_invalid_content_type(self, serh_api, serh_payloads):
        """TC_PWD_RESET_008: Content-Type: text/plain → 415."""
        response = serh_api.post_plain_text(RESET_PATH, serh_payloads["password_reset"])

        assert_non_server_error(response, "TC_PWD_RESET_008")
        assert response.status_code == 415, (
            f"TC_PWD_RESET_008: Expected 415 but got {response.status_code}. "
            f"Body: {response.text}"
        )

    # ------------------------------------------------------------------ #
    # TC_PWD_RESET_009 – Reuse of the same reset token (security)          #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.security
    def test_TC_PWD_RESET_009_reuse_reset_token(self, serh_api):
        """TC_PWD_RESET_009: Re-submit an already-consumed resetToken → 400/401.

        Precondition : SERH_USED_RESET_TOKEN env var set to a reset token that
                       was already used in a prior successful password reset.
        """
        used_token = os.getenv("SERH_USED_RESET_TOKEN")
        if not used_token:
            pytest.skip("SERH_USED_RESET_TOKEN env var not set – set it to a consumed token")

        response = serh_api.password_reset(
            {"resetToken": used_token, "newPassword": "AnotherPass@5678"}
        )

        assert response.status_code in {400, 401}, (
            f"TC_PWD_RESET_009: Reused resetToken must be rejected. "
            f"Got {response.status_code}. Body: {response.text}"
        )
        assert_has_common_field(response, "TC_PWD_RESET_009")

