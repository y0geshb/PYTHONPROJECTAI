"""Minimal local stub server for offline API automation."""

from __future__ import annotations

import argparse
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.environments import ensure_environment_loaded, get_api_mode, is_mock_mode
from handlers.router import route_request


class MockRequestHandler(BaseHTTPRequestHandler):
    """HTTP handler that serves JSON stub responses from the routing layer."""

    server_version = "SERHMockServer/1.0"

    def do_GET(self) -> None:
        self._dispatch()

    def do_POST(self) -> None:
        self._dispatch()

    def do_PUT(self) -> None:
        self._dispatch()

    def do_PATCH(self) -> None:
        self._dispatch()

    def do_DELETE(self) -> None:
        self._dispatch()

    def log_message(self, format: str, *args: object) -> None:
        return

    def _dispatch(self) -> None:
        body_length = int(self.headers.get("Content-Length", "0"))
        body_text = self.rfile.read(body_length).decode("utf-8") if body_length else ""
        status_code, headers, payload = route_request(
            method=self.command,
            raw_path=self.path,
            headers={key: value for key, value in self.headers.items()},
            body_text=body_text,
        )

        response_bytes = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the local API mock server.")
    parser.add_argument("--host", default=os.getenv("MOCK_SERVER_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("MOCK_SERVER_PORT", "4010")))
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    ensure_environment_loaded()

    if not is_mock_mode():
        print("Warning: API_MODE is not set to mock. The mock server can still run, but tests may target real APIs.")

    server = ThreadingHTTPServer((args.host, args.port), MockRequestHandler)
    print(f"Mock server listening on http://{args.host}:{args.port} (mode={get_api_mode()})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()