# Show Me Card QA Audit System Design

> Created: 2026-03-24
> Status: Approved

## Goal

62개 Show Me 카드의 품질을 자동으로 검증하는 Playwright 기반 감사 스크립트를 만든다.
결과는 JSON 보고서로 출력하고, 선택적으로 탭별 스크린샷을 캡처한다.

## Scope

- 전체 62개 카드 (`_registry.js` 기반)
- 4개 검증 영역: 캔버스 렌더링, 콘텐츠 정확성, 인터랙션/UX, 시각적 일관성
- 보고서만 생성 (자동 수정 없음)

## Architecture

```
tools/showme_card_audit.py          ← 메인 감사 스크립트
claudedocs/showme-audit-report.json ← 감사 결과 JSON
claudedocs/screenshots/<card-id>/   ← 탭별 스크린샷 (선택)
```

## Checklist (15 checks per card)

### A. Canvas Rendering
- A1: Page load success (DOM ready, no crash)
- A2: demoCanvas exists and is non-empty (pixel data > 0)
- A3: before/after canvases rendered (pixel data in each)
- A4: Scenario button click changes canvas (pixel hash diff)

### B. Content Accuracy
- B1: All 4 tabs exist (`[data-tab]` count == 4)
- B2: Each panel has text content (innerText length > 0)
- B3: Keyboard shortcuts displayed (`.kbd` elements, if applicable)
- B4: External links valid (`.doc-ref a` href format check)

### C. Interaction & UX
- C1: Tab switching works (click each tab → panel visible)
- C2: Quiz feedback (`.quiz-option` click → `.quiz-feedback` shown)
- C3: Slider/input response (value change → label update)
- C4: No console errors (collect page console errors)

### D. Visual Consistency
- D1: CSS variable usage (detect hardcoded hex in `<style>`)
- D2: Per-tab screenshots (4 tabs × 62 cards = 248 images)
- D3: No viewport overflow (scrollWidth > clientWidth)

## Report Format (JSON)

```json
{
  "audit_date": "ISO timestamp",
  "total_cards": 62,
  "summary": { "pass": N, "warn": N, "fail": N },
  "cards": [{
    "id": "card-id",
    "label": "한글 라벨",
    "week": 3,
    "status": "pass|warn|fail",
    "checks": { "A1_page_load": "pass", ... },
    "errors": ["[warn] C4: console warning: ..."],
    "screenshot_dir": "claudedocs/screenshots/card-id/"
  }]
}
```

## CLI

```bash
python tools/showme_card_audit.py                    # full audit
python tools/showme_card_audit.py --cards extrude,inset  # specific cards
python tools/showme_card_audit.py --screenshots      # with screenshots
```

## Dependencies

- playwright (already used in existing E2E tests)
- No new dependencies needed
