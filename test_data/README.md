# Test Data

This folder contains JSON files used by pytest parametrized tests.

## Files

| File | Purpose |
|------|---------|
| `valid_payloads.json` | Success scenario payloads (one key per endpoint) |
| `invalid_payloads.json` | Error scenario payloads with expected status codes |

## How to Use in pytest

### Loading data in a test

```python
import json
import pytest

# Load at module level so it is available to all tests
with open("test_data/invalid_payloads.json") as f:
    INVALID_DATA = json.load(f)

# Extract cases for a specific endpoint
LOGIN_INVALID_CASES = [
    (item["case"], item["payload"], item["expected_status"])
    for item in INVALID_DATA["auth_login"]
]
```

### Using @pytest.mark.parametrize

```python
@pytest.mark.negative
@pytest.mark.parametrize("case,payload,expected_status", LOGIN_INVALID_CASES)
def test_login_invalid_input_returns_error(self, base_url, case, payload, expected_status):
    """Verify login endpoint rejects invalid input with the correct error status.

    Parametrized over all invalid cases defined in test_data/invalid_payloads.json.
    """
    from config.http_client import APIClient
    client = APIClient(base_url=base_url)
    response = client.post("/api/v1/auth/login", json=payload, timeout=10)

    assert response.status_code == expected_status, (
        f"Case: '{case}' — Expected {expected_status} but got "
        f"{response.status_code}. Body: {response.text}"
    )
```

## Test Data Conventions

- Email fields use the `@testdomain.com` suffix
- Passwords use the format `TestPass#YYYY` (never real passwords)
- All `invalid_payloads.json` entries have three keys:
  - `case` — human-readable description of what is invalid
  - `payload` — the request body to send
  - `expected_status` — the HTTP status code the API should return (400, 422, 409, etc.)

