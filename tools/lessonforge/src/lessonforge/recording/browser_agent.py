"""Browser automation agent using Playwright.

Records browser interactions for web-based practice steps:
- Navigate to URLs (Meshy, PolyHaven, Mixamo, etc.)
- Simulate user actions (clicks, scrolls, form inputs)
- Screenshot specific states for documentation

Playwright is used in headed mode so the screen recorder
can capture the browser viewport during operations.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class BrowserConfig:
    """Browser launch settings."""

    headless: bool = False  # False for screen recording
    viewport_width: int = 1920
    viewport_height: int = 1080
    slow_mo: int = 500  # ms between actions (for visibility)
    default_timeout: int = 30000  # ms
    browser_type: str = "chromium"  # chromium, firefox, webkit


@dataclass
class BrowserAction:
    """A single browser action to execute."""

    action_type: str  # navigate, click, type, scroll, wait, screenshot
    selector: Optional[str] = None
    value: Optional[str] = None  # URL for navigate, text for type
    wait_seconds: float = 1.0
    screenshot_path: Optional[str] = None


@dataclass
class BrowserSession:
    """Tracks an active browser session."""

    page: object = None  # playwright Page
    browser: object = None  # playwright Browser
    context: object = None  # playwright BrowserContext
    screenshots: list[Path] = field(default_factory=list)


class BrowserAgent:
    """Automates browser operations via Playwright.

    Usage:
        agent = BrowserAgent()
        async with agent.session() as session:
            await agent.navigate(session, "https://meshy.ai")
            await agent.screenshot(session, Path("output/meshy.png"))
    """

    def __init__(self, config: Optional[BrowserConfig] = None):
        self.config = config or BrowserConfig()
        self._playwright = None

    @staticmethod
    def is_available() -> bool:
        """Check if Playwright is installed."""
        try:
            import playwright
            return True
        except ImportError:
            return False

    async def _ensure_playwright(self):
        """Lazy-init playwright."""
        if self._playwright is None:
            from playwright.async_api import async_playwright
            self._playwright = await async_playwright().start()

    async def start_session(self) -> BrowserSession:
        """Launch browser and create a new session."""
        await self._ensure_playwright()
        cfg = self.config

        launcher = getattr(self._playwright, cfg.browser_type)
        browser = await launcher.launch(
            headless=cfg.headless,
            slow_mo=cfg.slow_mo,
        )

        context = await browser.new_context(
            viewport={
                "width": cfg.viewport_width,
                "height": cfg.viewport_height,
            },
            locale="ko-KR",
        )
        context.set_default_timeout(cfg.default_timeout)

        page = await context.new_page()

        return BrowserSession(
            page=page,
            browser=browser,
            context=context,
        )

    async def close_session(self, session: BrowserSession) -> None:
        """Close browser session."""
        if session.browser:
            await session.browser.close()

    async def navigate(
        self, session: BrowserSession, url: str, wait_seconds: float = 2.0
    ) -> None:
        """Navigate to a URL and wait for page load."""
        await session.page.goto(url, wait_until="networkidle")
        await asyncio.sleep(wait_seconds)

    async def click(
        self, session: BrowserSession, selector: str, wait_seconds: float = 1.0
    ) -> None:
        """Click an element."""
        await session.page.click(selector)
        await asyncio.sleep(wait_seconds)

    async def type_text(
        self, session: BrowserSession, selector: str, text: str, wait_seconds: float = 0.5
    ) -> None:
        """Type text into an input field."""
        await session.page.fill(selector, text)
        await asyncio.sleep(wait_seconds)

    async def scroll(
        self, session: BrowserSession, pixels: int = 500, wait_seconds: float = 1.0
    ) -> None:
        """Scroll down the page."""
        await session.page.evaluate(f"window.scrollBy(0, {pixels})")
        await asyncio.sleep(wait_seconds)

    async def screenshot(
        self, session: BrowserSession, output_path: Path
    ) -> Path:
        """Take a screenshot of the current page."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        await session.page.screenshot(path=str(output_path), full_page=False)
        session.screenshots.append(output_path)
        return output_path

    async def execute_actions(
        self, session: BrowserSession, actions: list[BrowserAction]
    ) -> list[Path]:
        """Execute a sequence of browser actions.

        Returns list of screenshot paths taken during execution.
        """
        screenshots = []

        for action in actions:
            if action.action_type == "navigate" and action.value:
                await self.navigate(session, action.value, action.wait_seconds)

            elif action.action_type == "click" and action.selector:
                await self.click(session, action.selector, action.wait_seconds)

            elif action.action_type == "type" and action.selector and action.value:
                await self.type_text(
                    session, action.selector, action.value, action.wait_seconds
                )

            elif action.action_type == "scroll":
                pixels = int(action.value) if action.value else 500
                await self.scroll(session, pixels, action.wait_seconds)

            elif action.action_type == "wait":
                await asyncio.sleep(action.wait_seconds)

            elif action.action_type == "screenshot" and action.screenshot_path:
                path = await self.screenshot(
                    session, Path(action.screenshot_path)
                )
                screenshots.append(path)

        return screenshots

    async def record_url_visit(
        self,
        url: str,
        output_dir: Path,
        *,
        scroll_steps: int = 3,
        wait_per_step: float = 2.0,
    ) -> list[Path]:
        """Visit a URL, scroll through it, and capture screenshots.

        Simple automation for demonstrating a website:
        1. Navigate to URL
        2. Screenshot the landing page
        3. Scroll down in steps, screenshotting each
        """
        session = await self.start_session()
        screenshots = []

        try:
            output_dir.mkdir(parents=True, exist_ok=True)

            # Navigate
            await self.navigate(session, url, wait_seconds=3.0)

            # Landing screenshot
            path = await self.screenshot(
                session, output_dir / "page_landing.png"
            )
            screenshots.append(path)

            # Scroll and capture
            for i in range(scroll_steps):
                await self.scroll(session, 600, wait_per_step)
                path = await self.screenshot(
                    session, output_dir / f"page_scroll_{i+1:02d}.png"
                )
                screenshots.append(path)

        finally:
            await self.close_session(session)

        return screenshots


