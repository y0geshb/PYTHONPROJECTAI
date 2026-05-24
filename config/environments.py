"""Helper functions for loading and reading environment configuration."""

import os
from pathlib import Path

from dotenv import dotenv_values, load_dotenv

_ENV_LOADED = False


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_if_exists(path: Path, *, override: bool) -> None:
    if path.exists():
        load_dotenv(dotenv_path=path, override=override)


def _fill_missing_from_file(path: Path) -> None:
    if not path.exists():
        return

    for key, value in dotenv_values(path).items():
        if value is None:
            continue

        current_value = os.getenv(key)
        if current_value is None or current_value == "":
            os.environ[key] = value


def _configured_env_name() -> str:
    return os.getenv("ENV", "qa").strip().lower()


def get_api_mode() -> str:
    """Return the active API mode: mock or real."""
    configured_mode = os.getenv("API_MODE", "").strip().lower()
    if configured_mode:
        return configured_mode

    return "mock" if _configured_env_name() in {"mock", "mocks"} else "real"


def ensure_environment_loaded() -> str:
    """Load root and mode-specific environment files once per process."""
    global _ENV_LOADED
    if _ENV_LOADED:
        return get_api_mode()

    root = _project_root()
    _load_if_exists(root / ".env", override=False)

    mode = get_api_mode()
    env_name = _configured_env_name()
    env_file_name = ".env.mocks" if mode == "mock" else f".env.{env_name}"
    env_file_path = root / "config" / env_file_name
    if mode == "mock":
        _load_if_exists(env_file_path, override=True)
    else:
        _fill_missing_from_file(env_file_path)

    _ENV_LOADED = True
    return get_api_mode()


def is_mock_mode() -> bool:
    """Return True when the framework should target the local mock server."""
    return ensure_environment_loaded() == "mock"


def get_base_url() -> str:
    """Return API base URL from the active environment configuration."""
    ensure_environment_loaded()
    return os.getenv("API_BASE_URL")


def get_auth_headers(token: str) -> dict:
    """Return standard bearer authentication headers."""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
