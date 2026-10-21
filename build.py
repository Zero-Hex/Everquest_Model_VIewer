#!/usr/bin/env python3
"""Build index.html, the standalone page, from eqg_viewer.html.

eqg_viewer.html is the page body as published on claude.ai (CDN scripts, no
<html>/<head> wrapper). index.html wraps it in a full document and points the
scripts at the copies in vendor/, so it runs from GitHub Pages or a local
folder with no network access.

    python3 build.py
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
CDN = {
    "https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js": "vendor/three.min.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js": "vendor/OrbitControls.js",
    "https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/exporters/GLTFExporter.js": "vendor/GLTFExporter.js",
    "https://cdnjs.cloudflare.com/ajax/libs/pako/2.1.0/pako.min.js": "vendor/pako.min.js",
}


def main():
    src = (HERE / "eqg_viewer.html").read_text(encoding="utf-8")
    for url, local in CDN.items():
        if url not in src:
            raise SystemExit(f"expected {url} in eqg_viewer.html")
        src = src.replace(url, local)
    # Title, metas, fonts and styles go in <head>; the rest is the body.
    split = src.index('<div class="app">')
    head, body = src[:split].strip(), src[split:].strip()
    page = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        f"{head}\n</head>\n<body>\n{body}\n</body>\n</html>\n"
    )
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote index.html ({len(page):,} bytes)")


if __name__ == "__main__":
    main()
