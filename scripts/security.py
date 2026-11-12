#!/usr/bin/env python3
"""Generate/check SRI attributes and response headers using reviewed asset metadata.

Normal updates and Docker builds are offline. --verify-remote checks the recorded
CDN digests without modifying them; new dependency digests require manual review.
"""

import argparse
import base64
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
TAG = re.compile(r"<(script|link)\b[^>]*>", re.IGNORECASE)
DIGEST = re.compile(r"sha384-[A-Za-z0-9+/]{64}\Z")
PINNED = re.compile(
    r"https://(?:cdn\.jsdelivr\.net/npm/|unpkg\.com/)[\w-]+@\d+\.\d+\.\d+/"
    r"|https://cdnjs\.cloudflare\.com/ajax/libs/[\w-]+/\d+\.\d+\.\d+/"
)
# These dedicated image services may be trusted at origin scope. Keep shared
# hosting services (especially raw GitHub content) restricted to reviewed paths.
IMAGE_ORIGINS = {"https://img.shields.io", "https://www.plantuml.com"}
HEADERS = {
    "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Cross-Origin-Opener-Policy": "same-origin",
    "Cross-Origin-Embedder-Policy": "require-corp",
    "Cross-Origin-Resource-Policy": "same-origin",
    "X-XSS-Protection": "0",
    "X-DNS-Prefetch-Control": "off",
    "Permissions-Policy": (
        "camera=(), microphone=(), geolocation=(), display-capture=(), "
        "fullscreen=(), payment=(), usb=(), accelerometer=(), gyroscope=(), "
        "magnetometer=(), clipboard-read=(), clipboard-write=(self)"
    ),
}


def digest(data):
    return "sha384-" + base64.b64encode(hashlib.sha384(data).digest()).decode("ascii")


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.in_script = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if any(name.startswith("on") for name in attrs):
            raise ValueError("Inline event handlers are forbidden")
        if tag == "script":
            if not attrs.get("src"):
                raise ValueError("Inline script blocks are forbidden")
            self.in_script = True
        self.tags.append((tag, attrs))

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False

    def handle_data(self, data):
        if self.in_script and data.strip():
            raise ValueError("Script elements must not contain inline code")


def load_manifest(root):
    manifest = json.loads((root / "security/assets.json").read_text())
    assets = {}
    for asset in manifest["assets"]:
        url = asset["url"]
        if url in assets or asset["kind"] not in {"script", "style"}:
            raise ValueError("Duplicate or invalid asset: " + url)
        parsed = urlsplit(url)
        if parsed.query or parsed.fragment:
            raise ValueError("Manifest assets must not contain queries/fragments: " + url)
        if parsed.scheme:
            if not PINNED.match(url) or not DIGEST.fullmatch(asset.get("integrity", "")):
                raise ValueError("CDN assets need an exact version and SHA-384 digest: " + url)
        elif not url.startswith("/") or url.startswith("//") or asset["kind"] != "script":
            raise ValueError("Invalid local script: " + url)
        assets[url] = asset
    resources = manifest["resources"]
    if set(resources) != {"img-src", "connect-src", "font-src"}:
        raise ValueError("Unexpected resource directives")
    for directive, sources in resources.items():
        if not sources:
            raise ValueError("Empty resource directive: " + directive)
        for source in sources:
            if source == "'self'" or (source == "data:" and directive == "img-src"):
                continue
            parsed = urlsplit(source)
            origin_allowed = directive == "img-src" and source in IMAGE_ORIGINS
            if (parsed.scheme != "https" or not parsed.netloc
                    or (parsed.path in {"", "/"} and not origin_allowed)
                    or any(c in source for c in "*;\n\r\t\"'$ ")):
                raise ValueError("Resources require explicit HTTPS paths or approved image origins: " + source)
    return assets, resources


