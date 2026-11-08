#!/usr/bin/env python3
"""Capture live HA UI, redact lab names, write final PNGs."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "captures" / "_raw"
OUT = ROOT / "captures"
BASE = "http://192.169.32.239"
STORAGE = RAW / "ha-state.json"

REDACT_JS = r"""
() => {
  const map = [
    [/automate/gi, 'alex'],
    [/tf-io-ha-backup-prod/gi, 'ha-backups-kiwi-home'],
    [/192\.169\.32\.239/g, 'homeassistant.local'],
  ];
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


def redact(page):
    page.evaluate(REDACT_JS)
    page.wait_for_timeout(200)


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
    RAW.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            device_scale_factor=2,
            storage_state=str(STORAGE),
        )
        page = context.new_page()

        # 01 — Overview
        page.goto(f"{BASE}/home/overview", wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        redact(page)
        page.screenshot(path=str(OUT / "01-ha-home.png"))
        print("01 ok")

        # 04 — Add AWS S3 form with fictitious values
        page.goto(f"{BASE}/config/integrations/dashboard", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        page.get_by_role("button", name="Add integration").click()
        page.wait_for_timeout(1200)
        page.locator("dialog-add-integration input").first.fill("AWS S3")
        page.wait_for_timeout(1000)
        page.locator("dialog-add-integration").get_by_text("Amazon", exact=True).click(
            force=True
        )
        page.wait_for_timeout(1200)
        page.locator("dialog-add-integration").get_by_text("AWS S3", exact=True).click(
            force=True
        )
        page.wait_for_timeout(2000)
        # Never use AKIA… — Builder Center OCR secret scanners reject those uploads.
        vals = [
            "••••••••••••EXAMPLE",
            "••••••••••••••••••••••••••••••••",
            "ha-backups-kiwi-home",
            "https://s3.ap-southeast-6.amazonaws.com/",
            "home-assistant",
        ]
        print("fill", fill_shadow_inputs(page, vals))
        # Prefer labeled fills when available
        for label, val in [
            ("Access key ID", vals[0]),
            ("Secret access key", vals[1]),
            ("Bucket name", vals[2]),
            ("Endpoint URL", vals[3]),
            ("Prefix", vals[4]),
        ]:
            try:
                page.get_by_label(label, exact=False).fill(val, timeout=1500)
            except Exception as e:
                print("label skip", label, type(e).__name__)
        page.wait_for_timeout(400)
        redact(page)
        page.screenshot(path=str(OUT / "04-ha-aws-s3.png"))
        page.screenshot(path=str(RAW / "04-ha-aws-s3.png"))
        print("04 ok")
        # dismiss without submitting
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        page.keyboard.press("Escape")

        # 05 — Backup overview (shows 2 locations)
        page.goto(f"{BASE}/config/backup/overview", wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        redact(page)
        page.screenshot(path=str(OUT / "05-ha-backups.png"))
        print("05 ok")

        # Also grab settings if Locations visible after deep scroll via click
        page.goto(f"{BASE}/config/backup/settings", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        # Click through to expand locations if present
        text = page.evaluate("() => document.body.innerText")
        print("settings snippet:", text[800:1600] if len(text) > 800 else text)
        for _ in range(12):
            page.mouse.wheel(0, 900)
            page.wait_for_timeout(250)
        redact(page)
        page.screenshot(path=str(RAW / "05-settings-bottom.png"))

        # 06 — Backup list with local + S3 icons
        page.goto(
            f"{BASE}/config/backup/backups?sort=date&direction=desc&group=type",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(4000)
        redact(page)
        page.screenshot(path=str(OUT / "06-backup-done.png"))
        print("06 ok")

        # Bonus: redacted AWS S3 integration card
        page.goto(
            f"{BASE}/config/integrations/integration/aws_s3",
            wait_until="domcontentloaded",
        )
        page.wait_for_timeout(3500)
        redact(page)
        page.screenshot(path=str(RAW / "04-aws-s3-configured.png"))

        browser.close()
    print("done")


if __name__ == "__main__":
    main()
