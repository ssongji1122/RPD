#!/usr/bin/env python3
"""
영상에 이미지 오버레이 삽입 스크립트

세 가지 모드 지원:
  1. PiP (Picture-in-Picture): 영상 위에 이미지를 작은 창으로 표시
  2. Insert (전체화면 인서트): 영상 중간에 이미지를 전체화면으로 삽입
  3. TextCallout (텍스트 콜아웃): 자동 생성 텍스트 박스를 영상 위에 표시

사용법:
  python3 overlay_images.py                    # 기본 설정으로 실행
  python3 overlay_images.py --dry-run          # FFmpeg 명령만 출력 (실행 안 함)
  python3 overlay_images.py --clip 004         # 특정 클립만 처리
  python3 overlay_images.py --generate-only    # 텍스트 콜아웃 이미지만 생성

설정: OVERLAYS 딕셔너리에서 클립별 오버레이를 정의합니다.
"""

import os
import subprocess
import tempfile
from pathlib import Path
from dataclasses import dataclass, field
from typing import Literal

# ──────────────────────────────────────────
# 설정
# ──────────────────────────────────────────
FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"
FPS = 30

CLIPS_DIR = Path(__file__).parent / "Blender_tutorial_clips"
OUTPUT_DIR = Path(__file__).parent / "output" / "week02_overlay"
IMAGES_DIR = Path(__file__).parent / "overlay_images"

# 전체화면 인서트 기본값
INSERT_DURATION = 5       # 인서트 표시 시간 (초)
INSERT_FADE = 0.5         # 페이드 인/아웃 (초)

# PiP 기본값
PIP_SCALE = 0.35          # 원본 대비 PiP 크기 비율
PIP_MARGIN = 30           # 화면 가장자리 여백 (px)
PIP_FADE = 0.3            # PiP 페이드 인/아웃 (초)

# 폰트
FONT_PATH = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"


@dataclass
class PipOverlay:
    """PiP 모드: 영상 위에 이미지를 작은 창으로 표시"""
    image: str                    # 이미지 파일명 (IMAGES_DIR 기준)
    start: float                  # 시작 시간 (초)
    end: float                    # 종료 시간 (초)
    position: str = "top-right"   # top-left, top-right, bottom-left, bottom-right, center
    scale: float = PIP_SCALE      # 크기 비율 (0.0~1.0)
    fade: float = PIP_FADE        # 페이드 길이 (초)
    border: int = 3               # 테두리 두께 (px), 0이면 없음
    shadow: bool = True           # 그림자 효과
    _abs_path: bool = False       # 내부용: image가 절대경로인지


@dataclass
class InsertOverlay:
    """전체화면 인서트: 영상 중간에 이미지를 전체화면으로 삽입"""
    image: str                    # 이미지 파일명 (IMAGES_DIR 기준)
    at: float                     # 삽입할 시점 (초) — 영상이 이 시점에서 잘려서 인서트가 들어감
    duration: float = INSERT_DURATION  # 표시 시간 (초)
    fade: float = INSERT_FADE          # 페이드 인/아웃 (초)
    bg_color: str = "black"            # 배경색 (이미지가 화면보다 작을 때)


@dataclass
class TextCallout:
    """텍스트 콜아웃: Pillow로 자동 생성되는 설명 박스 오버레이
    차녹 CHANOK 스타일의 텍스트 박스를 자동으로 만들어 영상에 삽입합니다.
    """
    text: str                     # 표시할 텍스트 (줄바꿈은 \n)
    start: float                  # 시작 시간 (초)
    end: float                    # 종료 시간 (초)
    position: str = "top-right"   # top-left, top-right, bottom-left, bottom-right, center
    # 스타일 설정
    font_size: int = 32           # 폰트 크기
    text_color: str = "#FFFFFF"   # 텍스트 색상
    bg_color: str = "#000000"     # 배경 색상
    bg_opacity: float = 0.75      # 배경 투명도 (0.0~1.0)
    accent_color: str = "#FF4444" # 강조색 (왼쪽 바, 밑줄 등)
    padding: int = 20             # 내부 여백 (px)
    border_radius: int = 12       # 둥근 모서리 반지름
    accent_bar: bool = True       # 왼쪽 강조 바 표시
    max_width: int = 500          # 최대 너비 (px)
    # 오버레이 설정
    fade: float = PIP_FADE
    margin: int = PIP_MARGIN
    # 제목 (선택)
    title: str = ""               # 제목 (큰 글자로 표시)
    title_color: str = "#FF6B6B"  # 제목 색상
    # 자동 생성 이미지 이름 (내부용)
    _generated_image: str = ""


