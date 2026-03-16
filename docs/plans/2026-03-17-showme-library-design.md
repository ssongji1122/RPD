# Show Me 도구 라이브러리 페이지 설계

**날짜:** 2026-03-17
**기능:** `library.html` — showme 카드 전체 검색/브라우징 전용 페이지

---

## 목표

도구 이름(툴명)으로 검색해서 해당 Show Me 카드를 바로 열 수 있는 독립 페이지.

---

## 구조

### 파일
- `course-site/library.html` — 신규 생성
- `course-site/assets/showme/_registry.js` — 기존 데이터 재활용 (수정 없음)
- `course-site/week.html` — 상단 네비게이션에 링크 추가

### 페이지 레이아웃

**헤더**
- 제목: "도구 라이브러리"
- 부제: "Blender 도구·모디파이어 개념 카드 모음"
- 검색바: 실시간 필터, placeholder "예: Array, Mirror, UV..."
- 카운터: "N개 도구" (필터 적용 시 "N / 56개")

**카테고리 탭**
`_registry.js` 그룹 기반:
- 전체 / Edit Mode / Generate Modifiers / Normals / Sculpting / Material / UV / Lighting / Animation / Rigging / Rendering / 기타

**카드 그리드**
- `auto-fit, minmax(160px, 1fr)` 반응형 그리드
- 카드당: 아이콘(크게) + 한글 라벨 + 영문 ID(서브텍스트)
- 호버 시 파란 테두리 강조
- 검색 결과 없음 → "검색 결과가 없습니다" 안내 메시지

**모달**
- week.html의 showme 모달과 동일한 디자인 (overlay + iframe)
- ESC / 배경 클릭으로 닫기

---

## 데이터 설계

`_registry.js`에 카테고리 정보가 없으므로, `library.html` 내에 카테고리 매핑 상수를 정의:

```js
const CATEGORY_MAP = {
  "edit-mode":    "Edit Mode",
  "extrude":      "Edit Mode",
  "loop-cut":     "Edit Mode",
  // ... 각 ID → 카테고리명 매핑
};
```

---

## 검색 로직

1. 검색어를 소문자로 정규화
2. 카드의 `label`(한글) + `id`(영문) 양쪽에서 매칭
3. 카테고리 탭 필터와 AND 조건으로 결합
4. 매칭된 카드만 표시, 나머지 `display: none`

---

## 네비게이션 연결

`week.html` 상단 `.week-nav` 영역에 "도구 라이브러리 →" 링크 추가.

---

## 스타일

- `tokens.css` 임포트, 기존 다크테마 변수 사용
- showme 카드 디자인 참고 (`.surface`, `.line` 계열 변수)
- 모바일: 탭은 가로 스크롤, 카드 그리드 1~2열
