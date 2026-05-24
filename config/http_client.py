"""Core HTTP client wrapper for API automation tests.

This module provides a reusable APIClient around requests.Session with
consistent timeout handling, URL composition, SSL verification enforcement,
and request/response logging.
"""

import logging
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class APIClient:
    """Reusable HTTP client for REST APIs.

    Args:
        base_url: Root API URL, for example ``https://api.example.com``.
        headers: Optional default headers applied to the internal session.
    """

    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        if headers:
            self.session.headers.update(headers)

    def _build_url(self, endpoint: str) -> str:
        """Build full URL using base_url + endpoint."""
        normalized_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        return f"{self.base_url}{normalized_endpoint}"

    def log_request_response(self, method: str, url: str, response: requests.Response) -> None:
        """Log request method, URL, response status code, and elapsed time in ms."""
        logger.info(
            "%s %s -> %s (%sms)",
            method.upper(),
            url,
            response.status_code,
            int(response.elapsed.total_seconds() * 1000),
        )

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        """Internal request dispatcher with framework-level defaults."""
        kwargs.setdefault("timeout", 10)
        # Hardcode SSL verification to prevent disabling cert checks.
        kwargs["verify"] = True

        url = self._build_url(endpoint)
        response = self.session.request(method=method.upper(), url=url, **kwargs)
        self.log_request_response(method=method, url=url, response=response)
        return response

    def get(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """Send a GET request and return the raw requests.Response."""
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """Send a POST request and return the raw requests.Response."""
        return self._request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """Send a PUT request and return the raw requests.Response."""
        return self._request("PUT", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """Send a PATCH request and return the raw requests.Response."""
        return self._request("PATCH", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> requests.Response:
        """Send a DELETE request and return the raw requests.Response."""
        return self._request("DELETE", endpoint, **kwargs)
