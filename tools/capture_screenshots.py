#!/usr/bin/env python3
"""
capture_screenshots.py
Blender 공식 문서 페이지에서 스텝별 스크린샷을 자동으로 찍어
course-site/assets/images/weekNN/ 에 저장합니다.

사용법:
    python3 tools/capture_screenshots.py           # 모든 주차
    python3 tools/capture_screenshots.py --week 4  # 특정 주차만
    python3 tools/capture_screenshots.py --dry-run # URL 목록만 출력
"""

import argparse
import re
from pathlib import Path

# ── Step → Doc URL 매핑 ─────────────────────────────────────────────────────
# 각 (week, step_index): (filename, doc_url)
# doc_url이 None이면 해당 스텝은 스킵 (AI 생성 도구 등 공식 문서 없음)

STEP_MAP = {
    # Week 3: 기초 모델링 1 - Modifier
    (3, 0): ("base-form",              "https://docs.blender.org/manual/en/latest/modeling/meshes/tools/extrude_region.html"),
    (3, 1): ("mirror-modifier",        "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/mirror.html"),
    (3, 2): ("subdivision-surface",    "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html"),
    (3, 3): ("array-boolean-detail",   "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html"),
    (3, 4): ("bevel-weighted-normal",  "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html"),

    # Week 4: 기초 모델링 2 - 하드서피스 디테일
    (4, 0): ("transform-apply",      "https://docs.blender.org/manual/en/latest/scene_layout/object/editing/apply.html"),
    (4, 1): ("inset-panel-detail",   "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html"),
    (4, 2): ("bevel-modifier",       "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html"),
    (4, 3): ("weighted-normal",      "https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/weighted_normal.html"),
    (4, 4): ("array-modifier",       "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/array.html"),

    # Week 5: AI 3D 생성 + Sculpting
    (5, 0): ("ai-3d-import",         None),   # AI 도구, 공식 문서 없음
    (5, 1): ("sculpt-mode",          "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/introduction/index.html"),

    # Week 6: Material & Shader Node
    (6, 0): ("material-assign",      "https://docs.blender.org/manual/en/latest/render/materials/introduction.html"),
    (6, 1): ("principled-bsdf",      "https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html"),
    (6, 2): ("shader-editor",        "https://docs.blender.org/manual/en/latest/editors/shader_editor.html"),

    # Week 7: UV Unwrapping + AI Texture
    (7, 0): ("uv-seam",              "https://docs.blender.org/manual/en/latest/modeling/meshes/uv/unwrapping/index.html"),
    (7, 1): ("uv-editor",            "https://docs.blender.org/manual/en/latest/editors/uv/introduction.html"),
    (7, 2): ("texture-paint",        None),   # AI 텍스처, 공식 문서 없음

    # Week 9: Lighting
    (9, 0): ("light-types",          "https://docs.blender.org/manual/en/latest/render/lights/light_object.html"),
    (9, 1): ("hdri-world",           "https://docs.blender.org/manual/en/latest/render/lights/world.html"),
    (9, 2): ("three-point-light",    "https://docs.blender.org/manual/en/latest/render/lights/light_object.html"),

    # Week 10: Animation
    (10, 0): ("keyframe-intro",      "https://docs.blender.org/manual/en/latest/animation/keyframes/introduction.html"),
    (10, 1): ("dope-sheet",          "https://docs.blender.org/manual/en/latest/editors/dope_sheet/introduction.html"),

    # Week 11: Rigging
    (11, 0): ("armature-structure",  "https://docs.blender.org/manual/en/latest/animation/armatures/index.html"),
    (11, 1): ("mesh-skinning",       "https://docs.blender.org/manual/en/latest/animation/armatures/skinning/index.html"),

    # Week 12: Mixamo (외부 서비스, 공식 Blender 문서 없음)
    (12, 0): ("mixamo-upload",       None),
    (12, 1): ("mixamo-import",       "https://docs.blender.org/manual/en/latest/files/import_export/index.html"),

    # Week 13: 렌더링
    (13, 0): ("cycles-eevee",        "https://docs.blender.org/manual/en/latest/render/cycles/index.html"),
    (13, 1): ("render-output",       "https://docs.blender.org/manual/en/latest/render/output/index.html"),
}

# JS: 사이드바 숨기고 콘텐츠 영역 정리
CLEAN_JS = """
() => {
    const hide = ['[class*="sidebar"]', '[class*="toc"]', 'nav', 'header', 'footer',
                  '.mobile-header', '.related-pages', '.prev-next'];
    hide.forEach(sel => document.querySelectorAll(sel).forEach(el => { el.style.display = 'none'; }));
    const art = document.querySelector('article') || document.querySelector('.bd-content') || document.body;
    art.style.cssText += 'max-width:860px;margin:0 auto;padding:32px;';
    document.body.style.background = '#111';
    return 'ok';
}
"""


