---
name: rpd-site-improve
description: RPD 수업 사이트 CSS/HTML 디자인 개선. tokens.css 수정, 레이아웃 조정, 컴포넌트 스타일링 시 사용. Use when modifying course-site CSS, layout, or visual design.
---

# RPD Site Improve

## 대상 파일
- `course-site/assets/tokens.css` — 공유 CSS 토큰 (index, week, admin 3페이지 공유)
- `course-site/index.html` — 메인 페이지 (inline styles)
- `course-site/week.html` — 주차 상세 페이지 (inline styles + JS 템플릿)
- `course-site/admin.html` — 관리자 편집기 (tokens.css 의존)
- `course-site/assets/showme/*.html` — Show Me 카드 인터랙션/탭 구조

## 핵심 제약

### admin.html 호환성
tokens.css를 수정할 때 반드시 admin.html도 확인해야 함.
admin.html이 사용하는 주요 클래스:
- `.section-head :is(h2, h3)`, `.card`, `.btn`, `.status-pill`
- `:root` CSS 변수 전체
- `.topbar`, `.progress-widget`, `.brand`

### 디자인 방향 (Style Guide 요약)
1. Apple-like: 과한 장식보다 정보의 선명함
2. Low Noise: 불필요하게 큰 타이틀, 과한 glow 줄이기
3. Read First: 학생은 디자인보다 먼저 "무엇을 해야 하는지"를 읽어야 함
4. Action Oriented: 읽기 자료가 아닌 행동 유도 인터페이스

### 인지부하 우선 규칙
- 반복 카드가 많으면 기본 상태에서는 이름만 먼저 보여주기
- 카테고리/난이도/slug 같은 보조 메타는 검색, 필터, 모달로 이동
- 한 카드에서 동시에 비교하게 만드는 정보 축은 1개만 남기기
- 클릭 전에 필요 없는 장식 아이콘, 배지, 보조 문장을 기본 화면에서 줄이기

### Show Me 카드 규칙
- 탭 1 `개념 이해`에 개념 설명 + 개념 시각화 요약을 함께 둔다
- 탭 2 라벨은 항상 `interaction`으로 통일한다
- `interaction` 탭에는 설명용 before/after, cause-effect, 긴 시나리오 문장을 두지 않는다
- 파라미터형 카드는 `.modifier-panel` + `range` + `number` + `checkbox/select` 조합을 우선 사용한다
- `"얇은 벽 / 두꺼운 벽"` 같은 프리셋 대신 `Thickness`, `Offset`, `Count`, `Width`, `Merge Distance`처럼 Blender 실제 파라미터명을 그대로 노출한다
- 학생이 꼭 알아야 하는 정보만 남기고, 긴 문장형 보조 설명은 줄인다
- 주석/보조 안내는 작은 카드 2~3개로 요약하는 쪽을 우선한다
- 개념 탭의 부가 설명은 외부 이동 대신 `더보기` 내부 펼침으로 둔다
- 버튼은 모드 전환이나 Reset처럼 꼭 필요한 경우만 남긴다
- 기존 카드 보정 시에도 라이브러리/주차 모달과 개별 HTML이 같은 UX를 보이도록 맞춘다

### 컬러 토큰
```
--bg: #0a0a0a          --text: #f5f5f7
--surface: #17181a     --muted: #a1a1aa
--key: #0a84ff         --key-soft: #8ec5ff
--success: #10b981     --warn: #f59e0b
--line: rgba(255,255,255,.08)
```
- 메인 강조색은 블루 하나만 사용
- 성공 상태 외에는 초록을 거의 쓰지 않음
- 카드 구분은 색보다 밝기 차와 보더로 해결

### tokens.css 섹션 맵
1. `:root` 변수 (line 8-38)
2. Reset + Body (line 40-53)
3. Grid overlay (line 55-66)
4. Topbar (line 68-91)
5. Progress widget (line 93-106)
6. Buttons (line 108-124)
7. Section wrapper (line 126-131)
8. Section headers (line 133-141)
9. Cards (line 143-156)
10. Eyebrow pill (line 158-164)
11. Step cards (line 166-201)
12. Status pills (line 210-219)
13. Task list (line 221-236)
14. Shortcuts table (line 270-298)
15. Explore cards (line 300-320)
16. Footer (line 322-329)
17. Responsive (line 331-339)

### 타이포 규칙
- H1: 40-56px, weight 600-700
- H2/Section title: 24-30px, weight 600
- Body: 16px, weight 400
- Caption/chip: 최소 12px (0.75rem)
- Korean body line-height: 1.75
- `word-break: keep-all` 필수

## 작업 체크리스트

CSS 변경 시 아래를 순서대로 확인:
1. [ ] tokens.css 수정 후 admin.html에서 깨지는 부분 없는지 확인
2. [ ] index.html에서 1280px / 375px 레이아웃 확인
3. [ ] week.html?week=3에서 동일 확인
4. [ ] 키보드 Tab 탐색 시 focus ring 보이는지 확인
5. [ ] `prefers-reduced-motion: reduce` 시 애니메이션 비활성화 확인
6. [ ] 콘솔 에러 없음 확인
7. [ ] Show Me 카드 수정 시 `개념 이해 / interaction / 언제 쓰나요? / 퀴즈` 4탭 구조 유지 확인
8. [ ] 파라미터형 interaction이 버튼 프리셋보다 슬라이더/숫자 입력 중심인지 확인

## 참고 문서
- `docs/COURSE_SITE_STYLE_GUIDE_2026-03-13.md`
- `docs/COGNITIVE_UI_GUIDE_2026-03-18.md`
- `docs/REFERENCE_RESEARCH_2026-03-15.md`

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)
