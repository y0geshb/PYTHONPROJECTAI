"""SERH Auth – Account Unlock endpoint tests.

CSV Reference: TC_ACC_UNLOCK_001 – TC_ACC_UNLOCK_010
Endpoint     : POST /api/auth/account/unlock
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

UNLOCK_PATH = ENDPOINTS["account_unlock"]

_DUMMY_UNLOCK_TOKEN = "00000000-0000-0000-0000-000000000000"
_TEST_EMAIL = "kajal.gupta@kellton.com"


class TestAccountUnlock:

    # ------------------------------------------------------------------ #
    # TC_ACC_UNLOCK_001 – Valid unlock request (happy path)                #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.positive
    def test_TC_ACC_UNLOCK_001_valid_unlock_request(self, serh_api):
        """TC_ACC_UNLOCK_001: Valid email + unlockToken → 200/204.

        Precondition : SERH_ENABLE_LIVE_POSITIVE=true, account is locked,
                       SERH_UNLOCK_EMAIL and SERH_UNLOCK_TOKEN env vars set.
        """
        if not live_positive_enabled():
            pytest.skip("Set SERH_ENABLE_LIVE_POSITIVE=true to run live account unlock test")

        email = os.getenv("SERH_UNLOCK_EMAIL")
        token = os.getenv("SERH_UNLOCK_TOKEN")
        if not email or not token:
            pytest.skip("SERH_UNLOCK_EMAIL and SERH_UNLOCK_TOKEN must be set")

        response = serh_api.account_unlock({"email": email, "unlockToken": token})

        assert response.status_code in {200, 204}, (
            f"TC_ACC_UNLOCK_001: Expected 200/204 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_has_common_field(response, "TC_ACC_UNLOCK_001")

    # ------------------------------------------------------------------ #
    # TC_ACC_UNLOCK_002 – Missing email field                              #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_ACC_UNLOCK_002_missing_email(self, serh_api):
        """TC_ACC_UNLOCK_002: Payload without email → 400."""
        response = serh_api.account_unlock({"unlockToken": "27284cab-fa56-464d-9c62-a0dc66f0aed3"})

        assert_negative_status(response, "TC_ACC_UNLOCK_002")
        assert_has_common_field(response, "TC_ACC_UNLOCK_002")

    # ------------------------------------------------------------------ #
    # TC_ACC_UNLOCK_003 – Missing unlockToken field                        #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_ACC_UNLOCK_003_missing_unlock_token(self, serh_api):
        """TC_ACC_UNLOCK_003: Payload without unlockToken → 400."""
        response = serh_api.account_unlock({"email": _TEST_EMAIL})

        assert_negative_status(response, "TC_ACC_UNLOCK_003")
        assert_has_common_field(response, "TC_ACC_UNLOCK_003")

    # ------------------------------------------------------------------ #
    # TC_ACC_UNLOCK_004 – Invalid / random unlockToken                     #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_ACC_UNLOCK_004_invalid_unlock_token(self, serh_api):
        """TC_ACC_UNLOCK_004: Random UUID unlockToken not issued by system → 400/401."""
        response = serh_api.account_unlock(
            {"email": _TEST_EMAIL, "unlockToken": _DUMMY_UNLOCK_TOKEN}
        )

        assert response.status_code in {400, 401}, (
            f"TC_ACC_UNLOCK_004: Expected 400/401 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_has_common_field(response, "TC_ACC_UNLOCK_004")

    # ------------------------------------------------------------------ #
    # TC_ACC_UNLOCK_005 – Expired unlockToken                              #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_ACC_UNLOCK_005_expired_unlock_token(self, serh_api):
        """TC_ACC_UNLOCK_005: Well-formed but expired unlockToken → 400/401."""
        response = serh_api.account_unlock(
            {
                "email": _TEST_EMAIL,
                "unlockToken": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeee0099",
            }
        )

        assert response.status_code in {400, 401}, (
            f"TC_ACC_UNLOCK_005: Expected 400/401 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_has_common_field(response, "TC_ACC_UNLOCK_005")

    # ------------------------------------------------------------------ #
    # TC_ACC_UNLOCK_006 – Non-existent email (enumeration guard)           #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.security
    def test_TC_ACC_UNLOCK_006_nonexistent_email(self, serh_api):
        """TC_ACC_UNLOCK_006: Email not registered → 400/404 generic error."""
        response = serh_api.account_unlock(
            {
                "email": "nobody_xyz_9999@example.com",
                "unlockToken": "27284cab-fa56-464d-9c62-a0dc66f0aed3",
            }
        )

        assert response.status_code in {400, 401, 404}, (
            f"TC_ACC_UNLOCK_006: Got unexpected status {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_non_server_error(response, "TC_ACC_UNLOCK_006")

    # ------------------------------------------------------------------ #
    # TC_ACC_UNLOCK_007 – Empty payload {}                                 #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_ACC_UNLOCK_007_empty_payload(self, serh_api):
        """TC_ACC_UNLOCK_007: Empty body → 400 with both field errors."""
        response = serh_api.account_unlock({})

        assert_negative_status(response, "TC_ACC_UNLOCK_007")
        assert_has_common_field(response, "TC_ACC_UNLOCK_007")

    # ------------------------------------------------------------------ #
    # TC_ACC_UNLOCK_008 – Invalid Content-Type header                      #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_ACC_UNLOCK_008_invalid_content_type(self, serh_api, serh_payloads):
        """TC_ACC_UNLOCK_008: Content-Type: text/plain → 415."""
        response = serh_api.post_plain_text(UNLOCK_PATH, serh_payloads["account_unlock"])

        assert_non_server_error(response, "TC_ACC_UNLOCK_008")
        assert response.status_code == 415, (
            f"TC_ACC_UNLOCK_008: Expected 415 but got {response.status_code}. "
            f"Body: {response.text}"
        )

    # ------------------------------------------------------------------ #
    # TC_ACC_UNLOCK_009 – Unlock an already-active (not locked) account    #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_ACC_UNLOCK_009_already_unlocked_account(self, serh_api):
        """TC_ACC_UNLOCK_009: Unlock attempt on an active account → 400/409.

        Precondition : SERH_ACTIVE_USER_EMAIL and SERH_ANY_UNLOCK_TOKEN env vars
                       set, pointing to an active (non-locked) user account.
        """
        email = os.getenv("SERH_ACTIVE_USER_EMAIL", _TEST_EMAIL)
        token = os.getenv("SERH_ANY_UNLOCK_TOKEN", "27284cab-fa56-464d-9c62-a0dc66f0aed3")

        response = serh_api.account_unlock({"email": email, "unlockToken": token})

        # If account is active, API must reject with 400 or 409 (not silently succeed)
        assert response.status_code in {400, 401, 409}, (
            f"TC_ACC_UNLOCK_009: Expected 400/409 for already-active account but got "
            f"{response.status_code}. Body: {response.text}"
        )
        assert_has_common_field(response, "TC_ACC_UNLOCK_009")

    # ------------------------------------------------------------------ #
    # TC_ACC_UNLOCK_010 – Reuse of the same unlockToken (security)         #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.security
    def test_TC_ACC_UNLOCK_010_reuse_unlock_token(self, serh_api):
        """TC_ACC_UNLOCK_010: Re-submit an already-used unlockToken → 400/401.

        Precondition : SERH_USED_UNLOCK_TOKEN env var set to a token that was
                       already consumed in a prior successful unlock.
        """
        used_token = os.getenv("SERH_USED_UNLOCK_TOKEN")
        if not used_token:
            pytest.skip("SERH_USED_UNLOCK_TOKEN env var not set – set it to a consumed token")

        response = serh_api.account_unlock({"email": _TEST_EMAIL, "unlockToken": used_token})

        assert response.status_code in {400, 401}, (
            f"TC_ACC_UNLOCK_010: Reused unlockToken must be rejected. "
            f"Got {response.status_code}. Body: {response.text}"
        )
        assert_has_common_field(response, "TC_ACC_UNLOCK_010")

