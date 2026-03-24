#!/usr/bin/env python3
"""Show Me Card QA Audit — Playwright-based automated quality checker.

Loads every Show Me card in a headless browser and runs 15 checks across
four domains: canvas rendering, content accuracy, interaction/UX, and
visual consistency.  Results are written to a JSON report.

Usage:
    python tools/showme_card_audit.py                         # full audit
    python tools/showme_card_audit.py --cards extrude,inset   # specific cards
    python tools/showme_card_audit.py --screenshots           # capture tab screenshots
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: playwright is not installed. Run: pip install playwright && python -m playwright install chromium")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
SHOWME_DIR = ROOT / "course-site" / "assets" / "showme"
REPORT_DIR = ROOT / "claudedocs"
SCREENSHOT_DIR = REPORT_DIR / "screenshots"

TAB_IDS = ["concept", "visual", "usage", "quiz"]


def parse_registry() -> dict[str, dict]:
    """Parse _registry.js to get card IDs and metadata."""
    registry_path = SHOWME_DIR / "_registry.js"
    text = registry_path.read_text(encoding="utf-8")

    cards: dict[str, dict] = {}
    for match in re.finditer(
        r'"([^"]+)"\s*:\s*\{([^}]+)\}', text
    ):
        card_id = match.group(1)
        body = match.group(2)

        label_m = re.search(r'label:\s*"([^"]+)"', body)
        week_m = re.search(r'week:\s*(\d+)', body)
        icon_m = re.search(r'icon:\s*"([^"]+)"', body)

        cards[card_id] = {
            "label": label_m.group(1) if label_m else card_id,
            "week": int(week_m.group(1)) if week_m else 0,
            "icon": icon_m.group(1) if icon_m else "",
        }
    return cards


def check_canvas_non_empty(page, canvas_id: str) -> bool:
    """Check if a canvas element has any drawn pixels."""
    return page.evaluate(
        """(canvasId) => {
            const c = document.getElementById(canvasId);
            if (!c) return false;
            const ctx = c.getContext('2d');
            const d = ctx.getImageData(0, 0, c.width, c.height).data;
            for (let i = 3; i < d.length; i += 4) {
                if (d[i] > 0) return true;
            }
            return false;
        }""",
        canvas_id,
    )


def get_canvas_hash(page, canvas_id: str) -> str:
    """Get a simple hash of canvas pixel data to detect changes."""
    return page.evaluate(
        """(canvasId) => {
            const c = document.getElementById(canvasId);
            if (!c) return '';
            try { return c.toDataURL().slice(-80); }
            catch(e) { return ''; }
        }""",
        canvas_id,
    )


def audit_card(page, card_id: str, *, screenshots: bool = False) -> dict:
    """Run all 15 checks on a single card. Returns check results dict."""
    card_path = SHOWME_DIR / f"{card_id}.html"
    url = card_path.as_uri()
    checks: dict[str, str] = {}
    errors: list[str] = []
    console_errors: list[str] = []

    # Collect console errors
    def on_console(msg):
        if msg.type in ("error", "warning"):
            console_errors.append(f"[{msg.type}] {msg.text}")

    page.on("console", on_console)

    # ── A1: Page load ──
    try:
        page.goto(url, wait_until="load", timeout=10000)
        page.wait_for_timeout(500)  # let canvas scripts run
        checks["A1_page_load"] = "pass"
    except Exception as exc:
        checks["A1_page_load"] = "fail"
        errors.append(f"[fail] A1: Page load failed: {exc}")
        page.remove_listener("console", on_console)
        return _build_result(card_id, checks, errors)

    # Switch to visual tab first — canvases and scenario buttons live there
    visual_tab = page.locator('[data-tab="visual"]')
    if visual_tab.count() > 0:
        visual_tab.click()
        page.wait_for_timeout(500)  # let canvas scripts render

    # ── A2: demoCanvas exists and non-empty ──
    has_demo = page.locator("#demoCanvas").count() > 0
    if has_demo:
        non_empty = check_canvas_non_empty(page, "demoCanvas")
        checks["A2_demo_canvas"] = "pass" if non_empty else "warn"
        if not non_empty:
            errors.append("[warn] A2: demoCanvas exists but appears empty")
    else:
        checks["A2_demo_canvas"] = "skip"

    # ── A3: before/after canvases ──
    before_canvases = page.locator("canvas[id*='before'], canvas[id*='Before']")
    after_canvases = page.locator("canvas[id*='after'], canvas[id*='After']")
    ba_count = before_canvases.count() + after_canvases.count()
    if ba_count > 0:
        all_rendered = True
        for i in range(before_canvases.count()):
            cid = before_canvases.nth(i).get_attribute("id")
            if cid and not check_canvas_non_empty(page, cid):
                all_rendered = False
                errors.append(f"[warn] A3: Canvas '{cid}' appears empty")
        for i in range(after_canvases.count()):
            cid = after_canvases.nth(i).get_attribute("id")
            if cid and not check_canvas_non_empty(page, cid):
                all_rendered = False
                errors.append(f"[warn] A3: Canvas '{cid}' appears empty")
        checks["A3_before_after"] = "pass" if all_rendered else "warn"
    else:
        checks["A3_before_after"] = "skip"

    # ── A4: Scenario button changes ANY canvas ──
    # Scenario buttons may update demoCanvas OR before/after canvases.
    # Collect hashes from all canvases, click scenario, compare.
    scenario_btns = page.locator(".scenario-btn")
    total_btns = scenario_btns.count()
    all_canvases = page.locator("canvas")
    canvas_count = all_canvases.count()
    if total_btns >= 2 and canvas_count > 0:
        # Snapshot all canvas hashes before click
        hashes_before = page.evaluate(
            """() => {
                const result = {};
                document.querySelectorAll('canvas').forEach(c => {
                    if (c.id) {
                        try { result[c.id] = c.toDataURL().slice(-80); }
                        catch(e) { result[c.id] = ''; }
                    }
                });
                return result;
            }"""
        )
        try:
            clicked = page.evaluate(
                """() => {
                    const btns = document.querySelectorAll('.scenario-btn');
                    for (const btn of btns) {
                        if (!btn.classList.contains('active') && !btn.classList.contains('is-active')) {
                            btn.click();
                            return btn.textContent.trim();
                        }
                    }
                    return null;
                }"""
            )
            if clicked:
                page.wait_for_timeout(400)
                hashes_after = page.evaluate(
                    """() => {
                        const result = {};
                        document.querySelectorAll('canvas').forEach(c => {
                            if (c.id) {
                                try { result[c.id] = c.toDataURL().slice(-80); }
                                catch(e) { result[c.id] = ''; }
                            }
                        });
                        return result;
                    }"""
                )
                any_changed = any(
                    hashes_before.get(cid) != hashes_after.get(cid)
                    for cid in hashes_after
                )
                checks["A4_scenario_change"] = "pass" if any_changed else "warn"
                if not any_changed:
                    errors.append(f"[warn] A4: Scenario '{clicked}' did not change any canvas")
            else:
                checks["A4_scenario_change"] = "skip"
        except Exception as exc:
            checks["A4_scenario_change"] = "warn"
            errors.append(f"[warn] A4: Scenario click error: {exc}")
    else:
        checks["A4_scenario_change"] = "skip"

    # ── B1: All 4 tabs exist ──
    tab_buttons = page.locator("[data-tab]")
    tab_count = tab_buttons.count()
    checks["B1_four_tabs"] = "pass" if tab_count >= 4 else "fail"
    if tab_count < 4:
        errors.append(f"[fail] B1: Expected 4 tabs, found {tab_count}")

    # ── B2: Each panel has text content ──
    panels_empty = []
    for tid in TAB_IDS:
        panel = page.locator(f"#panel-{tid}")
        if panel.count() > 0:
            text = (panel.text_content() or "").strip()
            if len(text) < 10:
                panels_empty.append(tid)
    checks["B2_panel_content"] = "pass" if not panels_empty else "fail"
    if panels_empty:
        errors.append(f"[fail] B2: Empty panels: {', '.join(panels_empty)}")

    # ── B3: Keyboard shortcuts ──
    kbd_count = page.locator(".kbd").count()
    shortcut_list = page.locator(".shortcut-list, .shortcut-row").count()
    checks["B3_kbd_shortcuts"] = "pass" if kbd_count > 0 or shortcut_list > 0 else "info"

    # ── B4: External links format ──
    doc_links = page.locator(".doc-ref a")
    link_count = doc_links.count()
    bad_links = []
    for i in range(link_count):
        href = doc_links.nth(i).get_attribute("href") or ""
        if href and not href.startswith("https://docs.blender.org"):
            bad_links.append(href)
    if link_count > 0:
        checks["B4_external_links"] = "pass" if not bad_links else "warn"
        if bad_links:
            errors.append(f"[warn] B4: Non-Blender doc links: {bad_links}")
    else:
        checks["B4_external_links"] = "skip"

    # ── C1: Tab switching ──
    tab_switch_ok = True
    for tid in TAB_IDS:
        tab_btn = page.locator(f'[data-tab="{tid}"]')
        if tab_btn.count() == 0:
            continue
        try:
            tab_btn.click()
            page.wait_for_timeout(200)
            panel = page.locator(f"#panel-{tid}")
            if panel.count() > 0 and not panel.is_visible():
                tab_switch_ok = False
                errors.append(f"[fail] C1: Tab '{tid}' click did not show panel")
        except Exception as exc:
            tab_switch_ok = False
            errors.append(f"[fail] C1: Tab '{tid}' click error: {exc}")
    checks["C1_tab_switching"] = "pass" if tab_switch_ok else "fail"

    # ── C2: Quiz feedback ──
    # Switch to quiz tab
    quiz_tab = page.locator('[data-tab="quiz"]')
    if quiz_tab.count() > 0:
        quiz_tab.click()
        page.wait_for_timeout(300)

    quiz_options = page.locator(".quiz-option")
    if quiz_options.count() > 0:
        try:
            quiz_options.first.click()
            page.wait_for_timeout(300)
            feedback = page.locator(".quiz-feedback")
            has_feedback = feedback.count() > 0 and (
                "show" in (feedback.first.get_attribute("class") or "")
                or feedback.first.is_visible()
            )
            # Also check for correct/wrong class on option
            option_class = quiz_options.first.get_attribute("class") or ""
            has_state = "correct" in option_class or "wrong" in option_class
            checks["C2_quiz_feedback"] = "pass" if (has_feedback or has_state) else "warn"
            if not has_feedback and not has_state:
                errors.append("[warn] C2: Quiz option click did not show feedback")
        except Exception as exc:
            checks["C2_quiz_feedback"] = "warn"
            errors.append(f"[warn] C2: Quiz interaction error: {exc}")
    else:
        checks["C2_quiz_feedback"] = "skip"

    # ── C3: Slider/input response ──
    # Ensure visual tab is active for controls
    vis_tab = page.locator('[data-tab="visual"]')
    if vis_tab.count() > 0:
        vis_tab.click()
        page.wait_for_timeout(200)

    range_inputs = page.locator('input[type="range"]')
    if range_inputs.count() > 0:
        try:
            first_range = range_inputs.first
            range_id = first_range.get_attribute("id") or ""
            # Find associated label (common pattern: element with id like {base}Label)
            base = re.sub(r'(Range|Slider)$', '', range_id)
            label_sel = f"#{base}Label"
            label_el = page.locator(label_sel)

            if label_el.count() > 0:
                old_text = (label_el.text_content() or "").strip()
                # Change the range value
                first_range.evaluate(
                    """(el) => {
                        const mid = (parseFloat(el.min) + parseFloat(el.max)) / 2;
                        el.value = mid;
                        el.dispatchEvent(new Event('input', {bubbles: true}));
                    }"""
                )
                page.wait_for_timeout(200)
                new_text = (label_el.text_content() or "").strip()
                checks["C3_slider_response"] = "pass" if old_text != new_text else "warn"
                if old_text == new_text:
                    errors.append(f"[warn] C3: Slider '{range_id}' did not update label")
            else:
                checks["C3_slider_response"] = "skip"
        except Exception as exc:
            checks["C3_slider_response"] = "warn"
            errors.append(f"[warn] C3: Slider test error: {exc}")
    else:
        checks["C3_slider_response"] = "skip"

    # ── C4: Console errors ──
    real_errors = [e for e in console_errors if "[error]" in e.lower() or "uncaught" in e.lower()]
    warnings = [e for e in console_errors if e not in real_errors]
    if real_errors:
        checks["C4_console_errors"] = "fail"
        for e in real_errors:
            errors.append(f"[fail] C4: {e}")
    elif warnings:
        checks["C4_console_errors"] = "warn"
        for w in warnings[:3]:  # cap at 3
            errors.append(f"[warn] C4: {w}")
    else:
        checks["C4_console_errors"] = "pass"

    # ── D1: CSS variable usage (detect hardcoded hex) ──
    style_blocks = page.locator("style").all_text_contents()
    hardcoded_hex = set()
    for block in style_blocks:
        # Skip :root variable definitions
        root_m = re.search(r':root\s*\{[^}]+\}', block, re.DOTALL)
        rest = block
        if root_m:
            rest = block[:root_m.start()] + block[root_m.end():]
        # Find hex colors outside var() and :root
        for hex_match in re.finditer(r'(?<!--)#([0-9a-fA-F]{3,8})\b', rest):
            val = hex_match.group(0)
            # Ignore very common ones that might be intentional
            if val.lower() not in ("#fff", "#000", "#ffffff", "#000000"):
                hardcoded_hex.add(val)
    if hardcoded_hex:
        checks["D1_css_variables"] = "warn"
        sample = list(hardcoded_hex)[:5]
        errors.append(f"[warn] D1: Hardcoded hex colors: {sample}")
    else:
        checks["D1_css_variables"] = "pass"

    # ── D2: Screenshots (optional) ──
    if screenshots:
        ss_dir = SCREENSHOT_DIR / card_id
        ss_dir.mkdir(parents=True, exist_ok=True)
        for tid in TAB_IDS:
            tab_btn = page.locator(f'[data-tab="{tid}"]')
            if tab_btn.count() > 0:
                tab_btn.click()
                page.wait_for_timeout(300)
                page.screenshot(path=str(ss_dir / f"tab-{tid}.png"), full_page=True)
        checks["D2_screenshots"] = "pass"
    else:
        checks["D2_screenshots"] = "skip"

    # ── D3: Viewport overflow ──
    overflow = page.evaluate(
        """() => {
            return document.documentElement.scrollWidth > document.documentElement.clientWidth;
        }"""
    )
    checks["D3_overflow"] = "warn" if overflow else "pass"
    if overflow:
        errors.append("[warn] D3: Horizontal viewport overflow detected")

    page.remove_listener("console", on_console)
    return _build_result(card_id, checks, errors)


def _build_result(card_id: str, checks: dict, errors: list) -> dict:
    """Determine overall status from individual checks."""
    has_fail = any(v == "fail" for v in checks.values())
    has_warn = any(v == "warn" for v in checks.values())
    if has_fail:
        status = "fail"
    elif has_warn:
        status = "warn"
    else:
        status = "pass"
    return {
        "id": card_id,
        "status": status,
        "checks": checks,
        "errors": errors,
    }


def run_audit(card_filter: list[str] | None = None, screenshots: bool = False) -> dict:
    """Run the full audit and return report data."""
    registry = parse_registry()

    if card_filter:
        registry = {k: v for k, v in registry.items() if k in card_filter}

    # Verify card files exist
    missing = [cid for cid in registry if not (SHOWME_DIR / f"{cid}.html").exists()]
    if missing:
        print(f"WARNING: Missing card files: {missing}")
        for m in missing:
            del registry[m]

    print(f"Auditing {len(registry)} cards...")

    results: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1500, "height": 1100},
            color_scheme="dark",
            device_scale_factor=1,
        )

        for i, (card_id, meta) in enumerate(registry.items()):
            page = context.new_page()
            print(f"  [{i+1}/{len(registry)}] {card_id}...", end=" ", flush=True)

            t0 = time.time()
            result = audit_card(page, card_id, screenshots=screenshots)
            elapsed = time.time() - t0

            result["label"] = meta["label"]
            result["week"] = meta["week"]
            result["icon"] = meta["icon"]

            status_icon = {"pass": "OK", "warn": "WARN", "fail": "FAIL"}[result["status"]]
            print(f"{status_icon} ({elapsed:.1f}s)")

            results.append(result)
            page.close()

        context.close()
        browser.close()

    # Build summary
    pass_count = sum(1 for r in results if r["status"] == "pass")
    warn_count = sum(1 for r in results if r["status"] == "warn")
    fail_count = sum(1 for r in results if r["status"] == "fail")

    report = {
        "audit_date": datetime.now(timezone.utc).isoformat(),
        "total_cards": len(results),
        "summary": {"pass": pass_count, "warn": warn_count, "fail": fail_count},
        "cards": results,
    }

    return report


def main():
    parser = argparse.ArgumentParser(description="Show Me Card QA Audit")
    parser.add_argument("--cards", type=str, default=None, help="Comma-separated card IDs to audit")
    parser.add_argument("--screenshots", action="store_true", help="Capture tab screenshots")
    parser.add_argument("--output", type=str, default=None, help="Output JSON path")
    args = parser.parse_args()

    card_filter = args.cards.split(",") if args.cards else None
    report = run_audit(card_filter=card_filter, screenshots=args.screenshots)

    # Write report
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = Path(args.output) if args.output else REPORT_DIR / "showme-audit-report.json"
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # Print summary
    s = report["summary"]
    print(f"\n{'='*50}")
    print(f"Audit complete: {report['total_cards']} cards")
    print(f"  PASS: {s['pass']}  |  WARN: {s['warn']}  |  FAIL: {s['fail']}")
    print(f"Report: {output_path}")

    if s["fail"] > 0:
        print(f"\nFailed cards:")
        for card in report["cards"]:
            if card["status"] == "fail":
                print(f"  - {card['id']}: {', '.join(card['errors'][:3])}")

    if s["warn"] > 0:
        print(f"\nWarning cards:")
        for card in report["cards"]:
            if card["status"] == "warn":
                print(f"  - {card['id']}: {', '.join(card['errors'][:2])}")


if __name__ == "__main__":
    main()
