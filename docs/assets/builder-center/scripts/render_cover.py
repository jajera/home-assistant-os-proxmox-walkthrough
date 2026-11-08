#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
MOCK = ROOT / "mockups"
OUT = ROOT / "captures"

JOBS = [
    ("00-cover.html", "00-cover.png", 1200, 675),
    ("00-flow.html", "00-flow.png", 1200, 420),
]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for html_name, png_name, w, h in JOBS:
            page = browser.new_context(
                viewport={"width": w, "height": h},
                device_scale_factor=2,
            ).new_page()
            page.goto((MOCK / html_name).resolve().as_uri())
            page.wait_for_timeout(300)
            out = OUT / png_name
            page.screenshot(path=str(out), type="png")
            print(out, out.stat().st_size)
            page.context.close()
        browser.close()


if __name__ == "__main__":
    main()