def take_screenshot(page, url: str, out_path: Path) -> bool:
    """URL을 열고 메인 콘텐츠만 스크린샷 저장. 성공 여부 반환."""
    try:
        resp = page.goto(url, timeout=20_000, wait_until="networkidle")
        if resp and resp.status >= 400:
            print(f"  ⚠ {resp.status} — {url}")
            return False

        page.evaluate(CLEAN_JS)
        page.wait_for_timeout(600)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(out_path), full_page=False)
        print(f"  ✓ saved → {out_path.relative_to(Path.cwd())}")
        return True
    except Exception as e:
        print(f"  ✗ error: {e}")
        return False


def update_curriculum_image(curriculum_path: Path, week: int, step_idx: int, image_path: str) -> bool:
    """curriculum.js의 해당 step에 image 필드를 텍스트 치환으로 추가/업데이트.
    step의 "title" 필드 바로 뒤에 "image" 줄을 삽입합니다.
    이미 image 필드가 있으면 값을 교체합니다.
    """
    text = curriculum_path.read_text()

    # week 블록 내에서 step_idx 번째 step을 찾아야 함
    # 전략: "week": N 위치를 찾고, 그 이후에서 step 목록을 순회
    week_pattern = re.compile(r'"week"\s*:\s*' + str(week) + r'\b')
    wm = week_pattern.search(text)
    if not wm:
        return False

    # week 블록 시작 이후에서 "steps" 배열 내 step_idx 번째 { 를 찾기
    after_week = text[wm.start():]
    steps_match = re.search(r'"steps"\s*:\s*\[', after_week)
    if not steps_match:
        return False

    steps_start = wm.start() + steps_match.end()
    # step 블록들을 중괄호 깊이로 파싱
    depth = 0
    step_starts = []
    i = steps_start
    while i < len(text):
        ch = text[i]
        if ch == '{':
            if depth == 0:
                step_starts.append(i)
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth < 0:
                break  # steps 배열 종료
        i += 1

    if step_idx >= len(step_starts):
        return False

    step_begin = step_starts[step_idx]
    # step 블록 내에서 "title" 줄 찾기
    step_end = step_starts[step_idx + 1] if step_idx + 1 < len(step_starts) else i
    step_block = text[step_begin:step_end]

    # 이미 image 필드가 있으면 교체
    existing = re.search(r'("image"\s*:\s*")[^"]*(")', step_block)
    if existing:
        new_block = step_block[:existing.start(1)] + f'"image": "{image_path}"' + step_block[existing.end(2):]
        new_text = text[:step_begin] + new_block + text[step_begin + len(step_block):]
        curriculum_path.write_text(new_text)
        return True

    # title 필드 뒤에 image 삽입
    title_match = re.search(r'("title"\s*:\s*"[^"]*")', step_block)
    if not title_match:
        return False

    insert_pos = step_begin + title_match.end()
    indent = "        "  # curriculum.js의 들여쓰기 맞춤
    image_line = f',\n{indent}"image": "{image_path}"'
    new_text = text[:insert_pos] + image_line + text[insert_pos:]
    curriculum_path.write_text(new_text)
    return True


def main():
    parser = argparse.ArgumentParser(description="Blender docs screenshot bot")
    parser.add_argument("--week", type=int, default=None, help="특정 주차만 실행 (기본: 전체)")
    parser.add_argument("--dry-run", action="store_true", help="URL 목록만 출력, 실제 실행 안 함")
    parser.add_argument("--skip-curriculum", action="store_true", help="curriculum.js 업데이트 건너뜀")
    args = parser.parse_args()

    root = Path(__file__).parent.parent
    curriculum_path = root / "course-site" / "data" / "curriculum.js"
    images_root = root / "course-site" / "assets" / "images"

    targets = {
        k: v for k, v in STEP_MAP.items()
        if (args.week is None or k[0] == args.week) and v[1] is not None
    }

    if not targets:
        print("처리할 항목이 없습니다.")
        return

    print(f"총 {len(targets)}개 스크린샷 예정\n")

    if args.dry_run:
        for (w, s), (fname, url) in sorted(targets.items()):
            print(f"  W{w:02d}-step{s}  {fname}.png")
            print(f"          {url}")
        return

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 820})
        page = ctx.new_page()

        success = 0
        for (w, s), (fname, url) in sorted(targets.items()):
            week_str = f"week{w:02d}"
            out_path = images_root / week_str / f"{fname}.png"
            image_field = f"assets/images/{week_str}/{fname}.png"

            print(f"W{w:02d} step{s} — {fname}")
            ok = take_screenshot(page, url, out_path)
            if ok and not args.skip_curriculum:
                update_curriculum_image(curriculum_path, w, s, image_field)
            if ok:
                success += 1

        browser.close()

    print(f"\n완료: {success}/{len(targets)} 성공")


if __name__ == "__main__":
    main()
