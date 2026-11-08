#!/usr/bin/env python3
"""Re-capture HA AWS S3 form without AKIA-looking access key IDs."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "captures" / "_raw"
OUT_PNG = ROOT / "captures" / "04-ha-aws-s3.png"
OUT_JPG = ROOT / "captures" / "04-ha-aws-s3.jpg"
BASE = "http://192.169.32.239"
STORAGE = RAW / "ha-state.json"

# No "AKIA" prefix — Builder Center secret scanners reject those pixels via OCR.
ACCESS_KEY = "••••••••••••EXAMPLE"
SECRET_KEY = "••••••••••••••••••••••••••••••••"
BUCKET = "ha-backups-kiwi-home"
ENDPOINT = "https://s3.ap-southeast-6.amazonaws.com/"
PREFIX = "home-assistant"

REDACT_JS = r"""
() => {
  const map = [[/automate/gi, 'alex'], [/tf-io-ha-backup-prod/gi, 'ha-backups-kiwi-home']];
  const rewrite = (s) => {
    let out = s;
    for (const [re, rep] of map) out = out.replace(re, rep);
    return out;
  };
  const walk = (root) => {
    const tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (tw.nextNode()) nodes.push(tw.currentNode);
    for (const n of nodes) {
      const next = rewrite(n.nodeValue);
      if (next !== n.nodeValue) n.nodeValue = next;
    }
    root.querySelectorAll('*').forEach((el) => {
      if (el.shadowRoot) walk(el.shadowRoot);
    });
  };
  walk(document);
}
"""


def fill_shadow_inputs(page, values):
    return page.evaluate(
        """(vals) => {
      const inputs = [];
      const walk = (root) => {
        root.querySelectorAll('input').forEach((i) => {
          if (i.type === 'hidden' || i.type === 'checkbox') return;
          const ph = (i.placeholder || '').toLowerCase();
          const al = (i.getAttribute('aria-label') || '').toLowerCase();
          if (ph.includes('search') || al.includes('search')) return;
          inputs.push(i);
        });
        root.querySelectorAll('*').forEach((el) => {
          if (el.shadowRoot) walk(el.shadowRoot);
        });
      };
      walk(document);
      let n = 0;
      for (const inp of inputs) {
        if (n >= vals.length) break;
        inp.focus();
        const setter = Object.getOwnPropertyDescriptor(
          window.HTMLInputElement.prototype, 'value'
        ).set;
        setter.call(inp, vals[n]);
        inp.dispatchEvent(new Event('input', { bubbles: true }));
        inp.dispatchEvent(new Event('change', { bubbles: true }));
        n++;
      }
      return { found: inputs.length, filled: n };
    }""",
        values,
    )


def main():
    if not STORAGE.exists():
        raise SystemExit(f"missing HA session {STORAGE}; run capture_ha.py first")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1200, "height": 675},
            device_scale_factor=1,
            storage_state=str(STORAGE),
        )
        page = context.new_page()
        page.goto(f"{BASE}/config/integrations/dashboard", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        page.get_by_role("button", name="Add integration").click()
        page.wait_for_timeout(1200)
        page.locator("dialog-add-integration input").first.fill("AWS S3")
        page.wait_for_timeout(900)
        page.locator("dialog-add-integration").get_by_text("Amazon", exact=True).click(
            force=True
        )
        page.wait_for_timeout(1000)
        page.locator("dialog-add-integration").get_by_text("AWS S3", exact=True).click(
            force=True
        )
        page.wait_for_timeout(1800)

        vals = [ACCESS_KEY, SECRET_KEY, BUCKET, ENDPOINT, PREFIX]
        print("fill", fill_shadow_inputs(page, vals))
        page.wait_for_timeout(400)
        page.evaluate(REDACT_JS)
        page.wait_for_timeout(200)
        page.screenshot(path=str(OUT_PNG), type="png")
        browser.close()

    im = Image.open(OUT_PNG).convert("RGB")
    # Hard-crop / ensure exact Builder Center-friendly size
    if im.size != (1200, 675):
        im = im.resize((1200, 675), Image.Resampling.LANCZOS)
    im.save(OUT_PNG, format="PNG", optimize=True)
    im.save(OUT_JPG, format="JPEG", quality=88, optimize=True)

    # Pixel OCR-ish sanity: raw PNG must not contain ASCII AKIA
    if b"AKIA" in OUT_PNG.read_bytes():
        raise SystemExit("AKIA still present in PNG bytes")

    print(f"png {OUT_PNG} {OUT_PNG.stat().st_size} {im.size}")
    print(f"jpg {OUT_JPG} {OUT_JPG.stat().st_size}")


if __name__ == "__main__":
    main()