# --- Pre-built browser action sequences ---

BROWSER_DEMOS = {
    "meshy_visit": [
        BrowserAction(action_type="navigate", value="https://www.meshy.ai"),
        BrowserAction(action_type="wait", wait_seconds=3.0),
        BrowserAction(action_type="screenshot", screenshot_path="meshy_landing.png"),
        BrowserAction(action_type="scroll", value="600"),
        BrowserAction(action_type="screenshot", screenshot_path="meshy_features.png"),
    ],

    "polyhaven_visit": [
        BrowserAction(action_type="navigate", value="https://polyhaven.com"),
        BrowserAction(action_type="wait", wait_seconds=2.0),
        BrowserAction(action_type="screenshot", screenshot_path="polyhaven_landing.png"),
        BrowserAction(action_type="scroll", value="400"),
        BrowserAction(action_type="screenshot", screenshot_path="polyhaven_assets.png"),
    ],

    "mixamo_visit": [
        BrowserAction(action_type="navigate", value="https://www.mixamo.com"),
        BrowserAction(action_type="wait", wait_seconds=3.0),
        BrowserAction(action_type="screenshot", screenshot_path="mixamo_landing.png"),
    ],

    "blockade_labs_visit": [
        BrowserAction(
            action_type="navigate", value="https://skybox.blockadelabs.com"
        ),
        BrowserAction(action_type="wait", wait_seconds=3.0),
        BrowserAction(action_type="screenshot", screenshot_path="blockade_landing.png"),
    ],
}


def get_browser_demo(step_title: str) -> Optional[list[BrowserAction]]:
    """Match a step title to a pre-built browser demo."""
    title_lower = step_title.lower()

    if "meshy" in title_lower:
        return BROWSER_DEMOS["meshy_visit"]
    elif "polyhaven" in title_lower or "poly haven" in title_lower:
        return BROWSER_DEMOS["polyhaven_visit"]
    elif "mixamo" in title_lower:
        return BROWSER_DEMOS["mixamo_visit"]
    elif "blockade" in title_lower or "skybox" in title_lower:
        return BROWSER_DEMOS["blockade_labs_visit"]

    return None
