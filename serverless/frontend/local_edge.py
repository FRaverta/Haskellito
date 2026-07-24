"""Local CloudFront/S3/API Gateway simulator for serverless development."""

from __future__ import annotations

import argparse
import mimetypes
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIST = ROOT / "frontend" / "dist"
PUBLIC_DIR = Path(__file__).resolve().parent / "public"
DEFAULT_API_ORIGIN = "http://127.0.0.1:3000"
CHALLENGES_PREFIX = "/api/v2/playground/challenges"


class LocalEdgeHandler(BaseHTTPRequestHandler):
    frontend_dist: Path
    public_dir: Path
    api_origin: str

    def do_HEAD(self) -> None:
        self.route_request(include_body=False)

    def do_GET(self) -> None:
        self.route_request(include_body=True)

    def do_OPTIONS(self) -> None:
        self.proxy_request()

    def do_POST(self) -> None:
        self.proxy_request()

    def do_PUT(self) -> None:
        self.proxy_request()

    def do_PATCH(self) -> None:
        self.proxy_request()

    def do_DELETE(self) -> None:
        self.proxy_request()

    def route_request(self, include_body: bool) -> None:
        parsed = urllib.parse.urlsplit(self.path)
        static_challenge = self.challenge_json_path(parsed)
        if static_challenge is not None:
            self.serve_file(static_challenge, include_body)
            return

        if parsed.path.startswith("/api/"):
            self.proxy_request()
            return

        self.serve_frontend(parsed.path, include_body)

    def challenge_json_path(
        self,
        parsed: urllib.parse.SplitResult,
    ) -> Path | None:
        path = parsed.path.rstrip("/")
        if not path.startswith(CHALLENGES_PREFIX):
            return None
        if "/submit" in path:
            return None

        query = urllib.parse.parse_qs(parsed.query)
        lang = ""
        values = query.get("lang", [])
        if values and values[0] in {"en", "es"}:
            lang = f".{values[0]}"

        if path == CHALLENGES_PREFIX:
            object_path = f"{CHALLENGES_PREFIX}/index{lang}.json"
        else:
            object_path = f"{path}{lang}.json"

        return self.public_dir / object_path.lstrip("/")

    def serve_frontend(self, request_path: str, include_body: bool) -> None:
        relative = request_path.lstrip("/") or "index.html"
        candidate = (self.frontend_dist / relative).resolve()

        if not self.is_relative_to(candidate, self.frontend_dist):
            self.send_error(404)
            return

        if candidate.is_dir():
            candidate = candidate / "index.html"

        if not candidate.exists():
            candidate = self.frontend_dist / "index.html"

        self.serve_file(candidate, include_body)

    def serve_file(self, path: Path, include_body: bool) -> None:
        if not path.exists() or not path.is_file():
            self.send_error(404)
            return

        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        body = path.read_bytes()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

        if include_body:
            self.wfile.write(body)

    def proxy_request(self) -> None:
        target = self.api_origin.rstrip("/") + self.path
        body = self.read_request_body()
        headers = {
            key: value
            for key, value in self.headers.items()
            if key.lower() not in {"host", "content-length"}
        }

        request = urllib.request.Request(
            target,
            data=body,
            headers=headers,
            method=self.command,
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                response_body = response.read()
                self.send_response(response.status)
                self.copy_response_headers(response.headers, len(response_body))
                self.end_headers()
                self.wfile.write(response_body)
        except urllib.error.HTTPError as error:
            error_body = error.read()
            self.send_response(error.code)
            self.copy_response_headers(error.headers, len(error_body))
            self.end_headers()
            self.wfile.write(error_body)
        except urllib.error.URLError as error:
            self.send_error(
                502,
                f"Could not reach API origin {self.api_origin}: {error.reason}",
            )

    def read_request_body(self) -> bytes | None:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return None
        return self.rfile.read(length)

    def copy_response_headers(self, headers, content_length: int) -> None:
        skipped = {"connection", "content-length", "transfer-encoding"}
        for key, value in headers.items():
            if key.lower() not in skipped:
                self.send_header(key, value)
        self.send_header("Content-Length", str(content_length))

    def log_message(self, format: str, *args) -> None:
        print(f"{self.address_string()} - {format % args}")

    @staticmethod
    def is_relative_to(path: Path, parent: Path) -> bool:
        try:
            path.relative_to(parent)
            return True
        except ValueError:
            return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a local CloudFront/S3/API Gateway simulator."
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--api-origin", default=DEFAULT_API_ORIGIN)
    parser.add_argument("--frontend-dist", type=Path, default=FRONTEND_DIST)
    parser.add_argument("--public-dir", type=Path, default=PUBLIC_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    frontend_dist = args.frontend_dist.resolve()
    public_dir = args.public_dir.resolve()

    if not (frontend_dist / "index.html").exists():
        raise SystemExit(
            f"Missing {frontend_dist / 'index.html'}; run `npm run build` in frontend."
        )

    if not public_dir.exists():
        raise SystemExit(
            f"Missing {public_dir}; run `python3 serverless/frontend/export_challenges.py`."
        )

    LocalEdgeHandler.frontend_dist = frontend_dist
    LocalEdgeHandler.public_dir = public_dir
    LocalEdgeHandler.api_origin = args.api_origin

    server = ThreadingHTTPServer((args.host, args.port), LocalEdgeHandler)
    print(f"Local edge serving http://{args.host}:{args.port}")
    print(f"Static frontend: {frontend_dist}")
    print(f"Static challenge JSON: {public_dir}")
    print(f"Dynamic API origin: {args.api_origin}")
    server.serve_forever()


if __name__ == "__main__":
    main()

