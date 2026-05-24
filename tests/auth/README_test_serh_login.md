# SERH Auth Login Test Suite

This README documents the test cases, scenarios, data sources, and dependencies for `test_serh_login.py` in this folder.

---

## Overview

This suite tests the `/api/auth/login` endpoint for the SERH authentication service. It covers both positive and negative scenarios, including security and input validation checks. Each test case is mapped to a specific scenario and is referenced by a unique test case ID (TC_LOGIN_001 – TC_LOGIN_014).

---

## Test Cases and Scenarios

| Test Case ID   | Scenario Description                                      | Expected Result / Notes |
|---------------|----------------------------------------------------------|------------------------|
| TC_LOGIN_001  | Valid login (happy path)                                 | 200 OK, returns access/refresh tokens. Uses env vars if set, else default payload. |
| TC_LOGIN_002  | Invalid email format                                     | 400 Bad Request        |
| TC_LOGIN_003  | Wrong password                                           | 401 Unauthorized, error message must not reveal field |
| TC_LOGIN_004  | Missing email field                                      | 400 Bad Request        |
| TC_LOGIN_005  | Missing password field                                   | 400 Bad Request        |
| TC_LOGIN_006  | Missing captchaToken field                               | 400 Bad Request        |
| TC_LOGIN_007  | Empty payload                                            | 400 Bad Request        |
| TC_LOGIN_008  | Null email                                               | 400 Bad Request        |
| TC_LOGIN_009  | Null password                                            | 400 Bad Request        |
| TC_LOGIN_010  | Non-existent email                                       | 401 Unauthorized, generic error (no user enumeration) |
| TC_LOGIN_011  | Invalid Content-Type header (text/plain)                 | 415 Unsupported Media Type |
| TC_LOGIN_012  | SQL injection in email field                             | 400 Bad Request, must not crash or expose data |
| TC_LOGIN_013  | Unknown/extra field in payload                           | Not 200 OK, must not cause 5xx |
| TC_LOGIN_014  | Wrong HTTP method (GET on POST endpoint)                 | 405 Method Not Allowed |

---

## Data Sources and References

- **Payloads:**
  - Default login payloads are loaded from `test_data/serh_auth_payloads.json` via the `serh_payloads` fixture.
  - If set, the following environment variables override the payload fields:
    - `API_USER_EMAIL`
    - `API_USER_PASSWORD`
    - `SERH_CAPTCHA_TOKEN`
- **API Client:**
  - The `serh_api` fixture provides an instance of the endpoint wrapper (`SERHAuthAPI`), which calls the actual API.
- **Helpers:**
  - Assertion and endpoint helpers are in `auth_test_helpers.py`.
- **Configuration:**
  - The API base URL is set via the `base_url` fixture (from pytest or environment).
  - The test suite will skip if the API is not reachable.

---

## Dependencies

- `auth_test_helpers.py` – Assertion helpers and endpoint constants.
- `conftest.py` – Fixtures for payloads and API client.
- `serh_auth_api.py` – API wrapper for endpoint calls.
- `test_data/serh_auth_payloads.json` – Default payloads.
- API server (mock or real) must be running and reachable at the configured base URL.

---

## How to Run

1. Ensure all dependencies and fixtures are present.
2. Set environment variables for credentials if needed, or edit `test_data/serh_auth_payloads.json`.
3. Start the API server (mock or real).
4. Run the tests:
   ```sh
   pytest tests/auth/test_serh_login.py
   ```

---

## Notes

- The test suite is designed to be robust and secure, ensuring no sensitive information is leaked in error messages.
- All negative and edge cases are covered for the login endpoint.
- For new scenarios, add a new test method following the naming and docstring conventions.
