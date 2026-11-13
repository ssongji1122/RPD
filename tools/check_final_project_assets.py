#!/usr/bin/env python3
"""기말 작품 데이터가 가리키는 자산 파일이 git에 커밋돼 있는지 확인한다.

`.gitignore`가 `*.mp4`를 일괄 제외하므로 영상은 `git add -f`로만 들어간다.
자산을 옮기거나 새로 넣을 때 강제 추가를 빠뜨리면 로컬에서는 보이지만
배포본에서는 404가 난다(2026-07 #128에서 project-21/video-03.mp4 누락).
이 검사는 `course-site/data/final-projects.js`의 모든 `assets/...` 경로를
`git ls-files` 결과와 대조해, 커밋되지 않은 경로가 있으면 실패한다.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "course-site" / "data" / "final-projects.js"
ASSET_BASE = "course-site"
ASSET_PREFIX = "assets/"
JS_ASSIGNMENT = "window.RPDFinalProjects ="


def load_data(path: Path) -> dict:
    text = path.read_text(encoding="utf-8").strip()
    if not text.startswith(JS_ASSIGNMENT):
        raise ValueError(f"{path}: '{JS_ASSIGNMENT}'로 시작하지 않습니다")
    body = text[len(JS_ASSIGNMENT):].strip().rstrip(";")
    return json.loads(body)


def iter_asset_paths(node: object) -> Iterator[str]:
    if isinstance(node, str):
        if node.startswith(ASSET_PREFIX):
            yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from iter_asset_paths(value)
    elif isinstance(node, list):
        for value in node:
            yield from iter_asset_paths(value)


def tracked_files(root: Path) -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", ASSET_BASE],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return {p for p in result.stdout.decode("utf-8").split("\0") if p}


def find_missing(data: dict, tracked: set[str]) -> list[str]:
    referenced = sorted(set(iter_asset_paths(data)))
    return [p for p in referenced if f"{ASSET_BASE}/{p}" not in tracked]


def main() -> int:
    data = load_data(DATA_FILE)
    missing = find_missing(data, tracked_files(ROOT))
    total = len(set(iter_asset_paths(data)))
    if missing:
        print(f"[final-project-assets] 커밋되지 않은 자산 {len(missing)}건 / 참조 {total}건:")
        for path in missing:
            print(f"  - {ASSET_BASE}/{path}")
        print("영상(*.mp4)은 .gitignore 대상이므로 `git add -f <경로>`로 추가해야 합니다.")
        return 1
    print(f"[final-project-assets] 참조 {total}건 모두 커밋돼 있습니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
