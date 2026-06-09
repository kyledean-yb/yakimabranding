#!/usr/bin/env python3
"""Local dev server with clean URL rewrites (mirrors vercel.json behavior)."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
VERCEL = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))


def compile_rule(source: str) -> re.Pattern[str]:
    pattern = source
    pattern = pattern.replace(":path*", r"(?P<path>.*)")
    pattern = pattern.replace(":slug", r"(?P<slug>[^/]+)")
    pattern = "^" + pattern + "$"
    return re.compile(pattern)


@lru_cache(maxsize=1)
def redirect_rules() -> list[tuple[re.Pattern[str], str]]:
    return [(compile_rule(rule["source"]), rule["destination"]) for rule in VERCEL.get("redirects", [])]


@lru_cache(maxsize=1)
def rewrite_rules() -> list[tuple[re.Pattern[str], str]]:
    return [(compile_rule(rule["source"]), rule["destination"]) for rule in VERCEL.get("rewrites", [])]


def apply_template(dest: str, match: re.Match[str]) -> str:
    out = dest
    groups = match.groupdict()
    if "path" in groups and groups["path"] is not None:
        out = out.replace(":path*", groups["path"])
    if "slug" in groups and groups["slug"] is not None:
        out = out.replace(":slug", groups["slug"])
    return out


def resolve_request(path: str) -> tuple[str, bool]:
    """Return (filesystem path, is_redirect)."""
    path = unquote(path.split("?", 1)[0].split("#", 1)[0])
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")

    for pattern, dest in redirect_rules():
        match = pattern.match(path)
        if match:
            return apply_template(dest, match), True

    for pattern, dest in rewrite_rules():
        match = pattern.match(path)
        if match:
            return apply_template(dest, match), False

    if path == "/":
        return "/index.html", False

    rel = path.lstrip("/")
    if (ROOT / rel).is_file():
        return f"/{rel}", False
    if (ROOT / f"{rel}.html").is_file():
        return f"/{rel}.html", False
    return path, False


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        resolved, is_redirect = resolve_request(parsed.path)
        query = f"?{parsed.query}" if parsed.query else ""

        if is_redirect:
            self.send_response(301)
            self.send_header("Location", resolved + query)
            self.end_headers()
            return

        self.path = resolved + query
        super().do_GET()

    def do_HEAD(self) -> None:
        self.do_GET()


def main() -> None:
    port = 8787
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Serving {ROOT} with clean URLs at http://127.0.0.1:{port}/")
    server.serve_forever()


if __name__ == "__main__":
    main()
