"""Generate title cards and section headers using Pillow.

These are static images used for intro/outro screens, section transitions,
and step indicators in the final video. Design matches the Marp dark theme.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


# Design tokens matching marp-theme.css / lessonforge.config.yaml
COLORS = {
    "background": "#1a1a2e",
    "surface": "#2d2d44",
    "accent": "#00d4ff",
    "emphasis": "#ff6b6b",
    "text": "#eaeaea",
    "text_muted": "#aaaaaa",
}


def _hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def _get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Get a suitable font, falling back to default if needed."""
    # Try common Korean/system fonts on macOS
    font_candidates = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/Library/Fonts/Pretendard-Regular.otf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    if bold:
        font_candidates = [
            "/Library/Fonts/Pretendard-Bold.otf",
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        ] + font_candidates

    for font_path in font_candidates:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, size)
            except (OSError, IOError):
                continue

    # Fallback to default
    return ImageFont.load_default()


def generate_title_card(
    week: int,
    title: str,
    segment_number: int,
    output_path: Path,
    *,
    subtitle: str = "",
    width: int = 1920,
    height: int = 1080,
) -> Path:
    """Generate a title card image for segment intro.

    Design: Dark background with centered title, week/segment info,
    and accent-colored decorative elements.
    """
    bg = _hex_to_rgb(COLORS["background"])
    accent = _hex_to_rgb(COLORS["accent"])
    text_color = _hex_to_rgb(COLORS["text"])
    muted = _hex_to_rgb(COLORS["text_muted"])

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    # Accent line at top
    draw.rectangle([(0, 0), (width, 4)], fill=accent)

    # Week badge
    badge_font = _get_font(28)
    badge_text = f"WEEK {week:02d}  •  PART {segment_number}"
    badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_w = badge_bbox[2] - badge_bbox[0]
    draw.text(
        ((width - badge_w) // 2, height // 2 - 120),
        badge_text,
        font=badge_font,
        fill=accent,
    )

    # Main title
    title_font = _get_font(56, bold=True)
    # Word-wrap title if too long
    lines = _wrap_text(draw, title, title_font, width - 200)
    y = height // 2 - 40
    for line in lines:
        line_bbox = draw.textbbox((0, 0), line, font=title_font)
        line_w = line_bbox[2] - line_bbox[0]
        draw.text(((width - line_w) // 2, y), line, font=title_font, fill=text_color)
        y += 70

    # Subtitle
    if subtitle:
        sub_font = _get_font(28)
        sub_bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
        sub_w = sub_bbox[2] - sub_bbox[0]
        draw.text(
            ((width - sub_w) // 2, y + 30), subtitle, font=sub_font, fill=muted
        )

    # Bottom info bar
    info_font = _get_font(20)
    info_text = "인하대학교 • 로봇프러덕트 디자인 • 2026 Spring"
    info_bbox = draw.textbbox((0, 0), info_text, font=info_font)
    info_w = info_bbox[2] - info_bbox[0]
    draw.text(
        ((width - info_w) // 2, height - 60), info_text, font=info_font, fill=muted
    )

    # Bottom accent line
    draw.rectangle([(0, height - 4), (width, height)], fill=accent)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "PNG")
    return output_path


def generate_section_header(
    section_type: str,
    title: str,
    output_path: Path,
    *,
    width: int = 1920,
    height: int = 1080,
) -> Path:
    """Generate a section transition card (이론/실습/과제).

    Color-coded by section type:
    - Theory: accent (#00d4ff)
    - Practice: emphasis (#ff6b6b)
    - Assignment: surface (#2d2d44)
    """
    bg = _hex_to_rgb(COLORS["background"])
    text_color = _hex_to_rgb(COLORS["text"])

    type_colors = {
        "theory": _hex_to_rgb(COLORS["accent"]),
        "practice": _hex_to_rgb(COLORS["emphasis"]),
        "assignment": _hex_to_rgb(COLORS["surface"]),
    }
    type_labels = {
        "theory": "이론",
        "practice": "실습",
        "assignment": "과제",
    }
    accent = type_colors.get(section_type, _hex_to_rgb(COLORS["accent"]))
    label = type_labels.get(section_type, section_type)

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    # Left accent bar
    draw.rectangle([(80, height // 2 - 80), (90, height // 2 + 80)], fill=accent)

    # Section type label
    label_font = _get_font(36, bold=True)
    draw.text((120, height // 2 - 70), label, font=label_font, fill=accent)

    # Section title
    title_font = _get_font(48, bold=True)
    lines = _wrap_text(draw, title, title_font, width - 300)
    y = height // 2 - 10
    for line in lines:
        draw.text((120, y), line, font=title_font, fill=text_color)
        y += 60

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "PNG")
    return output_path


def generate_step_indicator(
    step_number: int,
    step_title: str,
    output_path: Path,
    *,
    total_steps: int = 0,
    width: int = 1920,
    height: int = 1080,
) -> Path:
    """Generate a step indicator card for practice sections."""
    bg = _hex_to_rgb(COLORS["background"])
    accent = _hex_to_rgb(COLORS["emphasis"])
    text_color = _hex_to_rgb(COLORS["text"])
    muted = _hex_to_rgb(COLORS["text_muted"])

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    # Step number circle
    cx, cy = width // 2, height // 2 - 60
    r = 50
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=accent)
    num_font = _get_font(40, bold=True)
    num_text = str(step_number)
    num_bbox = draw.textbbox((0, 0), num_text, font=num_font)
    num_w = num_bbox[2] - num_bbox[0]
    num_h = num_bbox[3] - num_bbox[1]
    draw.text(
        (cx - num_w // 2, cy - num_h // 2 - 4),
        num_text,
        font=num_font,
        fill=_hex_to_rgb(COLORS["background"]),
    )

    # Step title
    title_font = _get_font(44, bold=True)
    title_bbox = draw.textbbox((0, 0), step_title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(
        ((width - title_w) // 2, cy + 70), step_title, font=title_font, fill=text_color
    )

    # Progress indicator (if total_steps known)
    if total_steps > 0:
        prog_font = _get_font(22)
        prog_text = f"Step {step_number} / {total_steps}"
        prog_bbox = draw.textbbox((0, 0), prog_text, font=prog_font)
        prog_w = prog_bbox[2] - prog_bbox[0]
        draw.text(
            ((width - prog_w) // 2, cy + 130), prog_text, font=prog_font, fill=muted
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "PNG")
    return output_path


def generate_outro_card(
    output_path: Path,
    *,
    message: str = "수고하셨습니다",
    width: int = 1920,
    height: int = 1080,
) -> Path:
    """Generate an outro/end card."""
    bg = _hex_to_rgb(COLORS["background"])
    accent = _hex_to_rgb(COLORS["accent"])
    text_color = _hex_to_rgb(COLORS["text"])
    muted = _hex_to_rgb(COLORS["text_muted"])

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)

    # Main message
    msg_font = _get_font(52, bold=True)
    msg_bbox = draw.textbbox((0, 0), message, font=msg_font)
    msg_w = msg_bbox[2] - msg_bbox[0]
    draw.text(
        ((width - msg_w) // 2, height // 2 - 40),
        message,
        font=msg_font,
        fill=text_color,
    )

    # Accent underline
    draw.rectangle(
        [(width // 2 - 60, height // 2 + 30), (width // 2 + 60, height // 2 + 34)],
        fill=accent,
    )

    # Footer
    footer_font = _get_font(22)
    footer = "인하대학교 로봇프러덕트 디자인"
    footer_bbox = draw.textbbox((0, 0), footer, font=footer_font)
    footer_w = footer_bbox[2] - footer_bbox[0]
    draw.text(
        ((width - footer_w) // 2, height - 60), footer, font=footer_font, fill=muted
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output_path), "PNG")
    return output_path


def _wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    """Simple text wrapping."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines or [text]
