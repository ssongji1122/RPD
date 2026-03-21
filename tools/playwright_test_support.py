from __future__ import annotations

import os
import re
from pathlib import Path


def _sanitize_artifact_name(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return normalized or "playwright-artifact"


class PlaywrightFailureArtifactsMixin:
    def _matches_failed_test_case(self, test_case: object) -> bool:
        if test_case is self:
            return True

        return getattr(test_case, "test_case", None) is self or getattr(test_case, "_test_case", None) is self

    def _artifact_base_dir(self) -> Path | None:
        raw_dir = os.getenv("RPD_TEST_ARTIFACT_DIR", "").strip()
        if not raw_dir:
            return None
        base_dir = Path(raw_dir)
        base_dir.mkdir(parents=True, exist_ok=True)
        return base_dir

    def _test_failed(self) -> bool:
        outcome = getattr(self, "_outcome", None)
        result = getattr(outcome, "result", None)
        if result is None:
            return False

        failures = list(getattr(result, "failures", []))
        errors = list(getattr(result, "errors", []))
        return any(self._matches_failed_test_case(test_case) for test_case, _ in failures + errors)

    def _capture_playwright_artifacts(self, page, *, suffix: str = "") -> None:
        if page is None:
            return

        base_dir = self._artifact_base_dir()
        if base_dir is None:
            return

        stem = _sanitize_artifact_name(self.id())
        if suffix:
            stem = f"{stem}-{_sanitize_artifact_name(suffix)}"

        screenshot_path = base_dir / f"{stem}.png"
        html_path = base_dir / f"{stem}.html"

        if hasattr(page, "is_closed") and page.is_closed():
            return

        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
        except Exception:  # pragma: no cover - artifact capture must not mask the real failure
            pass

        try:
            html_path.write_text(page.content(), encoding="utf-8")
        except Exception:  # pragma: no cover - artifact capture must not mask the real failure
            pass