@dataclass
class HighlightBox:
    """화면 특정 영역을 색 테두리로 강조 (하이라이트 박스)
    Blender UI의 특정 패널/영역을 강조할 때 사용합니다.
    """
    start: float                  # 시작 시간 (초)
    end: float                    # 종료 시간 (초)
    # 박스 위치 (영상 해상도 기준 비율, 0.0~1.0)
    x: float = 0.0                # 왼쪽 위 X (비율)
    y: float = 0.0                # 왼쪽 위 Y (비율)
    w: float = 0.3                # 너비 (비율)
    h: float = 0.3                # 높이 (비율)
    # 스타일
    color: str = "#FF4444"        # 테두리 색상
    thickness: int = 3            # 테두리 두께 (px)
    opacity: float = 0.9          # 투명도
    label: str = ""               # 라벨 텍스트 (박스 위에 표시)
    fade: float = PIP_FADE


# ──────────────────────────────────────────
# 텍스트 콜아웃 이미지 생성 (Pillow)
# ──────────────────────────────────────────
def _hex_to_rgba(hex_color: str, opacity: float = 1.0) -> tuple[int, int, int, int]:
    """#RRGGBB → (R, G, B, A)"""
    rgb = bytes.fromhex(hex_color.lstrip("#"))
    return (rgb[0], rgb[1], rgb[2], int(opacity * 255))


