---
name: blender-showme-icons
description: 블렌더 Show Me 카드용 실제 도구 아이콘 캡처/추출/반영 스킬. Use when expanding the archive with new Blender tool cards, replacing placeholder icons with official Blender icon captures, wiring icon assets into course-site pages, or verifying updated card grids and Show Me modals in browser.
---

# Blender Show Me Icons

블렌더 오퍼레이터 아이콘을 Show Me 카드용 실제 자산으로 바꾸는 스킬입니다.

## Quick Start

1. `course-site/assets/showme/_registry.js` 에서 대상 카드의 `toolName`, `iconKey` 메타를 확인하거나 추가합니다.
2. Blender 내부 아이콘 데이터로 갤러리 스크린샷을 생성합니다.
3. 갤러리에서 투명 PNG 아이콘을 잘라 `course-site/assets/showme/icons/` 에 저장합니다.
4. `week.html` 렌더러가 PNG 자산을 우선 사용하고, 없을 때만 SVG/emoji로 폴백하게 유지합니다.
5. 브라우저에서 카드 그리드와 Show Me 모달을 다시 확인합니다.

## Project Targets

- `course-site/assets/showme/_registry.js`
- `course-site/assets/showme/icons/`
- `course-site/week.html`
- `course-site/library.html`
- `course-site/index.html`

현재 아이콘 매핑, 명령어, 검증 포인트는 [references/integration.md](references/integration.md)를 보면 됩니다.

## Capture Workflow

OS 화면 캡처보다 Blender 내부 아이콘 데이터를 우선 사용합니다.

이유:

- Blender는 공식 아이콘을 `.dat` 리소스로 함께 제공합니다.
- `bpy.app.icons.new_triangles_from_file(...)` 로 그 아이콘을 직접 읽을 수 있습니다.
- `bpy.ops.screen.screenshot(...)` 를 쓰면 macOS 화면 녹화 권한 이슈를 피할 수 있습니다.

갤러리 캡처 예시:

```bash
SHOWME_ICON_GALLERY_OUTPUT="$PWD/output/blender-showme-icons-gallery.png" \
"/Applications/Blender.app/Contents/MacOS/Blender" \
  --factory-startup \
  --python "$PWD/.claude/skills/blender-showme-icons/scripts/capture_showme_icon_gallery.py"
```

새 툴을 추가할 때는:

- `scripts/capture_showme_icon_gallery.py` 의 `ICON_SPECS` 를 업데이트합니다.
- `scripts/extract_showme_icons.py` 의 `SPECS` 를 업데이트합니다.
- `_registry.js` 의 `iconKey` 와 파일명이 일치하게 맞춥니다.

## Extraction Workflow

갤러리 스크린샷에서 실제 PNG 아이콘을 만듭니다.

```bash
python3 "$PWD/.claude/skills/blender-showme-icons/scripts/extract_showme_icons.py" \
  --gallery "$PWD/output/blender-showme-icons-gallery.png" \
  --output-dir "$PWD/course-site/assets/showme/icons"
```

이 extractor는 현재 archive 레이아웃과 아이콘 셋에 맞춰 튜닝되어 있습니다. 새로운 툴을 추가할 때마다 crop logic을 처음부터 다시 짜기보다 `SPECS` 맵만 확장하는 쪽을 우선합니다.

## Page Integration

렌더 우선순위는 다음 순서를 유지합니다.

1. `assets/showme/icons/<iconKey>.png`
2. 기존 inline SVG fallback
3. emoji fallback

학생이 아이콘이 잘 안 보인다고 하면, 먼저 badge 안 이미지 크기를 키웁니다. 라벨 두께나 카드 레이아웃은 그 다음에 만집니다.

아이콘 자산을 바꾼 뒤에는:

- asset query string을 올려 캐시를 갱신합니다.
- 카드 그리드, 브라우저 리스트, related pill, 모달 헤더를 같이 확인합니다.

## Verification

`course-site` 를 로컬에서 띄운 뒤 아래 순서로 확인합니다.

1. `week.html?week=<n>` 열기
2. 대상 Show Me 카드가 들어 있는 step 펼치기
3. Show Me 카드 묶음 스크린샷 찍기
4. 대표 카드 하나 열기
5. 모달 컨테이너 스크린샷 찍기

기존 iframe sandbox warning은 예상 가능한 경고로 취급합니다. 대신 실제 콘솔 에러, 누락된 이미지 자산, 깨진 모달 상태는 바로 확인합니다.

## Repo and Codex Sync

이 스킬은 repo 안의 버전 관리 복사본입니다. 로컬 Codex 스킬로도 같이 쓰려면 아래 스크립트로 동기화합니다.

```bash
./tools/sync-codex-skill.sh blender-showme-icons
```

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)