def render(root):
    assets, resources = load_manifest(root)
    source = (root / "frontend/index.html").read_text()
    page = Page()
    page.feed(source)
    used = set()
    script_hashes = set()
    styles = set()

    def replace(match):
        element = Page()
        element.feed(match.group())
        tag, attrs = element.tags[0]
        kind = "script" if tag == "script" else "style"
        if kind == "style" and attrs.get("rel") != "stylesheet":
            return match.group()
        url = attrs.get("src" if tag == "script" else "href", "")
        parsed = urlsplit(url)
        if parsed.netloc and parsed.scheme != "https":
            raise ValueError("Resources must use explicit HTTPS URLs: " + url)
        if parsed.fragment:
            raise ValueError("Resource URLs must not contain fragments: " + url)
        key = url if parsed.scheme else parsed.path
        if kind == "style" and not parsed.scheme and not parsed.netloc:
            if not key.startswith("/"):
                raise ValueError("Local stylesheets must be root-relative: " + url)
            return match.group()
        if key not in assets or assets[key]["kind"] != kind:
            raise ValueError("Resource is not approved in security/assets.json: " + url)
        if key in used:
            raise ValueError("Duplicate resource element: " + url)
        used.add(key)
        if parsed.scheme:
            integrity = assets[key]["integrity"]
        else:
            file = (root / "frontend" / key.lstrip("/")).resolve()
            file.relative_to((root / "frontend").resolve())
            integrity = digest(file.read_bytes())
        if kind == "script":
            script_hashes.add("'" + integrity + "'")
        else:
            # SRI still pins each linked stylesheet; only CSS source permissions
            # use CDN origins. This never adds those origins to script-src.
            styles.add(parsed.scheme + "://" + parsed.netloc)
        attrs["integrity"] = integrity
        attrs["crossorigin"] = "anonymous"
        attributes = "".join(
            " " + name + ("" if value is None else '="' + html.escape(value, quote=True) + '"')
            for name, value in attrs.items()
        )
        return "<" + tag + attributes + (" />" if tag == "link" else ">")

    index = TAG.sub(replace, source)
    if used != set(assets):
        raise ValueError("Approved assets missing from index.html: " + ", ".join(sorted(set(assets) - used)))
    policy = {
        "default-src": ["'none'"],
        "script-src": sorted(script_hashes),
        "script-src-attr": ["'none'"],
        "style-src": ["'self'", "'unsafe-inline'", *sorted(styles)],
        "font-src": resources["font-src"],
        "connect-src": resources["connect-src"],
        "img-src": resources["img-src"],
        **{name: ["'none'"] for name in (
            "base-uri", "object-src", "frame-src", "frame-ancestors", "form-action",
            "worker-src", "media-src", "manifest-src",
        )},
        "upgrade-insecure-requests": [],
    }
    csp = "; ".join(" ".join([name, *sources]) for name, sources in policy.items()) + ";"
    headers = {"Content-Security-Policy": csp, **HEADERS}
    config = "# Generated by scripts/security.py; review security/assets.json before updating.\n"
    for name, value in headers.items():
        config += 'add_header ' + name + ' "' + value.replace('"', '\\"') + '" always;\n'
    return {root / "frontend/index.html": index, root / "security-headers.conf": config}


def synchronize(root, check=False):
    outputs = render(root)
    stale = [str(path.relative_to(root)) for path, text in outputs.items()
             if not path.exists() or path.read_text() != text]
    if check and stale:
        raise ValueError("Stale security metadata: " + ", ".join(stale)
                         + ". Run python3 scripts/security.py and review the diff.")
    if not check:
        for path, text in outputs.items():
            path.write_text(text)


def verify_remote(root):
    assets, _ = load_manifest(root)
    for url, asset in assets.items():
        if not url.startswith("https://"):
            continue
        request = Request(url, headers={"Origin": "https://fintlabs.no"})
        with urlopen(request, timeout=30) as response:
            if response.url != url:
                raise ValueError("Pinned asset unexpectedly redirects: " + url)
            if digest(response.read()) != asset["integrity"]:
                raise ValueError("CDN integrity mismatch; do not automatically replace the digest: " + url)
            if response.headers.get("Access-Control-Allow-Origin") != "*":
                raise ValueError("CDN no longer permits anonymous CORS: " + url)
        print("Verified", url)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail on drift without modifying files")
    parser.add_argument("--verify-remote", action="store_true", help="also verify pinned CDN bytes/CORS")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        synchronize(args.root.resolve(), check=args.check)
        if args.verify_remote:
            verify_remote(args.root.resolve())
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, str(error) + "\n")
    print("Security metadata is current." if args.check else "Updated SRI attributes and security headers.")


if __name__ == "__main__":
    main()
