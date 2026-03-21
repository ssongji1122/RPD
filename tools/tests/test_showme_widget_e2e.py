from __future__ import annotations

import sys
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

BEVEL_TOOL_URL = (ROOT / "course-site" / "assets" / "showme" / "bevel-tool.html").as_uri()
BEVEL_MODIFIER_URL = (ROOT / "course-site" / "assets" / "showme" / "bevel-modifier.html").as_uri()
BOX_ROUNDING_URL = (ROOT / "course-site" / "assets" / "showme" / "box-rounding.html").as_uri()
TRANSFORM_APPLY_URL = (ROOT / "course-site" / "assets" / "showme" / "transform-apply.html").as_uri()
SOLIDIFY_MODIFIER_URL = (ROOT / "course-site" / "assets" / "showme" / "solidify-modifier.html").as_uri()


class ShowMeBevelToolE2ETest(PlaywrightFailureArtifactsMixin, unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if sync_playwright is None:
            raise unittest.SkipTest("playwright is not installed")

        try:
            cls.playwright = sync_playwright().start()
            cls.browser = cls.playwright.chromium.launch(headless=True)
        except PlaywrightError as exc:
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

    def setUp(self) -> None:
        self._artifact_suffix = ""
        self._playwright_artifacts_captured = False
        self.context = self.browser.new_context(
            viewport={"width": 1500, "height": 1100},
            color_scheme="dark",
            device_scale_factor=1,
        )
        self.page = self.context.new_page()

    def tearDown(self) -> None:
        if self._test_failed() and not self._playwright_artifacts_captured:
            self._capture_playwright_artifacts(self.page, suffix=self._artifact_suffix)
        self.context.close()

    def _open_visual_panel(self, url: str) -> None:
        self.page.goto(url, wait_until="load")
        self.page.click('[data-tab="visual"]')
        self.page.locator("#panel-visual").wait_for(state="visible")

    def _set_input_value(self, selector: str, value: str) -> None:
        self.page.locator(selector).evaluate(
            """(element, nextValue) => {
                element.value = nextValue;
                element.dispatchEvent(new Event("input", { bubbles: true }));
            }""",
            str(value),
        )

    def _input_value(self, selector: str) -> str:
        return self.page.locator(selector).input_value().strip()

    def _text(self, selector: str) -> str:
        return (self.page.locator(selector).text_content() or "").strip()

    def _set_checked(self, selector: str, checked: bool) -> None:
        if checked:
            self.page.locator(selector).check()
        else:
            self.page.locator(selector).uncheck()

    def _select_option(self, selector: str, value: str) -> None:
        self.page.locator(selector).select_option(value)

    def _count_highlight_pixels(self, x: int, y: int, radius: int = 6, canvas_id: str = "demoCanvas") -> int:
        return int(
            self.page.evaluate(
                """({x, y, radius, canvasId}) => {
                    const canvas = document.getElementById(canvasId);
                    const ctx = canvas.getContext("2d");
                    const left = Math.max(0, x - radius);
                    const top = Math.max(0, y - radius);
                    const width = Math.min(canvas.width - left, radius * 2 + 1);
                    const height = Math.min(canvas.height - top, radius * 2 + 1);
                    const pixels = ctx.getImageData(left, top, width, height).data;
                    let matches = 0;
                    for (let index = 0; index < pixels.length; index += 4) {
                        const red = pixels[index];
                        const green = pixels[index + 1];
                        const blue = pixels[index + 2];
                        const alpha = pixels[index + 3];
                        const isBlue = blue >= 120 && green >= 70 && red <= 120;
                        const isGreen = green >= 120 && blue >= 70 && red <= 120;
                        if (alpha > 0 && (isBlue || isGreen)) {
                            matches += 1;
                        }
                    }
                    return matches;
                }""",
                {"x": x, "y": y, "radius": radius, "canvasId": canvas_id},
            )
        )

    def _has_highlight_near(self, x: int, y: int, radius: int = 6, canvas_id: str = "demoCanvas") -> bool:
        return self._count_highlight_pixels(x, y, radius=radius, canvas_id=canvas_id) > 0

    def _count_blue_label_pixels(self, x: int, y: int, radius: int = 12, canvas_id: str = "demoCanvas") -> int:
        return int(
            self.page.evaluate(
                """({x, y, radius, canvasId}) => {
                    const canvas = document.getElementById(canvasId);
                    const ctx = canvas.getContext("2d");
                    const left = Math.max(0, x - radius);
                    const top = Math.max(0, y - radius);
                    const width = Math.min(canvas.width - left, radius * 2 + 1);
                    const height = Math.min(canvas.height - top, radius * 2 + 1);
                    const pixels = ctx.getImageData(left, top, width, height).data;
                    let matches = 0;
                    for (let index = 0; index < pixels.length; index += 4) {
                        const red = pixels[index];
                        const green = pixels[index + 1];
                        const blue = pixels[index + 2];
                        const alpha = pixels[index + 3];
                        if (alpha > 0 && blue > 120 && green > 80 && red < 140) {
                            matches += 1;
                        }
                    }
                    return matches;
                }""",
                {"x": x, "y": y, "radius": radius, "canvasId": canvas_id},
            )
        )

    def _count_green_pixels(self, x: int, y: int, radius: int = 12, canvas_id: str = "demoCanvas") -> int:
        return int(
            self.page.evaluate(
                """({x, y, radius, canvasId}) => {
                    const canvas = document.getElementById(canvasId);
                    const ctx = canvas.getContext("2d");
                    const left = Math.max(0, x - radius);
                    const top = Math.max(0, y - radius);
                    const width = Math.min(canvas.width - left, radius * 2 + 1);
                    const height = Math.min(canvas.height - top, radius * 2 + 1);
                    const pixels = ctx.getImageData(left, top, width, height).data;
                    let matches = 0;
                    for (let index = 0; index < pixels.length; index += 4) {
                        const red = pixels[index];
                        const green = pixels[index + 1];
                        const blue = pixels[index + 2];
                        const alpha = pixels[index + 3];
                        const isGreen = green >= 120 && blue >= 70 && red <= 120;
                        if (alpha > 0 && isGreen) {
                            matches += 1;
                        }
                    }
                    return matches;
                }""",
                {"x": x, "y": y, "radius": radius, "canvasId": canvas_id},
            )
        )

    def test_bevel_tool_panel_inputs_stay_in_sync(self) -> None:
        self._open_visual_panel(BEVEL_TOOL_URL)

        self._set_input_value("#bevelSegmentsRange", "6")
        self.assertEqual(self._input_value("#bevelSegmentsNumber"), "6")
        self.assertEqual(self._text("#bevelSegmentsLabel"), "6")
        self.assertEqual(self._text("#bevelResultStatus"), "Rounded bevel")

        self._set_input_value("#bevelProfileNumber", "0.2")
        self.assertEqual(self._input_value("#bevelProfileRange"), "0.2")
        self.assertEqual(self._text("#bevelProfileLabel"), "0.2")
        self.assertEqual(self._text("#bevelProfileStatus"), "Flat chamfer")

        self._set_input_value("#bevelWidthRange", "0.06")
        self.assertEqual(self._input_value("#bevelWidthNumber"), "0.06")
        self.assertEqual(self._text("#bevelWidthLabel"), "0.06")
        self.assertEqual(self._text("#bevelWidthStatus"), "Wide")

        self._set_input_value("#bevelWidthNumber", "0.01")
        self.assertEqual(self._input_value("#bevelWidthRange"), "0.01")
        self.assertEqual(self._text("#bevelWidthStatus"), "Narrow")

    def test_bevel_curve_bends_toward_the_original_corner(self) -> None:
        self._open_visual_panel(BEVEL_TOOL_URL)

        self._set_input_value("#bevelSegmentsNumber", "6")
        self._set_input_value("#bevelProfileNumber", "0.4")
        self._set_input_value("#bevelWidthNumber", "0.04")

        self.assertTrue(
            self._has_highlight_near(495, 156, radius=7),
            "rounded bevel highlight should appear near the original corner",
        )
        self.assertFalse(
            self._has_highlight_near(483, 145, radius=4),
            "highlight should not bow inward like an inverted bevel",
        )

    def test_bevel_modifier_panel_controls_and_render_state(self) -> None:
        self._open_visual_panel(BEVEL_MODIFIER_URL)

        self._set_input_value("#bevelSegmentsRange", "5")
        self.assertEqual(self._input_value("#bevelSegmentsNumber"), "5")
        self.assertEqual(self._text("#bevelSegmentsLabel"), "5")
        self.assertEqual(self._text("#bevelShapeStatus"), "Round")

        self._set_input_value("#bevelWidthNumber", "0.08")
        self.assertEqual(self._input_value("#bevelWidthRange"), "0.08")
        self.assertEqual(self._text("#bevelWidthLabel"), "0.08")

        self._select_option("#bevelLimitMethod", "weight")
        self.assertEqual(self._text("#bevelLimitStatus"), "Weight")

        self._set_checked("#bevelWeightedNormal", False)
        self.assertEqual(self._text("#bevelShadingStatus"), "Weighted Normal OFF")

        self.assertTrue(
            self._has_highlight_near(490, 102, radius=8),
            "modifier bevel should keep a highlighted start point on the outer corner",
        )
        self.assertTrue(
            self._has_highlight_near(527, 140, radius=8),
            "modifier bevel should reach the outer edge endpoint",
        )
        self.assertFalse(
            self._has_highlight_near(470, 140, radius=5),
            "modifier bevel should not draw a highlight on the inner side of the corner",
        )

    def test_box_rounding_presets_update_description_and_active_cell(self) -> None:
        self._open_visual_panel(BOX_ROUNDING_URL)

        self.page.click('.demo-btn[data-width="0.6"]')
        self.page.click('.demo-btn[data-r="0.0"]')

        active_texts = [text.strip() for text in self.page.locator(".demo-btn.is-active").all_text_contents()]
        self.assertIn("넓게", active_texts)
        self.assertIn("0.0 오목", active_texts)

        description = self._text("#boxRoundDesc")
        self.assertIn("Width가 넓어서", description)
        self.assertIn("Profile이 낮아", description)

        self.assertGreater(
            self._count_blue_label_pixels(85, 292, radius=18),
            20,
            "active box-rounding cell should emphasize the left label when R=0.0 is selected",
        )
        self.assertLess(
            self._count_blue_label_pixels(595, 292, radius=18),
            5,
            "inactive box-rounding cells should not receive the same active blue label treatment",
        )

    def test_transform_apply_scenario_switch_updates_desc_and_flow(self) -> None:
        self._open_visual_panel(TRANSFORM_APPLY_URL)

        self.page.click('.scenario-btn[data-scene="rotation"]')

        self.assertEqual(
            self._text(".scenario-btn.is-active"),
            "Apply Rotation",
        )
        self.assertIn(
            "Apply Rotation: Rotation이 45도인 상태에서 Physics를 적용하면 오브젝트의 '실제 방향'이 달라 시뮬레이션이 엉뚱하게 동작합니다.",
            self._text("#sceneDesc"),
        )

        cause_effect_text = self._text("#ceFlow")
        self.assertIn("Rotation 45° 미적용 상태에서 Physics 추가", cause_effect_text)
        self.assertIn("Apply Rotation → Rotation (0, 0, 0) 후 Physics", cause_effect_text)
        self.assertIn("올바른 방향으로 Physics 시뮬레이션 동작", cause_effect_text)

    def test_solidify_modifier_panel_controls_and_render_state(self) -> None:
        self._open_visual_panel(SOLIDIFY_MODIFIER_URL)

        self._set_input_value("#solidifyThicknessNumber", "0.12")
        self.assertEqual(self._input_value("#solidifyThicknessRange"), "0.12")
        self.assertEqual(self._text("#solidifyThicknessLabel"), "0.12 m")

        self._set_input_value("#solidifyOffsetNumber", "-1.0")
        self.assertEqual(self._input_value("#solidifyOffsetRange"), "-1")
        self.assertEqual(self._text("#solidifyOffsetLabel"), "-1.00")

        self._set_checked("#solidifyEvenThickness", False)
        self.assertEqual(self._text("#solidifyDirectionStatus"), "안쪽으로 추가")
        self.assertEqual(self._text("#solidifyCenterStatus"), "원본 면은 바깥 경계")
        self.assertEqual(self._text("#solidifyCornerStatus"), "코너에서 두께가 눌릴 수 있음")

        probe_points = self.page.evaluate(
            """() => {
                const canvas = document.getElementById("demoCanvas");
                const w = canvas.width;
                const h = canvas.height;
                const leftArea = { x: 16, y: 16, w: Math.floor(w * 0.31), h: h - 32 };
                const rightArea = {
                    x: leftArea.x + leftArea.w + 12,
                    y: 16,
                    w: w - leftArea.w - 44,
                    h: Math.floor(h * 0.63),
                };
                const lineY = rightArea.y + rightArea.h * 0.6;
                const thicknessPx = 0.12 * 720;
                const top = lineY;
                const bottom = lineY + thicknessPx;
                const left = rightArea.x + 46;
                const width = rightArea.w - 92;
                return {
                    rightWall: {
                        x: Math.round(left + width + 8),
                        y: Math.round((top + bottom) / 2 - 8),
                    },
                    leftSide: {
                        x: Math.round(left + 8),
                        y: Math.round((top + bottom) / 2),
                    },
                };
            }"""
        )

        self.assertTrue(
            self._count_green_pixels(
                probe_points["rightWall"]["x"],
                probe_points["rightWall"]["y"],
                radius=14,
            )
            > 0,
            "solidify preview should show the green outer wall near the right-side extrusion",
        )
        self.assertFalse(
            self._count_green_pixels(
                probe_points["leftSide"]["x"],
                probe_points["leftSide"]["y"],
                radius=14,
            )
            > 0,
            "inner offset mode should not highlight the same green wall on the left side",
        )


if __name__ == "__main__":
    unittest.main()
