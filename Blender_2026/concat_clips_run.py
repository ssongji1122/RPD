#!/usr/bin/env python3
"""
강의 클립 개별 처리 스크립트 (타이틀 카드 + 정규화)
각 클립 앞에 타이틀 카드를 붙여 세그먼트별 폴더에 저장합니다.

사용법: python3 concat_clips_run.py
출력:   output/week02/A_설치_시작/01_blender_download.mp4 ...
"""

import os
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ──────────────────────────────────────────
# 설정
# ──────────────────────────────────────────
CLIPS_DIR = Path(__file__).parent / "Blender_tutorial_clips"
OUTPUT_DIR = Path(__file__).parent / "output" / "week02"

TITLE_DURATION = 3       # 타이틀 카드 길이 (초)
FADE_DURATION = 0.4      # 페이드 인/아웃 길이 (초)
FONT_PATH = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"

TITLE_BG_COLOR = (0, 0, 0)
TITLE_TEXT_COLOR = (255, 255, 255)
SUBTITLE_COLOR = (170, 170, 170)
WEEK_LABEL = "Week 02 | Blender 기초"

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"
FPS = 30

# 5-세그먼트 구성: (폴더명, 세그먼트 제목, 클립 번호 목록)
SEGMENTS = [
    ("A_설치_시작",        "A. 설치 & 시작",        [1, 2, 3]),
    ("B_인터페이스_도구",   "B. 인터페이스 & 도구",   [4, 5, 6]),
    ("C_오브젝트_기본조작", "C. 오브젝트 기본 조작",  [7, 8, 9]),
    ("D_Extrude_Bevel",   "D. Extrude & Bevel",    [10, 11]),
    ("E_LoopCut_Knife",   "E. LoopCut & Knife",    [12, 13, 14]),
]

# ──────────────────────────────────────────


def get_section_title(filename: str) -> str:
    """001_blender_download.mov → 'blender download'"""
    stem = Path(filename).stem
    parts = stem.split("_", 1)
    if len(parts) == 2:
        return parts[1].replace("_", " ")
    return stem


def make_title_card(title: str, output_path: str, resolution: tuple):
    """Pillow로 타이틀 이미지 생성 → ffmpeg로 영상 변환"""
    w, h = resolution
    img = Image.new("RGB", (w, h), TITLE_BG_COLOR)
    draw = ImageDraw.Draw(img)

    subtitle_size = max(36, int(h * 0.034))
    title_size = max(72, int(h * 0.068))

    font_subtitle = ImageFont.truetype(FONT_PATH, subtitle_size)
    font_title = ImageFont.truetype(FONT_PATH, title_size)

    # 소제목 (위)
    sub_bbox = draw.textbbox((0, 0), WEEK_LABEL, font=font_subtitle)
    sub_w = sub_bbox[2] - sub_bbox[0]
    draw.text(((w - sub_w) / 2, h / 2 - title_size - subtitle_size),
              WEEK_LABEL, fill=SUBTITLE_COLOR, font=font_subtitle)

    # 섹션 제목 (아래)
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((w - title_w) / 2, h / 2 - title_size / 2 + 10),
              title, fill=TITLE_TEXT_COLOR, font=font_title)

    img_path = output_path.replace(".mp4", ".png")
    img.save(img_path)

    fade = FADE_DURATION
    cmd = [
        FFMPEG, "-y",
        "-loop", "1", "-i", img_path,
        "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
        "-t", str(TITLE_DURATION),
        "-vf", f"fade=t=in:st=0:d={fade},fade=t=out:st={TITLE_DURATION - fade}:d={fade}",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-ar", "44100",
        "-r", str(FPS),
        "-shortest",
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def has_audio(video_path: str) -> bool:
    """영상에 오디오 스트림이 있는지 확인"""
    result = subprocess.run(
        [FFPROBE, "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=index",
         "-of", "csv=p=0", video_path],
        capture_output=True, text=True
    )
    return bool(result.stdout.strip())


def get_video_resolution(video_path: str) -> tuple:
    """영상 해상도 감지"""
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


def process_clip(clip: Path, output_path: Path, resolution: tuple, tmpdir: str):
    """개별 클립: 타이틀 카드 + 원본 → 하나의 파일로 합치기"""
    title = get_section_title(clip.name)

    # 1. 타이틀 카드 생성
    title_path = os.path.join(tmpdir, f"title_{clip.stem}.mp4")
    make_title_card(title, title_path, resolution)

    # 2. 원본 정규화 (해상도/코덱 통일, 무음 추가)
    normalized_path = os.path.join(tmpdir, f"norm_{clip.stem}.mp4")
    w, h = resolution
    if has_audio(str(clip)):
        cmd_norm = [
            FFMPEG, "-y", "-i", str(clip),
            "-vf", f"scale={w}:{h}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-ar", "44100",
            "-r", str(FPS),
            normalized_path
        ]
    else:
        cmd_norm = [
            FFMPEG, "-y", "-i", str(clip),
            "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
            "-vf", f"scale={w}:{h}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-ar", "44100",
            "-r", str(FPS),
            "-shortest",
            normalized_path
        ]
    subprocess.run(cmd_norm, check=True, capture_output=True)

    # 3. 타이틀 + 본영상 합치기
    concat_list = os.path.join(tmpdir, f"concat_{clip.stem}.txt")
    with open(concat_list, "w") as f:
        f.write(f"file '{title_path}'\n")
        f.write(f"file '{normalized_path}'\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        FFMPEG, "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list,
        "-c:v", "libx264", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(output_path)
    ], check=True, capture_output=True)


