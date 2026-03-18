# ShowMe Card System

날짜: 2026-03-18

## 목적

ShowMe 카드를 `개별 HTML`만으로 관리하지 않고, 아래 4개 층으로 나눠 운영한다.

1. `리서치/교육 설계`
2. `카탈로그 메타데이터`
3. `보충 설명 데이터`
4. `HTML 카드 본문`

이렇게 나누면 카드 수가 늘어나도 품질 기준과 운영 상태를 같이 관리할 수 있다.

## 파일 구조

- `course-site/assets/showme/_registry.js`
  버튼 라벨과 아이콘.
- `course-site/assets/showme/_catalog.json`
  카테고리, 난이도, 혼동 포인트, 시각화 패턴, 선수지식.
- `course-site/assets/showme/_catalog.js`
  `_catalog.json`에서 생성되는 브라우저용 파일.
- `course-site/assets/showme/_supplements.json`
  "아직 헷갈린다면?" 보충 설명 원본 데이터.
- `course-site/assets/showme/_supplements.js`
  `_supplements.json`에서 생성되는 브라우저용 파일.
- `course-site/assets/showme/_helpers.js`
  라이브러리/주차 페이지가 같이 쓰는 공통 렌더링 함수.
- `tools/showme-tooling.mjs`
  sync / audit 도구.

## 메타데이터 스키마

`_catalog.json`은 6개 블록으로 구성한다.

### `categoryOrder`

라이브러리 탭 순서.

### `categoryMap`

카드 ID → 카테고리 매핑.

### `manualSectionOrder`

라이브러리에서 보여줄 상위 문서 섹션 순서.

예:

- `getting-started`
- `user-interface`
- `modeling`
- `sculpting-painting`
- `materials-uv`
- `rendering`
- `animation-rigging`

### `manualSectionMap`

카드 ID → 상위 문서 섹션 매핑.

이 값은 라이브러리 탐색 구조를 Blender 공식 문서처럼 `큰 흐름 먼저` 보이게 만들 때 사용한다.
카테고리보다 한 단계 위의 정보구조라고 보면 된다.

### `categoryDefaults`

카테고리별 기본값:

- `difficulty`: `beginner | intermediate | advanced`
- `confusionLabel`: 학생이 흔히 헷갈리는 축
- `stageLabel`: 학습 단계
- `supplementPriority`: `high | medium | low`
- `visualPattern`: 카드가 따라야 할 시각화 패턴

### `cardOverrides`

카드별 개별 보정값:

- `keywords`
- `prerequisites`
- `audienceNeed`
- 카테고리 기본값을 덮어쓰는 세부 속성

## 보충 설명 스키마

`_supplements.json` 항목 구조:

```json
{
  "some-card": {
    "title": "아직 헷갈린다면?",
    "analogy": {
      "emoji": "🧱",
      "headline": "일상 비유",
      "body": "..."
    },
    "before_after": {
      "before": "...",
      "after": "..."
    },
    "confusion": [
      {
        "symptom": "...",
        "reason": "...",
        "fix": "..."
      }
    ],
    "takeaway": "핵심 한 줄",
    "targets": ["card-id-1", "card-id-2"]
  }
}
```

## 운영 명령어

생성 파일 동기화:

```bash
node tools/showme-tooling.mjs sync
```

구조 감사:

```bash
node tools/showme-tooling.mjs audit
```

기계 판독용 결과:

```bash
node tools/showme-tooling.mjs audit --json
```

배포 전 엄격 검사:

```bash
node tools/showme-tooling.mjs audit --strict
```

## 권장 제작 순서

1. `_catalog.json`에서 카드의 학습 목적과 혼동 포인트를 먼저 정한다.
2. `_supplements.json`에 "말로 설명해도 잘 안 먹는 부분"을 넣는다.
3. HTML 카드 본문을 만든다.
4. `node tools/showme-tooling.mjs sync`로 브라우저용 데이터를 갱신한다.
5. `node tools/showme-tooling.mjs audit --strict`로 누락을 확인한다.

## 제작 기준

- 카드 설명은 `course-site/CONTENT_GUIDE.md` 톤을 따른다.
- 카드가 다뤄야 하는 핵심은 "기능 설명"보다 "왜 여기서 헷갈리는지"다.
- 시각화는 가능한 한 `before → action → result` 흐름을 보여준다.
- 혼동이 잦은 카드는 supplement priority를 `high`로 올리고 보충 설명을 꼭 붙인다.
