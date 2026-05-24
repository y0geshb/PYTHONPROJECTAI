"""Helpers for reading JSON stub responses from disk."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _responses_root() -> Path:
    return Path(__file__).resolve().parents[1] / "mock-responses"


def load_stub_response(domain: str, name: str) -> dict[str, Any]:
    """Load a JSON stub response by domain and file name without extension."""
    response_path = _responses_root() / domain / f"{name}.json"
    with response_path.open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)