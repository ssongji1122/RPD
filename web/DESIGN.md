# DESIGN.md — rpd web

> **에이전트 필독.** 이 사이트는 studio.soluta 디자인 시스템을 그대로 사용합니다.
> 모든 디자인 결정은 `studio.soluta/_publish/web/DESIGN.md` 를 기준으로 합니다.

## 이 레포에서 추가/변경된 것

- 헤더 브랜드: `rpd` + `a studio.soluta series` 서브라벨
- 색상·폰트·간격 토큰: `src/styles/tokens.css` — studio.soluta와 동일
- 레이아웃: 동일한 `.wrap` / `.section` 패턴

## 빠른 참조

정본 디자인 시스템: `studio.soluta/_publish/web/DESIGN.md`
토큰 파일: `src/styles/tokens.css`

## 필수 규칙 (studio.soluta 동일)

1. `font-size: 24px` 금지 → `var(--fs-xl)` 사용
2. `#B85C38` 직접 입력 금지 → `var(--c-accent)` 사용
3. 한글 본문 `word-break: keep-all` 누락 금지
4. `.wrap` 없는 최상위 섹션 금지
