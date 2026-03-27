from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import unittest
from pathlib import Path

try:
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover - optional local dependency
    PlaywrightError = None
    sync_playwright = None


ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = ROOT / "tools"

if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from playwright_test_support import PlaywrightFailureArtifactsMixin


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class PublicPageStyleE2ETest(PlaywrightFailureArtifactsMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if sync_playwright is None:
            raise unittest.SkipTest("playwright is not installed")

        cls.port = _find_free_port()
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        cls.proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "http.server",
                str(cls.port),
                "--bind",
                "127.0.0.1",
            ],
            cwd=ROOT / "course-site",
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        cls.base_url = f"http://127.0.0.1:{cls.port}"
        cls._wait_for_server()

        try:
            cls.playwright = sync_playwright().start()
            cls.browser = cls.playwright.chromium.launch(headless=True)
        except PlaywrightError as exc:
            cls._terminate_server()
            raise unittest.SkipTest(
                f"playwright browser launch failed: {exc}. "
                "Run `python3 -m playwright install chromium`."
            )

    @classmethod
    def tearDownClass(cls) -> None:
        if getattr(cls, "browser", None) is not None:
            cls.browser.close()
        if getattr(cls, "playwright", None) is not None:
            cls.playwright.stop()
        cls._terminate_server()

    @classmethod
    def _terminate_server(cls) -> None:
        if getattr(cls, "proc", None) is None:
            return
        cls.proc.terminate()
        try:
            cls.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:  # pragma: no cover - defensive cleanup
            cls.proc.kill()
            cls.proc.wait(timeout=5)

    @classmethod
    def _wait_for_server(cls) -> None:
        last_error = "server did not start"
        for _ in range(80):
            try:
                with socket.create_connection(("127.0.0.1", cls.port), timeout=0.2):
                    return
            except OSError as exc:  # pragma: no cover - startup polling
                last_error = str(exc)
                time.sleep(0.1)

        output = ""
        if cls.proc.stdout is not None:
            output = cls.proc.stdout.read()
        raise RuntimeError(f"public page server failed to start: {last_error}\n{output}")

    def setUp(self) -> None:
        self.context = None
        self.page = None
        self._artifact_suffix = ""
        self._playwright_artifacts_captured = False

    def tearDown(self) -> None:
        if self._test_failed() and not self._playwright_artifacts_captured:
            self._capture_playwright_artifacts(self.page, suffix=self._artifact_suffix)
        self._close_context()

    def _close_context(self) -> None:
        if getattr(self, "context", None) is None:
            return
        self.context.close()
        self.context = None
        self.page = None

    def _new_page(self):
        self._close_context()
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        return self.page

    def _read_style(self, page, selector: str) -> dict[str, str | None]:
        page.locator(selector).first.wait_for(state="visible")
        return page.locator(selector).first.evaluate(
            """el => {
                const style = getComputedStyle(el);
                return {
                  ariaCurrent: el.getAttribute('aria-current'),
                  className: el.className,
                  color: style.color,
                  backgroundColor: style.backgroundColor,
                  backgroundImage: style.backgroundImage,
                  boxShadow: style.boxShadow,
                  borderTopWidth: style.borderTopWidth,
                  borderRightWidth: style.borderRightWidth,
                  borderBottomWidth: style.borderBottomWidth,
                  borderLeftWidth: style.borderLeftWidth,
                  borderTopColor: style.borderTopColor,
                  fontWeight: style.fontWeight
                };
            }"""
        )

    def _assert_text_priority_active(
        self,
        active_style: dict[str, str | None],
        inactive_style: dict[str, str | None],
        *,
        expect_aria_current: bool = True,
    ) -> None:
        if expect_aria_current:
            self.assertEqual(active_style["ariaCurrent"], "page")
        self.assertEqual(active_style["backgroundImage"], "none")
        self.assertIn(active_style["backgroundColor"], {"rgba(0, 0, 0, 0)", "transparent"})
        self.assertEqual(active_style["boxShadow"], "none")
        self.assertEqual(active_style["borderTopWidth"], "0px")
        self.assertEqual(active_style["borderRightWidth"], "0px")
        self.assertEqual(active_style["borderBottomWidth"], "0px")
        self.assertEqual(active_style["borderLeftWidth"], "0px")
        self.assertNotEqual(active_style["color"], inactive_style["color"])
        self.assertGreaterEqual(int(active_style["fontWeight"] or "0"), int(inactive_style["fontWeight"] or "0"))

    def test_public_topbar_active_tab_uses_text_priority_state(self) -> None:
        cases = [
            ("index.html", "archive"),
            ("inha.html", "class"),
            ("shortcuts.html", "archive"),
        ]

        for page_path, active_tab in cases:
            with self.subTest(page=page_path):
                self._artifact_suffix = page_path.replace(".html", "")
                page = self._new_page()
                try:
                    page.goto(f"{self.base_url}/{page_path}", wait_until="load")
                    active_selector = f".app-tab.is-active[data-tab-target='{active_tab}']"
                    inactive_selector = ".app-tab:not(.is-active)"
                    active_style = self._read_style(page, active_selector)
                    inactive_style = self._read_style(page, inactive_selector)
                    self._assert_text_priority_active(active_style, inactive_style, expect_aria_current=False)
                except Exception:
                    self._capture_playwright_artifacts(page, suffix=self._artifact_suffix)
                    self._playwright_artifacts_captured = True
                    raise

    def test_index_primary_cta_uses_filled_capsule(self) -> None:
        self._artifact_suffix = "index-cta"
        page = self._new_page()
        page.goto(f"{self.base_url}/index.html", wait_until="load")
        primary_cta = page.locator("#heroActions a").first
        primary_cta.wait_for(state="visible")
        class_name = primary_cta.get_attribute("class") or ""
        style = self._read_style(page, "#heroActions a")

        self.assertIn("btn-primary", class_name)
        self.assertNotIn(style["backgroundColor"], {"rgba(0, 0, 0, 0)", "transparent"})
        self.assertNotEqual(style["borderTopWidth"], "0px")

    def test_week_sidebar_active_link_uses_text_priority_state(self) -> None:
        self._artifact_suffix = "week-sidebar"
        page = self._new_page()
        page.goto(f"{self.base_url}/week.html", wait_until="load")
        page.locator(".sidebar-nav li.is-active a").first.wait_for(state="visible")
        active_style = self._read_style(page, ".sidebar-nav li.is-active a")
        inactive_style = self._read_style(page, ".sidebar-nav li:not(.is-active) a")
        self._assert_text_priority_active(active_style, inactive_style, expect_aria_current=False)


if __name__ == "__main__":
    unittest.main()
