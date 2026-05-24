"""SERH Auth – Refresh Token endpoint tests.

CSV Reference: TC_REFRESH_001 – TC_REFRESH_007
Endpoint     : POST /api/auth/refresh
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

REFRESH_PATH = ENDPOINTS["refresh_token"]


class TestSERHRefreshToken:

    # ------------------------------------------------------------------ #
    # TC_REFRESH_001 – Valid refresh token (happy path)                    #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.positive
    def test_TC_REFRESH_001_valid_refresh_token(self, serh_api):
        """TC_REFRESH_001: POST /api/auth/refresh with a valid JWT refreshToken → 200.

        Precondition : SERH_ENABLE_LIVE_POSITIVE=true and SERH_REFRESH_TOKEN env var set.
        Expected     : 200 with new accessToken (and optionally new refreshToken).
        """
        if not live_positive_enabled():
            pytest.skip("Set SERH_ENABLE_LIVE_POSITIVE=true to run live refresh token test")

        token = os.getenv("SERH_REFRESH_TOKEN")
        if not token:
            pytest.skip("SERH_REFRESH_TOKEN env var not set")

        response = serh_api.refresh_token({"refreshToken": token})

        assert response.status_code == 200, (
            f"TC_REFRESH_001: Expected 200 but got {response.status_code}. Body: {response.text}"
        )
        body = response_json(response)
        assert body is not None, "TC_REFRESH_001: Expected JSON body"
        token_keys = {"accessToken", "token", "access_token"}
        assert any(k in body or k in body.get("data", {}) for k in token_keys), (
            f"TC_REFRESH_001: Expected accessToken in response. Body: {body}"
        )

    # ------------------------------------------------------------------ #
    # TC_REFRESH_002 – Expired refresh token                               #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_REFRESH_002_expired_refresh_token(self, serh_api):
        """TC_REFRESH_002: Expired JWT token → 401 Token Expired."""
        # This is a well-formed JWT that is long-past its exp claim
        expired_jwt = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJzdWIiOiJ0ZXN0LXVzZXIiLCJleHAiOjE2MDAwMDAwMDB9"
            ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        )
        response = serh_api.refresh_token({"refreshToken": expired_jwt})

        assert response.status_code == 401, (
            f"TC_REFRESH_002: Expected 401 but got {response.status_code}. Body: {response.text}"
        )
        assert_has_common_field(response, "TC_REFRESH_002")

    # ------------------------------------------------------------------ #
    # TC_REFRESH_003 – Malformed / non-JWT token string                   #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_REFRESH_003_malformed_token(self, serh_api):
        """TC_REFRESH_003: Non-JWT string as refreshToken → 401."""
        response = serh_api.refresh_token({"refreshToken": "this-is-not-a-jwt"})

        assert response.status_code == 401, (
            f"TC_REFRESH_003: Expected 401 but got {response.status_code}. Body: {response.text}"
        )
        assert_has_common_field(response, "TC_REFRESH_003")

    # ------------------------------------------------------------------ #
    # TC_REFRESH_004 – Missing refreshToken field                          #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_REFRESH_004_missing_refresh_token_field(self, serh_api):
        """TC_REFRESH_004: Empty payload {} → 400 (refreshToken is required)."""
        response = serh_api.refresh_token({})

        assert_negative_status(response, "TC_REFRESH_004")
        assert_has_common_field(response, "TC_REFRESH_004")

    # ------------------------------------------------------------------ #
    # TC_REFRESH_005 – Null refreshToken                                   #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_REFRESH_005_null_refresh_token(self, serh_api):
        """TC_REFRESH_005: refreshToken set to null → 400."""
        response = serh_api.refresh_token({"refreshToken": None})

        assert_negative_status(response, "TC_REFRESH_005")
        assert_has_common_field(response, "TC_REFRESH_005")

    # ------------------------------------------------------------------ #
    # TC_REFRESH_006 – Already-used refresh token (token rotation)         #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.security
    def test_TC_REFRESH_006_already_used_token(self, serh_api):
        """TC_REFRESH_006: Re-submit a previously consumed refreshToken → 401.

        Precondition : SERH_USED_REFRESH_TOKEN env var set to a token that was
                       already exchanged once (token rotation security check).
        """
        used_token = os.getenv("SERH_USED_REFRESH_TOKEN")
        if not used_token:
            pytest.skip("SERH_USED_REFRESH_TOKEN env var not set – set it to a spent token")

        response = serh_api.refresh_token({"refreshToken": used_token})

        assert response.status_code == 401, (
            f"TC_REFRESH_006: Reused token must be rejected with 401. "
            f"Got {response.status_code}. Body: {response.text}"
        )
        assert_has_common_field(response, "TC_REFRESH_006")

    # ------------------------------------------------------------------ #
    # TC_REFRESH_007 – Invalid Content-Type header                         #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_REFRESH_007_invalid_content_type(self, serh_api, serh_payloads):
        """TC_REFRESH_007: Content-Type: text/plain → 415 Unsupported Media Type."""
        response = serh_api.post_plain_text(REFRESH_PATH, serh_payloads["refresh_token"])

        assert_non_server_error(response, "TC_REFRESH_007")
        assert response.status_code == 415, (
            f"TC_REFRESH_007: Expected 415 but got {response.status_code}. Body: {response.text}"
        )

