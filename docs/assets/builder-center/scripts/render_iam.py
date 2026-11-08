#!/usr/bin/env python3
"""Re-render IAM still for Builder Center upload (no AKIA pattern, 1200x675)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "mockups" / "03-iam-user.html").resolve().as_uri()
OUT_PNG = ROOT / "captures" / "03-iam-user.png"
OUT_JPG = ROOT / "captures" / "03-iam-user.jpg"


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_context(
            viewport={"width": 1200, "height": 675},
            device_scale_factor=1,
        ).new_page()
        page.goto(HTML)
        page.wait_for_timeout(250)
        page.screenshot(path=str(OUT_PNG), type="png")
        browser.close()

    im = Image.open(OUT_PNG).convert("RGB")
    im.save(OUT_PNG, format="PNG", optimize=True)
    im.save(OUT_JPG, format="JPEG", quality=88, optimize=True)

    # Sanity: reject if access-key-looking token slipped in
    raw = OUT_PNG.read_bytes()
    if b"AKIA" in raw:
        raise SystemExit("AKIA still present in PNG bytes — abort")

    print(f"png {OUT_PNG} {OUT_PNG.stat().st_size} {im.size}")
    print(f"jpg {OUT_JPG} {OUT_JPG.stat().st_size}")


if __name__ == "__main__":
    main()
