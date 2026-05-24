"""Central request router for the local mock server."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

from handlers.auth import handle_auth_request
from handlers.system import handle_system_request

RouteResult = tuple[int, dict[str, str], dict[str, Any]]


def route_request(method: str, raw_path: str, headers: dict[str, str], body_text: str) -> RouteResult:
    """Route a request to the first handler that recognizes the path."""
    path = urlsplit(raw_path).path.rstrip("/") or "/"

    for handler in (handle_system_request,):
        result = handler(method, path, headers)
        if result is not None:
            return result

    auth_result = handle_auth_request(method, path, headers, body_text)
    if auth_result is not None:
        return auth_result

    return 404, {"Content-Type": "application/json; charset=utf-8"}, {
        "message": "Route not found",
        "error": "NOT_FOUND",
        "path": path,
        "success": False,
    }