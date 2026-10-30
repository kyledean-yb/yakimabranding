#!/usr/bin/env python3
"""Local preview server that mimics Vercel cleanUrls (/about -> about.html).

Usage: python3 scripts/serve-local.py [port]
"""

import http.server
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CleanUrlHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def translate_path(self, path):
        fs_path = super().translate_path(path)
        if os.path.isfile(fs_path):
            return fs_path
        html_path = fs_path.rstrip("/") + ".html"
        if os.path.isfile(html_path):
            return html_path
        return fs_path

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_head(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        fs_path = super().translate_path(path)
        if not path.endswith("/") and os.path.isfile(fs_path.rstrip("/") + ".html"):
            self.path = path + ".html"
        return super().send_head()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    http.server.ThreadingHTTPServer(("", port), CleanUrlHandler).serve_forever()
