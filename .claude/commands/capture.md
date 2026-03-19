---
description: "Blender 공식 문서 스크린샷 자동 캡처. 예: /capture week 4, /capture url https://docs.blender.org/..., /capture list"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*), Bash(ls:*), Bash(wc:*), mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_take_screenshot, mcp__playwright__browser_evaluate, mcp__playwright__browser_wait_for, mcp__playwright__browser_resize
---

## Context

- 프로젝트 루트: !`git rev-parse --show-toplevel 2>/dev/null`
- 캡처 스크립트: !`ls tools/capture_screenshots.py 2>/dev/null && echo "✅ 있음" || echo "❌ 없음"`
- 기존 스크린샷 수: !`find course-site/assets/images -name "*.png" 2>/dev/null | wc -l | tr -d ' '`장
- 이미지 디렉토리: !`ls -d course-site/assets/images/week* 2>/dev/null | tr '\n' ' '`

## Task

인자: `$ARGUMENTS`

---

### 모드 분기

---

#### `week {N}` — 주차별 전체 캡처

지정된 주차에 필요한 모든 Blender 공식 문서 스크린샷을 자동으로 캡처합니다.

**절차:**
1. `tools/capture_screenshots.py`의 `STEP_MAP` 딕셔너리에서 해당 주차 항목 확인
2. 매핑이 있으면: `python3 tools/capture_screenshots.py --week {N}` 실행
3. 매핑이 없으면: curriculum.js에서 해당 주차 step들의 참고 자료 URL 추출 → Playwright로 직접 캡처

**Playwright 직접 캡처 절차:**
1. Blender docs URL 열기 (1280x900 viewport)
2. 사이드바/네비게이션/헤더/푸터 숨기기 (아래 JS 실행)
3. 배경색 #111로 변경
4. 콘텐츠 영역 max-width 860px, padding 32px
5. 전체 페이지 스크린샷 → `course-site/assets/images/week{NN:02d}/{step-name}.png`

**사이드바 제거 JS:**
```javascript
(() => {
    const hide = ['[class*="sidebar"]', '[class*="toc"]', 'nav', 'header', 'footer',
                  '.mobile-header', '.related-pages', '.prev-next'];
    hide.forEach(sel => document.querySelectorAll(sel).forEach(el => { el.style.display = 'none'; }));
    const art = document.querySelector('article') || document.querySelector('.bd-content') || document.body;
    art.style.cssText += 'max-width:860px;margin:0 auto;padding:32px;';
    document.body.style.background = '#111';
    return 'ok';
})()
```

6. 캡처 후 curriculum.js의 해당 step에 `image` 필드 자동 업데이트
7. 결과 리포트: 성공/실패/스킵 수

---

#### `url {URL} [--name filename]` — 단일 URL 캡처

특정 Blender 문서 URL 하나를 캡처합니다.

**절차:**
1. URL 유효성 확인 (docs.blender.org 도메인)
2. Playwright로 페이지 열기
3. 사이드바 제거 JS 실행
4. 스크린샷 저장
5. `--name`이 없으면 URL 경로에서 파일명 자동 생성

**저장 위치**: `course-site/assets/images/` (--name으로 지정하거나, URL에서 추론)

---

#### `list` — 캡처 현황 리포트

주차별 캡처 현황을 테이블로 출력합니다.

**출력:**
```
Week 03: 5 steps, 3 images (2 missing)
  ✅ base-form.png
  ✅ mirror-modifier.png
  ❌ subdivision-surface.png (step image 없음)
  ✅ array-boolean-detail.png
  ❌ bevel-weighted-normal.png (step image 없음)
```

**절차:**
1. curriculum.js에서 모든 주차의 step.image 필드 확인
2. 실제 파일 존재 여부 대조
3. 누락된 이미지 목록 표시

---

#### `dry-run {week}` — 캡처 계획만 출력

실제 캡처 없이 URL 목록과 저장 경로만 미리 보여줍니다.

---

#### 인자 없음 — 도움말

사용 가능한 모든 모드와 예시를 출력합니다.

---

### STEP_MAP 매핑 확인

기존 매핑은 `tools/capture_screenshots.py`의 `STEP_MAP` 딕셔너리에 정의됨:

