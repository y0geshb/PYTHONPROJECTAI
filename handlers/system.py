"""System and protected-resource handlers for the local mock server."""

from __future__ import annotations

from typing import Any

RouteResult = tuple[int, dict[str, str], dict[str, Any]]

_JSON_HEADERS = {"Content-Type": "application/json; charset=utf-8"}
_VALID_TOKEN = "mock-access-token"


def handle_system_request(method: str, path: str, headers: dict[str, str]) -> RouteResult | None:
    """Return a mock response for system routes or None if unmatched."""
    if path == "/api/health":
        if method != "GET":
            return _method_not_allowed(["GET"])
        return 200, dict(_JSON_HEADERS), {
            "status": "UP",
            "service": "serh-mock-server",
            "mode": "mock",
        }

    if path == "/api/v1/users":
        if method != "GET":
            return _method_not_allowed(["GET"])

        auth_header = headers.get("Authorization", "")
        if auth_header != f"Bearer {_VALID_TOKEN}":
            return 401, dict(_JSON_HEADERS), {
                "message": "Unauthorized",
                "error": "UNAUTHORIZED",
                "success": False,
            }

        return 200, dict(_JSON_HEADERS), {
            "data": [
                {
                    "id": "user-001",
                    "email": "mockuser@example.com",
                    "roles": ["qa-tester"],
                }
            ],
            "success": True,
        }

    return None


def _method_not_allowed(allowed_methods: list[str]) -> RouteResult:
    return 405, {**_JSON_HEADERS, "Allow": ", ".join(allowed_methods)}, {
        "message": "Method not allowed",
        "error": "METHOD_NOT_ALLOWED",
        "allowedMethods": allowed_methods,
    }