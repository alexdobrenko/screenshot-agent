#!/usr/bin/env python3
"""
screenshot.py - Take screenshots of web pages or local HTML files using Playwright.
Usage: python3 screenshot.py URL [OPTIONS]
"""

import argparse
import os
import sys
import time
import tempfile
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Screenshot a URL or local HTML file")
    parser.add_argument("url", help="URL or local file path to screenshot")
    parser.add_argument("-o", "--output", default="screenshot.png", help="Output file path (default: screenshot.png)")
    parser.add_argument("-w", "--width", type=int, default=1280, help="Viewport width (default: 1280)")
    parser.add_argument("--height", type=int, default=800, help="Viewport height (default: 800)")
    parser.add_argument("--full", action="store_true", help="Capture full page")
    parser.add_argument("--retina", action="store_true", help="2x device scale factor")
    parser.add_argument("--wait", type=float, default=2, help="Seconds to wait after load (default: 2)")
    parser.add_argument("--header", nargs=2, type=int, metavar=("W", "H"), help="Crop top of page and resize to WxH")
    parser.add_argument("--dark", action="store_true", help="Use dark color scheme preference")
    return parser.parse_args()


def resolve_url(url):
    # If it looks like a local path, convert to file:// URL
    if url.startswith("/") or url.startswith("./") or url.startswith("~/"):
        path = Path(url).expanduser().resolve()
        return f"file://{path}"
    if not url.startswith("http://") and not url.startswith("https://") and not url.startswith("file://"):
        # Bare path without leading slash - try resolving as file
        path = Path(url).resolve()
        if path.exists():
            return f"file://{path}"
    return url


def main():
    args = parse_args()
    url = resolve_url(args.url)
    output = Path(args.output)
    scale = 2 if args.retina else 1

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": args.width, "height": args.height},
            device_scale_factor=scale,
            color_scheme="dark" if args.dark else "light",
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle")

        if args.wait > 0:
            time.sleep(args.wait)

        if args.header:
            target_w, target_h = args.header
            # Take full page screenshot to a temp file, then crop and resize
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp_path = tmp.name
            page.screenshot(path=tmp_path, full_page=True)
            browser.close()

            from PIL import Image
            img = Image.open(tmp_path)
            os.unlink(tmp_path)
            # Crop from the top: width=full, height=scaled target_h
            crop_h = min(target_h, img.height)
            cropped = img.crop((0, 0, img.width, crop_h))
            resized = cropped.resize((target_w, target_h), Image.LANCZOS)
            resized.save(output)
            final_w, final_h = target_w, target_h
        else:
            page.screenshot(path=str(output), full_page=args.full)
            browser.close()

            from PIL import Image
            img = Image.open(output)
            final_w, final_h = img.size

    size_kb = output.stat().st_size // 1024
    print(f"Screenshot saved to {output} ({final_w}x{final_h}, {size_kb}KB)")


if __name__ == "__main__":
    main()