```python
STEP_MAP = {
    (week_num, step_index): ("filename", "blender_docs_url"),
    ...
}
```

매핑에 없는 주차/스텝은 curriculum.js의 `references[]` URL을 fallback으로 사용.

### Week 3 도구/모디파이어 개별 레퍼런스

툴 이름은 Blender 공식 문서 페이지 제목 그대로 사용.

#### Edit Mode 기본 도구

| Blender 공식 이름 | 파일명 | 문서 URL |
|------------------|--------|---------|
| Extrude Region | `base-form.png` | `.../modeling/meshes/tools/extrude_region.html` |
| Loop Cut | `loop-cut.png` | `.../modeling/meshes/tools/loop.html` |
| Inset Faces | `inset-faces.png` | `.../modeling/meshes/editing/face/inset_faces.html` |
| Bevel Edges | `bevel-tool.png` | `.../modeling/meshes/editing/edge/bevel.html` |

#### Generate Modifiers

| Blender 공식 이름 | 파일명 | 문서 URL |
|------------------|--------|---------|
| Mirror Modifier | `mirror-modifier.png` | `.../modeling/modifiers/generate/mirror.html` |
| Subdivision Surface Modifier | `subdivision-surface.png` | `.../modeling/modifiers/generate/subdivision_surface.html` |
| Solidify Modifier | `solidify-modifier.png` | `.../modeling/modifiers/generate/solidify.html` |
| Array Modifier | `array-modifier.png` | `.../modeling/modifiers/generate/array.html` |
| Boolean Modifier | `array-boolean-detail.png` | `.../modeling/modifiers/generate/booleans.html` |
| Bevel Modifier | `bevel-weighted-normal.png` | `.../modeling/modifiers/generate/bevel.html` |
| Decimate Modifier | `decimate.png` | `.../modeling/modifiers/generate/decimate.html` |

#### Deform Modifiers

| Blender 공식 이름 | 파일명 | 문서 URL |
|------------------|--------|---------|
| Simple Deform Modifier | `simple-deform.png` | `.../modeling/modifiers/deform/simple_deform.html` |

#### Normals Modifiers

| Blender 공식 이름 | 파일명 | 문서 URL |
|------------------|--------|---------|
| Weighted Normal Modifier | `weighted-normal.png` | `.../modeling/modifiers/normals/weighted_normal.html` |

---

### Blender 공식 문서 URL 패턴

| 카테고리 | URL 패턴 |
|----------|----------|
| Generate 모디파이어 | `https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/{name}.html` |
| Deform 모디파이어 | `https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/{name}.html` |
| Normals 모디파이어 | `https://docs.blender.org/manual/en/latest/modeling/modifiers/normals/{name}.html` |
| Mesh 편집 도구 (Face) | `https://docs.blender.org/manual/en/latest/modeling/meshes/editing/face/{tool}.html` |
| Mesh 편집 도구 (Edge) | `https://docs.blender.org/manual/en/latest/modeling/meshes/editing/edge/{tool}.html` |
| Mesh 도구 (toolbar) | `https://docs.blender.org/manual/en/latest/modeling/meshes/tools/{tool}.html` |
| Shader 노드 | `https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/{name}.html` |
| 에디터 | `https://docs.blender.org/manual/en/latest/editors/{editor}.html` |
| 애니메이션 | `https://docs.blender.org/manual/en/latest/animation/{topic}/introduction.html` |

### 이미지 저장 규칙

- **디렉토리**: `course-site/assets/images/week{NN:02d}/`
- **파일명**: kebab-case, `.png` (예: `mirror-modifier.png`, `principled-bsdf.png`)
- **해상도**: 1280x900 viewport, full-page: false (첫 화면만)
- **배경**: #111 (dark theme 맞춤)

### 핵심 파일

| 파일 | 역할 |
|------|------|
| `tools/capture_screenshots.py` | 기존 캡처 스크립트 (Playwright 기반) |
| `course-site/data/curriculum.js` | step.image 필드 소스 |
| `course-site/assets/images/weekNN/` | 캡처 이미지 저장 디렉토리 |

## 실행 로그
실행 완료 시 아래 형식으로 기록:
```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=$MODE result=$RESULT target=$TARGET" >> .claude/skill-logs/capture.log
```

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)
