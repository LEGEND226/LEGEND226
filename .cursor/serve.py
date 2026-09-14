#!/usr/bin/env python3
"""Static dev server for the personal website.

Serves the repository root over HTTP with an explicit UTF-8 charset in the
Content-Type header. Static hosts such as GitHub Pages already send
`text/html; charset=utf-8`, but Python's stock `http.server` omits the charset,
which garbles non-ASCII (e.g. Chinese) content. Declaring it here makes the
local dev server behave like production.
"""
import functools
import http.server
import os

PORT = int(os.environ.get("PORT", "8000"))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".html": "text/html; charset=utf-8",
        ".htm": "text/html; charset=utf-8",
    }


def main() -> None:
    handler = functools.partial(Handler, directory=ROOT)
    server = http.server.ThreadingHTTPServer(("", PORT), handler)
    with server as httpd:
        print(f"Serving {ROOT} on http://0.0.0.0:{PORT} (Ctrl+C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
