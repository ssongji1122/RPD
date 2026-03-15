# Showme 인터랙티브 교육카드 아키텍처

작성일: 2026-03-15

## 1. 핵심 결정

**Showme 카드는 "주차별"이 아니라 "블렌더 기능별"로 만든다.**

- 각 카드는 독립적인 HTML 파일로, 하나의 블렌더 기능/개념을 다룬다
- 주차별 페이지에서는 해당 주차에 필요한 카드만 가져와서 쓴다
- 같은 카드를 여러 주차에서 재사용할 수 있다

## 2. 왜 기능별인가

| 기준 | 주차별 | 기능별 (채택) |
|------|--------|---------------|
| 재사용성 | 낮음 — 같은 기능이 여러 주차에 나오면 중복 | 높음 — 한 번 만들면 어디서든 참조 |
| 유지보수 | 주차 구조 변경 시 카드도 같이 이동 | 기능은 변하지 않으므로 안정적 |
| 확장성 | 주차 추가 시 카드도 새로 만들어야 함 | 기존 카드 조합만으로 새 주차 커버 가능 |
| 학생 탐색 | 주차 안에서만 접근 가능 | 기능 라이브러리에서 직접 찾아볼 수도 있음 |

## 3. 파일 구조

```
course-site/
  assets/
    showme/                          ← 기능별 카드 라이브러리
      edit-mode-tools.html           ← Extrude / Loop Cut / Inset / Bevel
      mirror-modifier.html           ← Mirror Modifier
      subdivision-surface.html       ← Subdivision Surface
      solidify-modifier.html         ← Solidify
      array-modifier.html            ← Array
      boolean-modifier.html          ← Boolean
      bevel-modifier.html            ← Bevel Modifier + Weighted Normal
      origin-vs-3dcursor.html        ← Origin vs 3D Cursor (이미 완성)
      ...
```

## 4. 카드 구조 (표준 패턴)

모든 showme 카드는 아래 4-탭 패턴을 따른다:

1. **개념 이해** — 핵심 설명, 단축키, 비교 카드
2. **시각적 비교/데모** — Canvas 인터랙션 또는 애니메이션
3. **언제 쓰나요?** — 사용 사례, 추천 조합
4. **퀴즈** — 4~5문제, 즉시 피드백

### 기술 사양
- 독립형 단일 HTML (외부 의존성 없음)
- 다크/라이트 모드 대응 (`prefers-color-scheme`)
- 모바일 터치 대응
- 한국어 기본

## 5. 주차별 연결 방식

`curriculum.js`에서 각 step 또는 week에 `showme` 필드를 추가:

```js
{
  "week": 3,
  "showme": [
    "edit-mode-tools",
    "mirror-modifier",
    "subdivision-surface",
    "solidify-modifier",
    "array-modifier",
    "boolean-modifier",
    "bevel-modifier"
  ],
  "steps": [
    {
      "title": "기본형 만들기",
      "showme": "edit-mode-tools",   // step별로도 연결 가능
      ...
    }
  ]
}
```

`week.html`에서 showme 카드를 iframe 또는 모달 링크로 렌더링한다.

## 6. 주차별 카드 매핑 (현재 계획)

| 기능 카드 | W02 | W03 | W04 | W05 | W06 | W07 | ... |
|-----------|-----|-----|-----|-----|-----|-----|-----|
| origin-vs-3dcursor | ✅ | | | | | | |
| edit-mode-tools | | ✅ | ✅ | | | | |
| mirror-modifier | | ✅ | ✅ | | | | |
| subdivision-surface | | ✅ | ✅ | | | | |
| solidify-modifier | | ✅ | | | | | |
| array-modifier | | ✅ | | | | | |
| boolean-modifier | | ✅ | ✅ | | | | |
| bevel-modifier | | ✅ | ✅ | | | | |

> 이 매핑은 커리큘럼 변경에 따라 업데이트한다.

## 7. 참고 — 기존 showme 카드

- `blender_origin_vs_3dcursor_3.html` (~/Downloads): Origin vs 3D Cursor 프로토타입
  - 4탭 구조, Canvas 인터랙션, 퀴즈 엔진
  - 이 파일의 디자인 패턴을 표준으로 삼는다
