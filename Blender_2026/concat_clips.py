#!/usr/bin/env python3
"""
강의 클립 합치기 스크립트
사용법: python3 concat_clips.py
"""

import os
import subprocess
import tempfile
from pathlib import Path

# ──────────────────────────────────────────
# 설정
# ──────────────────────────────────────────
CLIPS_DIR = Path(__file__).parent / "Blender_tutorial_clips"
OUTPUT_FILE = Path(__file__).parent / "output_final.mp4"

TITLE_DURATION = 3       # 섹션 타이틀 카드 길이 (초)
FADE_DURATION = 0.4      # 페이드 인/아웃 길이 (초)
FONT_PATH = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"

TITLE_BG_COLOR = "0x1a1a2e"   # 짙은 남색 배경
TITLE_TEXT_COLOR = "white"
WEEK_LABEL = "Week 02 | Blender 기초"  # 상단 소제목

# ──────────────────────────────────────────
# 파일명 규칙: 01_설치.mp4, 02_UI구조.mp4 등
# 섹션 제목은 _ 뒤의 텍스트를 사용
# ──────────────────────────────────────────

def get_section_title(filename: str) -> str:
    """01_설치환경.mp4 → '설치환경'"""
    stem = Path(filename).stem  # 01_설치환경
    parts = stem.split("_", 1)
    if len(parts) == 2:
        return parts[1].replace("_", " ")
    return stem


def make_title_card(title: str, output_path: str, resolution: tuple = (1920, 1080)):
    """섹션 타이틀 카드 영상 생성"""
    w, h = resolution
    fade = FADE_DURATION
    dur = TITLE_DURATION

    # 배경 위에 텍스트 두 줄: 소제목(위) + 섹션 제목(아래)
    filter_complex = (
        f"color=c={TITLE_BG_COLOR}:size={w}x{h}:duration={dur}:rate=30,"
        f"drawtext=fontfile='{FONT_PATH}'"
        f":text='{WEEK_LABEL}'"
        f":fontcolor=0xaaaaaa:fontsize=36"
        f":x=(w-text_w)/2:y=(h/2)-80,"
        f"drawtext=fontfile='{FONT_PATH}'"
        f":text='{title}'"
        f":fontcolor={TITLE_TEXT_COLOR}:fontsize=72:bold=1"
        f":x=(w-text_w)/2:y=(h/2),"
        f"fade=t=in:st=0:d={fade},"
        f"fade=t=out:st={dur - fade}:d={fade}"
    )

    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", filter_complex,
        "-t", str(dur),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-an",
        output_path
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def get_video_resolution(video_path: str) -> tuple:
    """영상 해상도 감지"""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-of", "csv=p=0", video_path],
        capture_output=True, text=True
    )
    parts = result.stdout.strip().split(",")
    if len(parts) == 2:
        return int(parts[0]), int(parts[1])
    return (1920, 1080)


def main():
    # 클립 파일 목록 (번호 순 정렬)
    clips = sorted([
        f for f in CLIPS_DIR.iterdir()
        if f.suffix.lower() in (".mp4", ".mov", ".mkv")
    ])

    if not clips:
        print(f"❌ 클립 없음: {CLIPS_DIR}")
        print("   파일명 규칙: 01_설치.mp4, 02_UI구조.mp4 ...")
        return

    print(f"📂 클립 {len(clips)}개 발견:")
    for c in clips:
        print(f"   {c.name}")

    # 첫 번째 클립에서 해상도 감지
    resolution = get_video_resolution(str(clips[0]))
    print(f"\n📐 해상도: {resolution[0]}x{resolution[1]}")

    with tempfile.TemporaryDirectory() as tmpdir:
        segment_files = []

        for clip in clips:
            title = get_section_title(clip.name)
            print(f"\n🎬 처리 중: {clip.name} → 타이틀: '{title}'")

            # 타이틀 카드 생성
            title_path = os.path.join(tmpdir, f"title_{clip.stem}.mp4")
            make_title_card(title, title_path, resolution)
            segment_files.append(title_path)

            # 원본 클립을 해상도/코덱 통일
            normalized_path = os.path.join(tmpdir, f"norm_{clip.stem}.mp4")
            subprocess.run([
                "ffmpeg", "-y", "-i", str(clip),
                "-vf", f"scale={resolution[0]}:{resolution[1]}",
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-ar", "44100",
                normalized_path
            ], check=True, capture_output=True)
            segment_files.append(normalized_path)

        # concat 목록 파일 작성
        concat_list = os.path.join(tmpdir, "concat.txt")
        with open(concat_list, "w") as f:
            for seg in segment_files:
                f.write(f"file '{seg}'\n")

        # 최종 합치기
        print(f"\n⏳ 최종 합치는 중...")
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c:v", "libx264", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            str(OUTPUT_FILE)
        ], check=True)

    print(f"\n✅ 완료: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