def generate_callout_image(callout: TextCallout, output_path: str,
                           vid_resolution: tuple[int, int]) -> str:
    """TextCallout → 투명 배경 PNG 이미지 생성"""
    from PIL import Image, ImageDraw, ImageFont

    vid_w, vid_h = vid_resolution
    font_path = FONT_PATH

    # 폰트 로드
    try:
        font = ImageFont.truetype(font_path, callout.font_size)
        title_font = ImageFont.truetype(font_path, int(callout.font_size * 1.3))
    except OSError:
        font = ImageFont.load_default()
        title_font = font

    # 텍스트 크기 계산
    temp_img = Image.new("RGBA", (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)

    lines = callout.text.split("\n")
    max_text_w = 0
    line_heights = []

    for line in lines:
        bbox = temp_draw.textbbox((0, 0), line, font=font)
        max_text_w = max(max_text_w, bbox[2] - bbox[0])
        line_heights.append(bbox[3] - bbox[1])

    title_h = 0
    title_w = 0
    if callout.title:
        tbbox = temp_draw.textbbox((0, 0), callout.title, font=title_font)
        title_w = tbbox[2] - tbbox[0]
        title_h = tbbox[3] - tbbox[1] + callout.padding // 2
        max_text_w = max(max_text_w, title_w)

    # 이미지 크기 결정
    pad = callout.padding
    accent_w = 6 if callout.accent_bar else 0
    content_w = min(max_text_w, callout.max_width)
    img_w = content_w + pad * 2 + accent_w
    line_spacing = 6
    text_block_h = sum(line_heights) + line_spacing * (len(lines) - 1)
    img_h = title_h + text_block_h + pad * 2

    # 이미지 생성 (투명 배경)
    img = Image.new("RGBA", (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 배경 박스 (둥근 모서리)
    bg_rgba = _hex_to_rgba(callout.bg_color, callout.bg_opacity)
    r = callout.border_radius
    draw.rounded_rectangle(
        [(0, 0), (img_w - 1, img_h - 1)],
        radius=r,
        fill=bg_rgba
    )

    # 왼쪽 강조 바
    if callout.accent_bar:
        accent_rgba = _hex_to_rgba(callout.accent_color, 1.0)
        draw.rounded_rectangle(
            [(0, r), (accent_w - 1, img_h - 1 - r)],
            radius=0,
            fill=accent_rgba
        )
        # 상단/하단 연결
        draw.rectangle([(0, r), (accent_w - 1, r + accent_w)], fill=accent_rgba)
        draw.rectangle([(0, img_h - 1 - r - accent_w), (accent_w - 1, img_h - 1 - r)], fill=accent_rgba)

    # 제목 텍스트
    x_start = pad + accent_w
    y_cursor = pad

    if callout.title:
        title_rgba = _hex_to_rgba(callout.title_color, 1.0)
        draw.text((x_start, y_cursor), callout.title, fill=title_rgba, font=title_font)
        y_cursor += title_h

    # 본문 텍스트
    text_rgba = _hex_to_rgba(callout.text_color, 1.0)
    for i, line in enumerate(lines):
        # ★ 별표로 시작하는 줄은 강조색으로
        if line.startswith("★") or line.startswith("※"):
            color = _hex_to_rgba(callout.accent_color, 1.0)
        else:
            color = text_rgba
        draw.text((x_start, y_cursor), line, fill=color, font=font)
        y_cursor += line_heights[i] + line_spacing

    img.save(output_path)
    return output_path


def generate_highlight_image(highlight: HighlightBox, output_path: str,
                             vid_resolution: tuple[int, int]) -> str:
    """HighlightBox → 투명 배경 PNG (전체 화면 크기, 해당 영역에 테두리)"""
    from PIL import Image, ImageDraw, ImageFont

    vid_w, vid_h = vid_resolution

    img = Image.new("RGBA", (vid_w, vid_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 박스 좌표 계산 (비율 → 픽셀)
    bx = int(highlight.x * vid_w)
    by = int(highlight.y * vid_h)
    bw = int(highlight.w * vid_w)
    bh = int(highlight.h * vid_h)

    color_rgba = _hex_to_rgba(highlight.color, highlight.opacity)
    t = highlight.thickness

    # 테두리 그리기 (사각형)
    for i in range(t):
        draw.rectangle(
            [(bx + i, by + i), (bx + bw - i, by + bh - i)],
            outline=color_rgba
        )

    # 라벨
    if highlight.label:
        try:
            label_font = ImageFont.truetype(FONT_PATH, 28)
        except OSError:
            label_font = ImageFont.load_default()

        lbbox = draw.textbbox((0, 0), highlight.label, font=label_font)
        lw = lbbox[2] - lbbox[0]
        lh = lbbox[3] - lbbox[1]

        # 라벨 배경
        label_bg = _hex_to_rgba(highlight.color, 0.85)
        label_pad = 8
        draw.rounded_rectangle(
            [(bx, by - lh - label_pad * 2 - 4),
             (bx + lw + label_pad * 2, by - 4)],
            radius=6,
            fill=label_bg
        )
        draw.text((bx + label_pad, by - lh - label_pad - 2),
                  highlight.label, fill=(255, 255, 255, 255), font=label_font)

    img.save(output_path)
    return output_path


# ──────────────────────────────────────────
# 클립별 오버레이 설정
# ──────────────────────────────────────────
# TODO: 타이밍을 직접 지정해주세요!
# start/end (PiP/TextCallout/HighlightBox) 또는 at (Insert)의 초 단위 값을 수정하세요.
OVERLAYS: dict[str, list] = {
    # ─── 004_blender_interface.mov ─── 인터페이스 설명
    "004_blender_interface.mov": [
        # 1) Blender 레이블 스크린샷 — 전체화면 인서트 (영상 잠시 멈추고 이미지 표시)
        InsertOverlay(
            image="blender_labeled.png",     # 레이블된 Blender 스크린샷
            at=10.0,                          # ← 삽입 시점 (초) — 수정 필요!
            duration=5,
            fade=0.5,
        ),

        # 2) 뷰포트 영역 하이라이트
        HighlightBox(
            start=16.0, end=22.0,            # ← 수정 필요!
            x=0.01, y=0.05, w=0.75, h=0.88,  # 3D Viewport 영역 (대략)
            color="#00FF88",
            thickness=4,
            label="1. 3D Viewport (뷰포트)",
        ),

        # 3) 아웃라이너 영역 하이라이트
        HighlightBox(
            start=23.0, end=29.0,            # ← 수정 필요!
            x=0.77, y=0.05, w=0.22, h=0.20,  # Outliner 영역 (대략)
            color="#FF44FF",
            thickness=4,
            label="2. Outliner (아웃라이너)",
        ),

        # 4) 텍스트 콜아웃 — 자동 생성
        TextCallout(
            title="인터페이스",
            text="= 모든 작업공간을 이루는 말\n\n★뷰포트: 오브젝트를 실시간으로 보는 공간\n★아웃라이너: 오브젝트를 정리 및 관리\n★속성창: 오브젝트에 조작 및 설정",
            start=30.0, end=40.0,            # ← 수정 필요!
            position="top-right",
            font_size=28,
            accent_color="#FF4444",
        ),
    ],

    # ─── 005_blender_interface_2.mov ─── 인터페이스 2
    "005_blender_interface_2.mov": [
        # 1) 요약 필기 이미지 — PiP (화면 위 작은 창)
        PipOverlay(
            image="summary_note.png",         # 요약 필기 이미지
            start=5.0,                        # ← 수정 필요!
            end=15.0,                         # ← 수정 필요!
            position="top-right",
            scale=0.35,
        ),

        # 2) 속성창 설명 텍스트 콜아웃
        TextCallout(
            title="속성창 (Properties)",
            text="오브젝트의 위치/회전/크기 등\n세부 설정을 조작하는 공간",
            start=20.0, end=28.0,            # ← 수정 필요!
            position="bottom-left",
            font_size=28,
            accent_color="#FFB800",
        ),
    ],
}


# ──────────────────────────────────────────
# 유틸리티
# ──────────────────────────────────────────
def get_video_resolution(video_path: str) -> tuple[int, int]:
    result = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-of", "csv=p=0", video_path],
        capture_output=True, text=True
    )
    parts = result.stdout.strip().split(",")
    if len(parts) == 2:
        return int(parts[0]), int(parts[1])
    return (1920, 1080)


def get_video_duration(video_path: str) -> float:
    result = subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", video_path],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())


def has_audio(video_path: str) -> bool:
    result = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=index",
         "-of", "csv=p=0", video_path],
        capture_output=True, text=True
    )
    return bool(result.stdout.strip())


def get_pip_position(position: str, vid_w: int, vid_h: int,
                     pip_w: str, pip_h: str, margin: int) -> tuple[str, str]:
    """PiP 위치 계산 (FFmpeg 표현식 반환)"""
    positions = {
        "top-left":     (str(margin), str(margin)),
        "top-right":    (f"{vid_w}-{pip_w}-{margin}", str(margin)),
        "bottom-left":  (str(margin), f"{vid_h}-{pip_h}-{margin}"),
        "bottom-right": (f"{vid_w}-{pip_w}-{margin}", f"{vid_h}-{pip_h}-{margin}"),
        "center":       (f"({vid_w}-{pip_w})/2", f"({vid_h}-{pip_h})/2"),
    }
    return positions.get(position, positions["top-right"])


# ──────────────────────────────────────────
# PiP 오버레이 처리
# ──────────────────────────────────────────
def apply_pip(video_path: str, overlay: PipOverlay, output_path: str,
              resolution: tuple[int, int], dry_run: bool = False) -> str:
    """영상 위에 PiP 이미지 오버레이"""
    if overlay._abs_path:
        img_path = overlay.image
    else:
        img_path = str(IMAGES_DIR / overlay.image)
    vid_w, vid_h = resolution
    pip_w = int(vid_w * overlay.scale)

    # PiP 위치
    x, y = get_pip_position(
        overlay.position, vid_w, vid_h,
        "overlay_w", "overlay_h", PIP_MARGIN
    )

    # 페이드 효과가 있는 오버레이 알파
    fade = overlay.fade
    t_start = overlay.start
    t_end = overlay.end

    # 필터 체인:
    # [1] 이미지 스케일 → [1] 알파 페이드 → [0][1] 오버레이
    filter_parts = []

    # 이미지 스케일 + 알파 처리
    img_filter = f"[1:v]scale={pip_w}:-1,format=rgba"

    # 테두리 추가 (drawbox)
    if overlay.border > 0:
        b = overlay.border
        img_filter += f",pad=iw+{b*2}:ih+{b*2}:{b}:{b}:color=white@0.8"

    # 페이드 인/아웃 (알파 채널)
    img_filter += (
        f",colorchannelmixer=aa="
        f"if(lt(t\\,{t_start})\\,0\\,"
        f"if(lt(t\\,{t_start+fade})\\,(t-{t_start})/{fade}\\,"
        f"if(lt(t\\,{t_end-fade})\\,1\\,"
        f"if(lt(t\\,{t_end})\\,({t_end}-t)/{fade}\\,"
        f"0))))"
    )
    img_filter += "[pip]"
    filter_parts.append(img_filter)

    # 오버레이 적용 (enable로 시간 제한)
    overlay_filter = (
        f"[0:v][pip]overlay={x}:{y}:"
        f"enable='between(t,{t_start},{t_end})'"
    )
    filter_parts.append(overlay_filter)

    filter_complex = ";".join(filter_parts)

    cmd = [
        FFMPEG, "-y",
        "-i", video_path,
        "-loop", "1", "-i", img_path,
        "-filter_complex", filter_complex,
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-r", str(FPS),
        output_path
    ]

    if dry_run:
        print(f"  [DRY RUN] ffmpeg command:")
        print(f"    {' '.join(cmd)}")
        return output_path

    print(f"  🖼️  PiP: {overlay.image} @ {overlay.position} ({t_start}s~{t_end}s)")
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


# ──────────────────────────────────────────
# 전체화면 인서트 처리
# ──────────────────────────────────────────
def apply_insert(video_path: str, overlay: InsertOverlay, output_path: str,
                 resolution: tuple[int, int], tmpdir: str,
                 dry_run: bool = False) -> str:
    """영상 중간에 전체화면 이미지 인서트 삽입"""
    img_path = str(IMAGES_DIR / overlay.image)
    vid_w, vid_h = resolution
    vid_duration = get_video_duration(video_path)
    has_aud = has_audio(video_path)

    split_time = min(overlay.at, vid_duration)
    fade = overlay.fade
    dur = overlay.duration

    # 1. 영상을 split_time 기준으로 앞/뒤 분리
    part1 = os.path.join(tmpdir, "part1.mp4")
    part2 = os.path.join(tmpdir, "part2.mp4")

    cmd_split1 = [
        FFMPEG, "-y", "-i", video_path,
        "-t", str(split_time),
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac" if has_aud else "aac",
        "-r", str(FPS),
        part1
    ]

    cmd_split2 = [
        FFMPEG, "-y", "-i", video_path,
        "-ss", str(split_time),
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac" if has_aud else "aac",
        "-r", str(FPS),
        part2
    ]

    # 2. 이미지 → 인서트 영상 (페이드 포함)
    insert_video = os.path.join(tmpdir, "insert.mp4")
    vf = (
        f"scale={vid_w}:{vid_h}:force_original_aspect_ratio=decrease,"
        f"pad={vid_w}:{vid_h}:(ow-iw)/2:(oh-ih)/2:color={overlay.bg_color},"
        f"fade=t=in:st=0:d={fade},"
        f"fade=t=out:st={dur - fade}:d={fade}"
    )
    cmd_insert = [
        FFMPEG, "-y",
        "-loop", "1", "-i", img_path,
        "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
        "-t", str(dur),
        "-vf", vf,
        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "44100",
        "-r", str(FPS),
        "-shortest",
        insert_video
    ]

    # 3. 앞 + 인서트 + 뒤 합치기
    concat_list = os.path.join(tmpdir, "concat.txt")

    if dry_run:
        print(f"  [DRY RUN] Insert: {overlay.image} @ {split_time}s ({dur}s)")
        print(f"    Split video → part1 (0~{split_time}s) + part2 ({split_time}s~end)")
        print(f"    Create {dur}s insert from image")
        print(f"    Concat: part1 + insert + part2")
        return output_path

    print(f"  📸 Insert: {overlay.image} @ {split_time}s ({dur}s)")

    # 분리
    subprocess.run(cmd_split1, check=True, capture_output=True)
    subprocess.run(cmd_split2, check=True, capture_output=True)

    # 인서트 생성
    subprocess.run(cmd_insert, check=True, capture_output=True)

    # part1에 무음 추가 (필요시)
    if not has_audio(part1):
        part1_audio = os.path.join(tmpdir, "part1_audio.mp4")
        subprocess.run([
            FFMPEG, "-y", "-i", part1,
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-c:v", "copy", "-c:a", "aac", "-ar", "44100", "-shortest",
            part1_audio
        ], check=True, capture_output=True)
        os.replace(part1_audio, part1)

    if not has_audio(part2):
        part2_audio = os.path.join(tmpdir, "part2_audio.mp4")
        subprocess.run([
            FFMPEG, "-y", "-i", part2,
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-c:v", "copy", "-c:a", "aac", "-ar", "44100", "-shortest",
            part2_audio
        ], check=True, capture_output=True)
        os.replace(part2_audio, part2)

    # 합치기
    with open(concat_list, "w") as f:
        f.write(f"file '{part1}'\n")
        f.write(f"file '{insert_video}'\n")
        f.write(f"file '{part2}'\n")

    subprocess.run([
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c:v", "libx264", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        output_path
    ], check=True, capture_output=True)

    return output_path


# ──────────────────────────────────────────
# 메인
# ──────────────────────────────────────────
def _prepare_overlays(overlays: list, resolution: tuple[int, int],
                      tmpdir: str) -> list:
    """TextCallout/HighlightBox → 이미지 생성 후 PipOverlay로 변환"""
    prepared = []
    for i, ov in enumerate(overlays):
        if isinstance(ov, TextCallout):
            # Pillow로 콜아웃 이미지 자동 생성
            img_name = f"_auto_callout_{i}.png"
            img_path = os.path.join(tmpdir, img_name)
            generate_callout_image(ov, img_path, resolution)
            label = ov.title if ov.title else ov.text.replace("\n", " ")
            print(f"  🔤 TextCallout 생성: {label}")

            # PipOverlay로 변환 (생성된 이미지를 직접 참조)
            pip = PipOverlay(
                image=img_path,  # 절대경로
                start=ov.start,
                end=ov.end,
                position=ov.position,
                scale=1.0,       # 이미 적절한 크기로 생성됨
                fade=ov.fade,
                border=0,
            )
            pip._abs_path = True  # 내부 플래그: 절대경로 사용
            prepared.append(pip)

        elif isinstance(ov, HighlightBox):
            # Pillow로 하이라이트 이미지 생성
            img_name = f"_auto_highlight_{i}.png"
            img_path = os.path.join(tmpdir, img_name)
            generate_highlight_image(ov, img_path, resolution)
            print(f"  📦 HighlightBox 생성: {ov.label or f'({ov.x},{ov.y})'}")

            # PipOverlay로 변환 (전체 화면 크기이므로 scale=1.0, 위치 고정)
            pip = PipOverlay(
                image=img_path,
                start=ov.start,
                end=ov.end,
                position="top-left",
                scale=1.0,
                fade=ov.fade,
                border=0,
            )
            pip._abs_path = True
            prepared.append(pip)

        else:
            prepared.append(ov)

    return prepared


def process_clip(clip_name: str, overlays: list, dry_run: bool = False):
    """클립에 모든 오버레이를 순차 적용"""
    clip_path = CLIPS_DIR / clip_name
    if not clip_path.exists():
        print(f"  ❌ 클립 없음: {clip_path}")
        return

    resolution = get_video_resolution(str(clip_path))
    print(f"\n{'='*50}")
    print(f"🎬 {clip_name} ({resolution[0]}x{resolution[1]})")
    print(f"{'='*50}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        # TextCallout/HighlightBox → 이미지 생성 + PipOverlay 변환
        prepared = _prepare_overlays(overlays, resolution, tmpdir)

        # 오버레이를 순차적으로 적용 (이전 출력이 다음 입력)
        current_input = str(clip_path)

        for i, overlay in enumerate(prepared):
            is_last = (i == len(prepared) - 1)

            if is_last:
                out = str(OUTPUT_DIR / clip_path.with_suffix(".mp4").name)
            else:
                out = os.path.join(tmpdir, f"step_{i}.mp4")

            if isinstance(overlay, PipOverlay):
                current_input = apply_pip(
                    current_input, overlay, out, resolution, dry_run
                )
            elif isinstance(overlay, InsertOverlay):
                step_tmp = os.path.join(tmpdir, f"insert_tmp_{i}")
                os.makedirs(step_tmp, exist_ok=True)
                current_input = apply_insert(
                    current_input, overlay, out, resolution, step_tmp, dry_run
                )

            if not dry_run:
                print(f"     ✅ Step {i+1}/{len(prepared)} 완료")

    if not dry_run:
        print(f"  📁 출력: {OUTPUT_DIR / clip_path.with_suffix('.mp4').name}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="영상에 이미지 오버레이 삽입")
    parser.add_argument("--dry-run", action="store_true",
                        help="FFmpeg 명령만 출력, 실행 안 함")
    parser.add_argument("--clip", type=str, default=None,
                        help="특정 클립만 처리 (예: 004)")
    parser.add_argument("--generate-only", action="store_true",
                        help="TextCallout/HighlightBox 이미지만 생성 (영상 처리 안 함)")
    args = parser.parse_args()

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # --generate-only: 텍스트 콜아웃 이미지만 생성
    if args.generate_only:
        print("📝 텍스트 콜아웃/하이라이트 이미지 생성 모드")
        for clip_name, overlays in OVERLAYS.items():
            clip_path = CLIPS_DIR / clip_name
            if clip_path.exists():
                resolution = get_video_resolution(str(clip_path))
            else:
                resolution = (1920, 1080)
            for i, ov in enumerate(overlays):
                if isinstance(ov, TextCallout):
                    out = str(IMAGES_DIR / f"{Path(clip_name).stem}_callout_{i}.png")
                    generate_callout_image(ov, out, resolution)
                    print(f"  🔤 {out}")
                elif isinstance(ov, HighlightBox):
                    out = str(IMAGES_DIR / f"{Path(clip_name).stem}_highlight_{i}.png")
                    generate_highlight_image(ov, out, resolution)
                    print(f"  📦 {out}")
        print("✅ 이미지 생성 완료!")
        return

    # 수동 이미지(PiP/Insert) 존재 확인 — TextCallout/HighlightBox는 자동 생성이므로 제외
    missing = []
    for clip_name, overlays in OVERLAYS.items():
        for ov in overlays:
            if isinstance(ov, (PipOverlay, InsertOverlay)):
                img = IMAGES_DIR / ov.image
                if not img.exists():
                    missing.append(ov.image)
    if missing:
        print(f"⚠️  누락된 이미지 ({IMAGES_DIR}):")
        for m in set(missing):
            print(f"   - {m}")
        if not args.dry_run:
            print(f"\n이미지를 넣은 후 다시 실행하세요.")
            return

    # 처리
    for clip_name, overlays in OVERLAYS.items():
        if args.clip and args.clip not in clip_name:
            continue
        process_clip(clip_name, overlays, dry_run=args.dry_run)

    print(f"\n{'='*50}")
    print(f"✅ 전체 완료! 출력: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
