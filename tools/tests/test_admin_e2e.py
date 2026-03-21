from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
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


class AdminServerE2ETest(PlaywrightFailureArtifactsMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if sync_playwright is None:
            raise unittest.SkipTest("playwright is not installed")

        cls.temp_dir = tempfile.TemporaryDirectory(prefix="rpd-admin-e2e-")
        cls.temp_root = Path(cls.temp_dir.name)
        shutil.copytree(ROOT / "course-site", cls.temp_root / "course-site")
        shutil.copytree(ROOT / "weeks", cls.temp_root / "weeks")
        (cls.temp_root / "tools").mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "tools" / "notion-mapping.json", cls.temp_root / "tools" / "notion-mapping.json")
        cls.mapping_count = len(
            json.loads((cls.temp_root / "tools" / "notion-mapping.json").read_text(encoding="utf-8"))["weeks"]
        )

        cls.port = _find_free_port()
        env = os.environ.copy()
        env["ADMIN_KEY"] = "test-admin-key"
        env["NOTION_TOKEN"] = "mock-notion-token"
        env["PYTHONUNBUFFERED"] = "1"
        env["RPD_MOCK_NOTION"] = "1"
        env["RPD_ROOT_DIR"] = str(cls.temp_root)
        cls.proc = subprocess.Popen(
            [
                sys.executable,
                "tools/admin-server.py",
                "--host",
                "127.0.0.1",
                "--port",
                str(cls.port),
            ],
            cwd=ROOT,
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
            cls.temp_dir.cleanup()
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
        if getattr(cls, "temp_dir", None) is not None:
            cls.temp_dir.cleanup()

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
        raise RuntimeError(f"admin server failed to start: {last_error}\n{output}")

    def setUp(self) -> None:
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self._artifact_suffix = ""
        self._playwright_artifacts_captured = False

    def tearDown(self) -> None:
        if self._test_failed() and not self._playwright_artifacts_captured:
            self._capture_playwright_artifacts(self.page, suffix=self._artifact_suffix)
        if getattr(self, "context", None) is not None:
            self.context.close()
            self.context = None
            self.page = None

    def _login(self, page) -> None:
        page.goto(f"{self.base_url}/admin.html", wait_until="load")
        page.locator("#authInput").wait_for(state="visible")
        page.locator("#authInput").fill("test-admin-key")
        page.locator("#authSubmit").click()
        page.locator("#sidebarList .sidebar-item").first.wait_for(state="visible")
        page.locator("#authOverlay").wait_for(state="hidden")

    def _read_style(self, page, selector: str) -> dict[str, str | None]:
        page.locator(selector).first.wait_for(state="visible")
        return page.locator(selector).first.evaluate(
            """el => {
                const style = getComputedStyle(el);
                return {
                  color: style.color,
                  backgroundColor: style.backgroundColor,
                  backgroundImage: style.backgroundImage,
                  boxShadow: style.boxShadow,
                  borderTopWidth: style.borderTopWidth,
                  borderRightWidth: style.borderRightWidth,
                  borderBottomWidth: style.borderBottomWidth,
                  borderLeftWidth: style.borderLeftWidth,
                  fontWeight: style.fontWeight
                };
            }"""
        )

    def test_admin_editor_login_diff_save_and_upload(self) -> None:
        self._artifact_suffix = "login-diff-save-upload"
        page = self.page
        self._login(page)

        original_version = page.locator("#versionBadge").inner_text().strip()
        title_input = page.locator('input[data-field="title"]')
        original_title = title_input.input_value().strip()
        updated_title = f"{original_title} E2E"

        title_input.fill(updated_title)
        page.locator("#dirtyIndicator").wait_for(state="visible")

        page.locator("#diffBtn").click()
        page.locator("#diffOverlay").wait_for(state="visible")
        page.wait_for_function(
            "() => document.getElementById('diffMeta').textContent.includes('현재 ')"
        )
        diff_text = page.locator("#diffLog").inner_text()
        self.assertIn("Week 01", diff_text)
        self.assertIn("title", diff_text)
        page.locator("#diffCloseBtn").click()
        page.locator("#diffOverlay").wait_for(state="hidden")

        page.locator('input[data-upload-step="0"]').set_input_files(
            files=[
                {
                    "name": "e2e-step.png",
                    "mimeType": "image/png",
                    "buffer": b"\x89PNG\r\n\x1a\nE2E",
                }
            ]
        )
        page.locator(".toast.success").last.wait_for(state="visible")

        page.locator("#saveBtn").click()
        page.locator(".toast.success").last.wait_for(state="visible")
        page.locator("#dirtyIndicator").wait_for(state="hidden")

        new_version = page.locator("#versionBadge").inner_text().strip()
        self.assertNotEqual(original_version, new_version)

        page.reload(wait_until="load")
        page.locator('input[data-field="title"]').wait_for(state="visible")
        self.assertEqual(page.locator('input[data-field="title"]').input_value().strip(), updated_title)

        image_src = page.locator("img.step-image").first.get_attribute("src") or ""
        self.assertIn("assets/images/week-01/step-0.png", image_src)

        canonical = json.loads(
            (self.temp_root / "weeks" / "site-data.json").read_text(encoding="utf-8")
        )
        self.assertEqual(canonical[0]["title"], updated_title)

        uploaded_image = self.temp_root / "course-site" / "assets" / "images" / "week-01" / "step-0.png"
        self.assertTrue(uploaded_image.exists())

        page.locator("#logoutBtn").click()
        page.locator("#authInput").wait_for(state="visible")

    def test_admin_notion_push_all_mock_flow(self) -> None:
        self._artifact_suffix = "notion-push-all"
        page = self.page
        self._login(page)
        page.locator("#notionPushAllBtn").wait_for(state="visible")
        page.locator("#notionPushAllBtn").click()

        page.locator("#pushAllOverlay").wait_for(state="visible")
        page.wait_for_function(
            "() => document.getElementById('pushAllLog').textContent.includes('완료:')"
        )

        push_log = page.locator("#pushAllLog").inner_text()
        self.assertIn(f"{self.mapping_count}/{self.mapping_count} 성공", push_log)
        self.assertIn("Week 01", push_log)
        self.assertNotIn("검증 실패", push_log)

        page.locator("#pushAllCloseBtn").click()
        page.locator("#pushAllOverlay").wait_for(state="hidden")

    def test_admin_sidebar_section_active_link_uses_text_priority_state(self) -> None:
        self._artifact_suffix = "sidebar-text-priority"
        page = self.page
        self._login(page)
        active_style = self._read_style(page, '.sidebar-link.is-active[data-nav-target]')
        inactive_style = self._read_style(page, '.sidebar-link[data-nav-target]:not(.is-active)')

        self.assertEqual(active_style["backgroundImage"], "none")
        self.assertIn(active_style["backgroundColor"], {"rgba(0, 0, 0, 0)", "transparent"})
        self.assertEqual(active_style["boxShadow"], "none")
        self.assertEqual(active_style["borderTopWidth"], "0px")
        self.assertEqual(active_style["borderRightWidth"], "0px")
        self.assertEqual(active_style["borderBottomWidth"], "0px")
        self.assertEqual(active_style["borderLeftWidth"], "0px")
        self.assertNotEqual(active_style["color"], inactive_style["color"])
        self.assertGreaterEqual(int(active_style["fontWeight"] or "0"), int(inactive_style["fontWeight"] or "0"))


if __name__ == "__main__":
    unittest.main()
