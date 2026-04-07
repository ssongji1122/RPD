## Phase 2: Browser Verify

**실행 조건**: `week {N}`, `all` 인자가 있을 때만 실행.

### 2.0 서버 기동

preview_start 또는 기존 서버 활용. base URL: `http://localhost:8771`

### 2.1 페이지 로드 검증

대상 주차 각각에 대해:
1. `week.html?week={N}` 로드
2. 콘솔 에러 확인 (preview_console_logs) — 허용 목록: `getComputedStyle`, `sidebarToggle`
3. Noto Sans KR 폰트 로드 확인 (preview_eval: `document.fonts.check('16px "Noto Sans KR"')`)

### 2.2 이미지 렌더링 검증

```javascript
// preview_eval로 실행
[...document.querySelectorAll('img')].filter(img =>
---

  img.complete && img.naturalWidth === 0
).map(img => ({ src: img.src, alt: img.alt, step: img.closest('.practice-step')?.querySelector('.step-title')?.textContent }))
```
- 결과가 있으면 → `[CRITICAL] 깨진 이미지 렌더링`
- alt 속성 없는 img → `[WARNING]`

### 2.3 카드/레이아웃 검증

```javascript
// 빈 카드 감지
[...document.querySelectorAll('.practice-step')].filter(step => {
  const copy = step.querySelector('.step-copy');
  return !copy || copy.textContent.trim().length < 5;
}).map(step => step.querySelector('.step-title')?.textContent)
```

```javascript
// step 개수 매칭 (curriculum의 steps 수와 비교)
document.querySelectorAll('.practice-step').length
```

### 2.4 테마 일관성 검증

**다크 모드 검증 (기본):**
1. 페이지 로드 (기본 다크 모드)
2. 모든 iframe 요소의 배경색 확인:
```javascript
[...document.querySelectorAll('iframe')].map(f => {
  const style = getComputedStyle(f);
  return { src: f.src, bg: style.backgroundColor };
})
```
3. showme 버튼이 있으면 첫 번째 클릭 → 모달 내 iframe 배경 확인
4. 밝은 배경 (rgb 평균 > 200) 감지 → `[WARNING] 테마 불일치`

**라이트 모드 검증:**
1. 테마 전환: `document.documentElement.setAttribute('data-theme', 'light')`
2. 동일 검증 반복
3. 어두운 배경 iframe 감지 → `[WARNING] 테마 불일치`

**외부 삽입 이미지 검증:**
1. `.step-image-wrap img` 요소 중 밝은 배경 이미지 감지
2. 이미지 주변 배경과 이미지 자체 밝기 대비가 너무 강하면 → `[WARNING]`

### 2.5 모바일 검증

1. 뷰포트 375px로 리사이즈
2. 수평 잘림 확인: `document.documentElement.scrollWidth > document.documentElement.clientWidth`
3. 터치 타겟 확인:
```javascript
[...document.querySelectorAll('button, a, [role="button"]')].filter(el => {
  const rect = el.getBoundingClientRect();
  return rect.width < 44 || rect.height < 44;
}).length
```

### 2.6 스크린샷 증거

문제 발견 시 `preview_screenshot`으로 캡처.
파일명: `claudedocs/rpd-check-week{N}-{issue-type}.png`
