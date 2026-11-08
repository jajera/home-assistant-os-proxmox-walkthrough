#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
MOCK = ROOT / "mockups"
OUT = ROOT / "captures"

PAGES = ["02-s3-bucket", "03-iam-user"]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            device_scale_factor=2,
        )
        page = context.new_page()
        for name in PAGES:
            html = (MOCK / f"{name}.html").resolve().as_uri()
            page.goto(html)
            page.wait_for_timeout(150)
            out = OUT / f"{name}.png"
            page.screenshot(path=str(out), type="png")
            print(f"wrote {out} ({out.stat().st_size})")
        browser.close()


if __name__ == "__main__":
    main()
