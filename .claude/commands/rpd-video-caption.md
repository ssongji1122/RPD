---
description: Step·Week 비디오 캡션/설명 추가. 예: /rpd-video-caption list, /rpd-video-caption week03 step, /rpd-video-caption week03 videos, /rpd-video-caption week03
allowed-tools: Read, Edit, Glob, Grep
---

# rpd-video-caption

curriculum.js의 `step.video.caption`과 `videos[].description`을 추가·수정하는 커맨드.

데이터는 분리 유지 — 역할이 다르기 때문:
- **step caption**: 액션 유도형. 학생이 영상 시청 전 읽는 1줄 안내
- **videos description**: 참고 요약형. 링크 카드 하단에서 어떤 내용인지 설명

## 사용법

| 명령 | 동작 |
|------|------|
| `/rpd-video-caption list` | 캡션/description 없는 video 목록 출력 |
| `/rpd-video-caption week{N} step` | 해당 주차 step.video.caption만 추가/수정 |
| `/rpd-video-caption week{N} videos` | 해당 주차 videos[].description만 추가/수정 |
| `/rpd-video-caption week{N}` | step + videos 둘 다 처리 |

## 캡션 작성 기준

- **톤**: ~해요 체, 반말 금지
- **길이**: 30–50자 내외
- **step.video.caption** 형식: `"~하는 과정이에요. 영상을 보며 따라해요."` (행동 유도)
- **videos[].description** 형식: `"~하는 방법을 배워요."` 또는 `"~과정을 담은 영상이에요."` (내용 요약)

### 동일 영상 자동 감지

`week{N}` 통합 모드에서 step.video.src 파일명과 videos[].title이 의미상 같은 영상을 가리키면 → 두 필드를 각각 다른 톤으로 자동 생성.

## 데이터 구조

```json
// step.video — string은 레거시, object로 통일
"video": {
  "src": "assets/videos/weekXX/NNN-slug.mov",
  "caption": "액션 유도형 캡션 텍스트"
}

// videos[] 항목
{
  "title": "영상 제목",
  "url": "https://...",
  "description": "내용 요약형 설명 텍스트"
}
```

## 실행 흐름

### `list` 모드
1. `course-site/data/curriculum.js` 읽기
2. 주차별로 다음 항목 스캔:
   - `step.video`가 string이거나 `.caption` 없는 것 → "step video 미완성"
   - `videos[]` 항목 중 `.description` 없는 것 → "week video 미완성"
3. 표 형태로 출력:

```
| 주차 | 타입 | 제목/파일 | 상태 |
|------|------|----------|------|
| week03 | step video | 001-ref-setting.mov | caption 없음 |
| week03 | week video | [실습] 헤드 Mirror | description 없음 |
```

### `week{N} step` 모드
1. 해당 주차 steps에서 `video` 필드 있는 step 찾기
2. step의 title, copy, tasks 읽어 컨텍스트 파악
3. caption 초안 생성 (행동 유도형, 30–50자)
4. video가 string이면 object로 변환 후 caption 추가, object면 caption 필드 추가
5. curriculum.js 수정

### `week{N} videos` 모드
1. 해당 주차 videos[] 읽기
2. description 없는 항목에 대해 title로 내용 추론 → description 초안 생성
3. curriculum.js 수정

### `week{N}` 통합 모드
1. step 처리 후 videos 처리
2. 파일명과 videos title이 같은 영상이면: step caption은 행동 유도형, videos description은 요약형으로 각각 작성

## 수정 후 검증

- JSON 문법 확인: 쉼표 위치, 따옴표 닫힘
- `video` 필드가 object 형식인지 확인 (`src` + optional `caption`)
- `videos[]` 항목에 `description` 추가됐는지 확인
