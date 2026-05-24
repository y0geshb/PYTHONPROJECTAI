"""
utilities/env_validation.py
Validates that required environment variables are set before the test suite runs.
Call require_env() from conftest.py or individual test modules.
"""
import os
import sys


# Map of variable name -> human-readable description
REQUIRED_VARS = {
    "API_BASE_URL": "Target API base URL (e.g. https://your-api.com)",
}

# Required only when running live positive tests
LIVE_POSITIVE_VARS = {
    "API_USER_EMAIL": "QA test user email address",
    "API_USER_PASSWORD": "QA test user password",
    "SERH_CAPTCHA_TOKEN": "Captcha token for login tests",
}

# Required by specific test flows when live testing is active
OPTIONAL_FLOW_VARS = {
    "SERH_REFRESH_TOKEN": "JWT refresh token for refresh-token tests",
    "SERH_FORGOT_OTP_SESSION_TOKEN": "Session token for OTP verification tests",
    "SERH_RESET_TOKEN": "Token for password-reset tests",
    "SERH_NEW_PASSWORD": "New password value for reset-flow tests",
    "SERH_UNLOCK_TOKEN": "Token for account-unlock tests",
    "MOCK_VALID_EMAIL": "Valid email for mock server credential checks",
    "MOCK_VALID_PASSWORD": "Valid password for mock server credential checks",
}


def require_env(var_names: list[str]) -> dict[str, str]:
    """
    Ensure all listed environment variables are set and non-empty.
    Exits with a descriptive error if any are missing.

    Args:
        var_names: List of environment variable names to require.

    Returns:
        Dict mapping each name to its value.
    """
    missing = []
    values: dict[str, str] = {}

    for name in var_names:
        val = os.getenv(name, "").strip()
        if not val:
            missing.append(name)
        else:
            values[name] = val

    if missing:
        print("\n[env_validation] ERROR: The following required environment variables are not set:")
        all_known = {**REQUIRED_VARS, **LIVE_POSITIVE_VARS, **OPTIONAL_FLOW_VARS}
        for name in missing:
            desc = all_known.get(name, "No description available")
            print(f"  - {name}: {desc}")
        print("\nCopy .env.example to .env and fill in the missing values.")
        sys.exit(1)

    return values


def check_required() -> None:
    """Call at application startup to validate the always-required env vars."""
    require_env(list(REQUIRED_VARS.keys()))


def check_live_positive() -> None:
    """Call before running live positive tests."""
    require_env(list(LIVE_POSITIVE_VARS.keys()))


def get_or_skip(var_name: str, pytest_skip_fn=None) -> str | None:
    """
    Return the environment variable value, or skip the test if it is missing.
    Pass pytest.skip as pytest_skip_fn when calling from a test.
    """
    val = os.getenv(var_name, "").strip()
    if not val and pytest_skip_fn:
        pytest_skip_fn(f"Set {var_name} environment variable to run this test.")
    return val or None