def main():
    # 전체 클립 목록 → 번호 매핑
    all_clips = sorted([
        f for f in CLIPS_DIR.iterdir()
        if f.suffix.lower() in (".mp4", ".mov", ".mkv")
    ])

    clip_map = {}
    for clip in all_clips:
        num_str = clip.stem.split("_", 1)[0]
        try:
            clip_map[int(num_str)] = clip
        except ValueError:
            continue

    if not clip_map:
        print(f"❌ 클립 없음: {CLIPS_DIR}")
        return

    # 누락 클립 확인
    for folder, seg_title, clip_nums in SEGMENTS:
        missing = [n for n in clip_nums if n not in clip_map]
        if missing:
            print(f"⚠️  {seg_title}: 클립 {missing} 누락")
            return

    total = sum(len(nums) for _, _, nums in SEGMENTS)
    print(f"📂 총 {total}개 클립 → {len(SEGMENTS)}개 세그먼트 폴더")
    for folder, seg_title, clip_nums in SEGMENTS:
        names = [clip_map[n].name for n in clip_nums]
        print(f"   {seg_title}: {', '.join(names)}")

    # 첫 클립 기준 해상도
    first_clip = clip_map[min(clip_map)]
    resolution = get_video_resolution(str(first_clip))
    print(f"\n📐 해상도: {resolution[0]}x{resolution[1]}")

    # 출력 디렉토리 준비
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        for folder, seg_title, clip_nums in SEGMENTS:
            seg_dir = OUTPUT_DIR / folder
            seg_dir.mkdir(parents=True, exist_ok=True)

            print(f"\n{'='*50}")
            print(f"📌 {seg_title}")
            print(f"   → {seg_dir}")
            print(f"{'='*50}")

            for clip_num in clip_nums:
                clip = clip_map[clip_num]
                # 출력 파일명: 01_blender_download.mp4
                out_name = f"{clip_num:02d}_{clip.stem.split('_', 1)[1]}.mp4"
                out_path = seg_dir / out_name

                print(f"  🎬 {clip.name} → {out_name}")
                process_clip(clip, out_path, resolution, tmpdir)
                print(f"     ✅ 완료")

    print(f"\n✅ 전체 완료! 출력: {OUTPUT_DIR}")
    # 결과 요약
    for folder, seg_title, clip_nums in SEGMENTS:
        seg_dir = OUTPUT_DIR / folder
        files = sorted(seg_dir.glob("*.mp4"))
        print(f"   {seg_title}: {len(files)}개 파일")


if __name__ == "__main__":
    main()
