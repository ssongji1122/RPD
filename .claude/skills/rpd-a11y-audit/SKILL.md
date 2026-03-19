---
name: rpd-a11y-audit
description: "접근성 점검", "a11y", "WCAG 감사" 요청 시 호출. WCAG 2.1 AA 기준 다크테마 한국어 교육 사이트 접근성 감사. Use when checking accessibility, adding ARIA attributes, or fixing keyboard navigation.
---

# RPD Accessibility Audit

## 대상
- `course-site/index.html`
- `course-site/week.html`
- `course-site/admin.html`
- `course-site/assets/tokens.css`

## WCAG 2.1 AA 기준 (이 사이트에 적용)

### 색상 대비 (1.4.3)
| 조합 | 비율 | 판정 |
|------|------|------|
| #f5f5f7 on #0a0a0a | ~19.5:1 | AAA 통과 |
| #a1a1aa on #0a0a0a | ~7.8:1 | AA 통과 |
| #d4d4d8 on #0a0a0a | ~12.5:1 | AAA 통과 |
| #8ec5ff on #0a0a0a | ~9.2:1 | AAA 통과 |
| #a1a1aa on #17181a | ~5.8:1 | AA 통과 (주의) |

**주의**: `--muted` 텍스트가 `--surface` 배경 위에 올 때 5.8:1로 AA는 통과하지만 여유 적음.

### 포커스 인디케이터 (2.4.7)
```css
*:focus-visible {
  outline: 2px solid var(--key-soft);
  outline-offset: 2px;
}
```
- 모든 인터랙티브 요소에 적용 필수
- 커스텀 체크박스(토픽 체크리스트)는 `:focus-visible + label` 필요

### 키보드 탐색 (2.1.1)
필수 탐색 순서:
1. Skip-nav 링크 (Tab 첫 번째)
2. Topbar 요소 (사이드바 토글, 진도 위젯)
3. 메인 콘텐츠 (체크리스트, 스텝, 과제)
4. Footer

### 사이드바 포커스 트래핑 (2.4.3)
사이드바 열림 시:
- 사이드바 내부로 포커스 이동
- Tab/Shift+Tab이 사이드바 내에서만 순환
- Escape로 닫기
- 닫힘 시 토글 버튼으로 포커스 복귀

### Skip Navigation (2.4.1)
```html
<a href="#practice" class="skip-nav">실습으로 건너뛰기</a>
```
```css
.skip-nav {
  position: absolute; left: -9999px;
  z-index: 999;
}
.skip-nav:focus {
  position: fixed; top: 8px; left: 8px;
  padding: 12px 20px; border-radius: 8px;
  background: var(--key); color: #fff;
  font-size: .9rem; font-weight: 600;
}
```

### 제목 위계 (1.3.1)
- h1: 페이지 제목 (Hero)
- h2: 섹션 제목 (이번 주, 실습, 과제 등)
- h3: 하위 제목 (필요시)
- **h1 → h3 건너뛰기 금지**

### 한국어 텍스트 규칙
- `word-break: keep-all` — 음절 중간 줄바꿈 방지
- 최소 폰트: 12px (0.75rem) — 한글 복잡 음절(완, 축 등) 가독성
- line-height: 1.6 이상 (권장 1.75)

### 터치 타겟 (2.5.5 / 2.5.8)
- 최소 44x44px (AAA)
- 최소 24x24px (AA)
- 토픽 체크박스 label: padding 10px+ 확보

### ARIA 속성
| 요소 | 필요 속성 |
|------|-----------|
| 진도 바 | `role="progressbar"` `aria-valuenow` `aria-valuemin="0"` `aria-valuemax` |
| 사이드바 | `aria-hidden="true"` (닫힘 시) |
| 주차 카드 링크 | `aria-label="Week N: 제목"` |
| 이모지 | `<span role="img" aria-label="설명">` 또는 장식용이면 `aria-hidden="true"` |
| 테이블 | `<caption class="sr-only">` |

### 모션 (2.3.3)
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto;
  }
}
```

### 영어 텍스트 발음 (3.1.2)
```html
<span lang="en">Robot Product Design</span>
```
한국어 TTS가 영어를 한국어 발음으로 읽는 것을 방지.

## 감사 절차

### 자동 테스트
1. Lighthouse Accessibility 점수 확인 (목표: 90+)
2. axe-core 실행 (크롬 확장)

### 수동 테스트
1. **Tab 테스트**: 페이지 처음부터 Tab으로 끝까지 이동
   - skip-nav 보이는지
   - 모든 인터랙티브 요소에 focus ring 보이는지
   - 사이드바 열림 시 트래핑 되는지
2. **스크린리더 테스트** (VoiceOver):
   - 제목 위계 올바른지 (h1 → h2 → h3)
   - 카드 링크가 간결하게 읽히는지 (aria-label)
   - 진도 변경 시 알림 (aria-live)
3. **색상 테스트**: 흑백 모드에서도 구조 파악 가능한지
4. **모션 테스트**: reduced-motion 설정 후 확인

## 참고
- WCAG 2.1 Quick Reference: https://www.w3.org/WAI/WCAG21/quickref/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- `docs/REFERENCE_RESEARCH_2026-03-15.md` (접근성 섹션)

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)
