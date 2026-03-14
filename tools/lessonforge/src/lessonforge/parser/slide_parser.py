"""Render Marp slides to PNG images using Marp CLI.

Marp CLI converts markdown slides into individual PNG images that can be
composited into the final video. Each slide becomes one frame/scene.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional


def find_marp_cli() -> Optional[str]:
    """Find the marp CLI executable."""
    # Check common locations
    marp = shutil.which("marp")
    if marp:
        return marp

    # Check nvm-managed global install
    nvm_dir = Path.home() / ".nvm"
    if nvm_dir.exists():
        # Find the current node version's bin directory
        for version_dir in sorted(nvm_dir.glob("versions/node/*/bin/marp"), reverse=True):
            return str(version_dir)

    return None


def count_slides(slides_md: Path) -> int:
    """Count the number of slides in a Marp markdown file."""
    content = slides_md.read_text(encoding="utf-8")
    # Slides are separated by --- on its own line (after the frontmatter)
    # Remove YAML frontmatter
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            content = content[end + 3:]
    # Count slide separators
    separators = re.findall(r"^---\s*$", content, re.MULTILINE)
    return len(separators) + 1  # +1 for the first slide


def render_slides(
    slides_md: Path,
    output_dir: Path,
    *,
    theme_css: Optional[Path] = None,
    width: int = 1920,
    height: int = 1080,
) -> list[Path]:
    """Render Marp slides to individual PNG images.

    Args:
        slides_md: Path to the slides.md file.
        output_dir: Directory to save PNG images.
        theme_css: Optional custom CSS theme file.
        width: Image width in pixels.
        height: Image height in pixels.

    Returns:
        List of paths to generated PNG files, in slide order.
    """
    marp = find_marp_cli()
    if not marp:
        raise RuntimeError(
            "Marp CLI not found. Install with: npm install -g @marp-team/marp-cli"
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    # Build marp command
    cmd = [
        marp,
        str(slides_md),
        "--images", "png",
        "--image-scale", "1",
        "--output", str(output_dir / "slide.png"),  # marp adds .001.png, .002.png, etc.
    ]

    if theme_css and theme_css.exists():
        cmd.extend(["--theme", str(theme_css)])

    # Set resolution via --html flag and custom size
    cmd.extend(["--allow-local-files"])

    # Run marp
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Marp CLI failed:\n{result.stderr}")

    # Collect generated PNG files in order
    png_files = sorted(output_dir.glob("slide.*.png"))

    # If marp uses a different naming pattern, try alternatives
    if not png_files:
        png_files = sorted(output_dir.glob("*.png"))

    return png_files


def get_slide_titles(slides_md: Path) -> list[str]:
    """Extract titles (first heading) from each slide.

    Used for matching slides to narration blocks.
    """
    content = slides_md.read_text(encoding="utf-8")

    # Remove frontmatter
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            content = content[end + 3:]

    # Split into slides
    slides = re.split(r"^---\s*$", content, flags=re.MULTILINE)

    titles = []
    for slide in slides:
        slide = slide.strip()
        if not slide:
            titles.append("")
            continue
        # Find first heading
        match = re.search(r"^#+\s+(.+)$", slide, re.MULTILINE)
        titles.append(match.group(1).strip() if match else "")

    return titles
