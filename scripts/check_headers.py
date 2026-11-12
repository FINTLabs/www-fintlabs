#!/usr/bin/env python3
"""Check the real Nginx response headers (or a deployed public hostname)."""

import argparse
import re
from urllib.error import HTTPError
from urllib.request import urlopen

from security import HEADERS, ROOT


def check(base_url):
    config = (ROOT / "security-headers.conf").read_text()
    csp = re.search(r'add_header Content-Security-Policy "([^"]+)" always;', config).group(1)
    expected = {"Content-Security-Policy": csp, **HEADERS}
    cases = [
        ("/", 200, "text/html"),
        ("/index.html", 200, "text/html"),
        ("/getting-started/index.md", 200, None),
        ("/js/docsify-config.js", 200, "javascript"),
        ("/css/theme-custom.css", 200, "text/css"),
        ("/_media/novari-logo.svg", 200, "image/svg+xml"),
        ("/__missing_security_check__.md", 404, None),
        ("/__missing_security_check__.js", 404, None),
    ]
    for path, status, content_type in cases:
        try:
            response = urlopen(base_url.rstrip("/") + path, timeout=30)
        except HTTPError as error:
            response = error
        with response:
            assert response.status == status, (path, response.status)
            for name, value in expected.items():
                assert response.headers.get_all(name) == [value], (path, name, response.headers.get_all(name))
            if content_type:
                assert content_type in response.headers.get("Content-Type", ""), (path, "Content-Type")
            assert not re.search(r"nginx/\d", response.headers.get("Server", "")), (path, "Server version")
            if path.endswith((".html", ".md", ".js", ".css")) and status == 200:
                assert response.headers.get("Cache-Control") == "no-cache", (path, "Cache-Control")
            print("Verified", status, path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url", help="Nginx base URL, e.g. http://127.0.0.1:8765")
    check(parser.parse_args().base_url)
