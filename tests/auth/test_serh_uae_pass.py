"""SERH Auth – UAE Pass endpoint tests.

CSV Reference:
  TC_UAEPASS_START_001 – TC_UAEPASS_START_003   (GET  /api/auth/uae-pass/start)
  TC_UAEPASS_CB_001    – TC_UAEPASS_CB_008       (POST /api/auth/uae-pass/callback)
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

UAE_PASS_START_PATH = ENDPOINTS["uae_pass_start"]
UAE_PASS_CB_PATH = ENDPOINTS["uae_pass_callback"]

VALID_CALLBACK_PAYLOAD = {
    "state": "612d972e-e0bb-4228-83f9-d76e055a2539",
    "code": "authorization-code",
    "emiratesId": "784198765432109",
}


class TestUAEPassStart:

    # ------------------------------------------------------------------ #
    # TC_UAEPASS_START_001 – Valid GET request                             #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.positive
    def test_TC_UAEPASS_START_001_valid_get_request(self, serh_api):
        """TC_UAEPASS_START_001: GET /api/auth/uae-pass/start → 200 or 302 redirect.

        When the server returns 302 the Location header must point to the
        UAE Pass OAuth provider URL.
        """
        response = serh_api.uae_pass_start()

        assert response.status_code in {200, 302}, (
            f"TC_UAEPASS_START_001: Expected 200 or 302 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        if response.status_code == 302:
            assert "Location" in response.headers, (
                "TC_UAEPASS_START_001: 302 response must include Location header"
            )
            location = response.headers["Location"]
            assert location.startswith("http"), (
                f"TC_UAEPASS_START_001: Location header must be a URL, got: {location}"
            )

    # ------------------------------------------------------------------ #
    # TC_UAEPASS_START_002 – Wrong HTTP method (POST)                      #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_UAEPASS_START_002_wrong_http_method_post(self, serh_api):
        """TC_UAEPASS_START_002: POST to a GET-only endpoint → 405."""
        response = serh_api.post_plain_text(UAE_PASS_START_PATH, {})

        assert_non_server_error(response, "TC_UAEPASS_START_002")
        assert response.status_code == 405, (
            f"TC_UAEPASS_START_002: Expected 405 but got {response.status_code}. "
            f"Body: {response.text}"
        )

    # ------------------------------------------------------------------ #
    # TC_UAEPASS_START_003 – Arbitrary query parameters                    #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_UAEPASS_START_003_with_random_query_params(self, serh_api):
        """TC_UAEPASS_START_003: GET with unexpected query params must not cause 5xx."""

        response = serh_api.client.get(
            UAE_PASS_START_PATH,
            params={"foo": "bar", "baz": "qux"},
            allow_redirects=False,
        )
        assert_non_server_error(response, "TC_UAEPASS_START_003")
        assert response.status_code in {200, 302, 400}, (
            f"TC_UAEPASS_START_003: Got unexpected status {response.status_code}. "
            f"Body: {response.text}"
        )


class TestUAEPassCallback:

    # ------------------------------------------------------------------ #
    # TC_UAEPASS_CB_001 – Valid callback (happy path)                      #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.positive
    def test_TC_UAEPASS_CB_001_valid_callback(self, serh_api):
        """TC_UAEPASS_CB_001: POST /api/auth/uae-pass/callback with valid state/code/emiratesId.

        Precondition : SERH_ENABLE_LIVE_POSITIVE=true and matching env vars set.
        Expected     : 200 with accessToken + refreshToken.
        """
        if not live_positive_enabled():
            pytest.skip("Set SERH_ENABLE_LIVE_POSITIVE=true to run UAE Pass callback live test")

        payload = dict(VALID_CALLBACK_PAYLOAD)
        for field, env_key in {
            "state": "SERH_UAEPASS_STATE",
            "code": "SERH_UAEPASS_CODE",
            "emiratesId": "SERH_UAEPASS_EMIRATES_ID",
        }.items():
            env_val = os.getenv(env_key)
            if env_val:
                payload[field] = env_val

        response = serh_api.uae_pass_callback(payload)

        assert response.status_code == 200, (
            f"TC_UAEPASS_CB_001: Expected 200 but got {response.status_code}. Body: {response.text}"
        )
        body = response_json(response)
        assert body is not None
        token_keys = {"accessToken", "token", "access_token"}
        assert any(k in body or k in body.get("data", {}) for k in token_keys), (
            f"TC_UAEPASS_CB_001: Expected token in response. Body: {body}"
        )

    # ------------------------------------------------------------------ #
    # TC_UAEPASS_CB_002 – Missing state field                              #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_UAEPASS_CB_002_missing_state(self, serh_api):
        """TC_UAEPASS_CB_002: Payload without state → 400."""
        payload = {"code": "authorization-code", "emiratesId": "784198765432109"}
        response = serh_api.uae_pass_callback(payload)

        assert_negative_status(response, "TC_UAEPASS_CB_002")
        assert_has_common_field(response, "TC_UAEPASS_CB_002")

    # ------------------------------------------------------------------ #
    # TC_UAEPASS_CB_003 – Missing code field                               #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_UAEPASS_CB_003_missing_code(self, serh_api):
        """TC_UAEPASS_CB_003: Payload without code → 400."""
        payload = {"state": "612d972e-e0bb-4228-83f9-d76e055a2539", "emiratesId": "784198765432109"}
        response = serh_api.uae_pass_callback(payload)

        assert_negative_status(response, "TC_UAEPASS_CB_003")
        assert_has_common_field(response, "TC_UAEPASS_CB_003")

    # ------------------------------------------------------------------ #
    # TC_UAEPASS_CB_004 – Missing emiratesId field                         #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_UAEPASS_CB_004_missing_emirates_id(self, serh_api):
        """TC_UAEPASS_CB_004: Payload without emiratesId → 400."""
        payload = {
            "state": "612d972e-e0bb-4228-83f9-d76e055a2539",
            "code": "authorization-code",
        }
        response = serh_api.uae_pass_callback(payload)

        assert_negative_status(response, "TC_UAEPASS_CB_004")
        assert_has_common_field(response, "TC_UAEPASS_CB_004")

    # ------------------------------------------------------------------ #
    # TC_UAEPASS_CB_005 – Invalid emiratesId format                        #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_UAEPASS_CB_005_invalid_emirates_id_format(self, serh_api):
        """TC_UAEPASS_CB_005: Non-numeric or wrong-length emiratesId → 400."""
        payload = {
            "state": "612d972e-e0bb-4228-83f9-d76e055a2539",
            "code": "authorization-code",
            "emiratesId": "INVALID-ID",
        }
        response = serh_api.uae_pass_callback(payload)

        assert_negative_status(response, "TC_UAEPASS_CB_005")
        assert_has_common_field(response, "TC_UAEPASS_CB_005")

    # ------------------------------------------------------------------ #
    # TC_UAEPASS_CB_006 – Tampered / random state (CSRF check)             #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.security
    def test_TC_UAEPASS_CB_006_invalid_state(self, serh_api):
        """TC_UAEPASS_CB_006: Random state UUID not matching any session → 400 or 401."""
        payload = {
            "state": "00000000-0000-0000-0000-000000000000",
            "code": "authorization-code",
            "emiratesId": "784198765432109",
        }
        response = serh_api.uae_pass_callback(payload)

        assert response.status_code in {400, 401}, (
            f"TC_UAEPASS_CB_006: Expected 400 or 401 but got {response.status_code}. "
            f"Body: {response.text}"
        )
        assert_has_common_field(response, "TC_UAEPASS_CB_006")

    # ------------------------------------------------------------------ #
    # TC_UAEPASS_CB_007 – Empty payload {}                                 #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_UAEPASS_CB_007_empty_payload(self, serh_api):
        """TC_UAEPASS_CB_007: Empty JSON body → 400 with all required-field errors."""
        response = serh_api.uae_pass_callback({})

        assert_negative_status(response, "TC_UAEPASS_CB_007")
        assert_has_common_field(response, "TC_UAEPASS_CB_007")

    # ------------------------------------------------------------------ #
    # TC_UAEPASS_CB_008 – Invalid Content-Type                             #
    # ------------------------------------------------------------------ #
    @pytest.mark.regression
    @pytest.mark.negative
    def test_TC_UAEPASS_CB_008_invalid_content_type(self, serh_api):
        """TC_UAEPASS_CB_008: Content-Type: text/plain → 415."""
        response = serh_api.post_plain_text(UAE_PASS_CB_PATH, VALID_CALLBACK_PAYLOAD)

        assert_non_server_error(response, "TC_UAEPASS_CB_008")
        assert response.status_code == 415, (
            f"TC_UAEPASS_CB_008: Expected 415 but got {response.status_code}. Body: {response.text}"
        )

