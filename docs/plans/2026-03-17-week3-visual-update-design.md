# Week 3 시각화 업데이트 설계

**날짜:** 2026-03-17
**범위:** Week 3 스텝 카드에 영상 클립 + ShowMe 애니메이션 이중 시각화 시스템 구축

## 핵심 원칙

학생 학습 흐름: **ShowMe(원리) → 영상 클립(실전) → 직접 따라하기(체크리스트)**

| 레이어 | 형태 | 역할 | 재사용성 |
|--------|------|------|----------|
| ShowMe | HTML Canvas 애니메이션 | 범용 개념 교육 모듈 | 다른 주차·프로젝트에 재사용 |
| 영상 클립 | MP4/WebM 인라인 비디오 | Mint Robot 실제 작업 과정 | 프로젝트 전용 |

## 1. 영상 클립 시스템

### 소스 영상
- `001.Mint_Robot_reference_setting.mov` (8분, 3024x1894)
- `002.Mint_Robot_head_mirror.mov` (6분, 3024x1894)

### 추출 계획

| 클립 ID | 소스 | 구간 | 내용 | 대상 스텝 |
|---------|------|------|------|-----------|
| ref-import | 001 | ~1:30-2:00 | Shift+A → Image 불러오기 | Step 1 |
| ref-position | 001 | ~3:30-4:30 | 정면/측면/후면 배치 | Step 1 |
| ref-opacity | 001 | ~5:30-6:00 | Opacity 조절, 뷰 정렬 | Step 1 |
| head-scale | 002 | ~0:30-1:30 | 큐브 스케일 + X-Ray | Step 2 |
| head-edit | 002 | ~2:30-3:30 | Edge Slide, 형태 조정 | Step 2 |
| mirror-setup | 002 | ~4:00-5:00 | 절반 삭제 + Mirror + Clipping | Step 3 |
| mirror-edit | 002 | ~5:00-6:00 | 대칭 편집 확인 | Step 3 |

### 압축 스펙
- 해상도: 720p (1280x800)
- 포맷: MP4 (H.264, AAC) + WebM (VP9) 듀얼
- 파일 크기: 1-3MB/클립
- 저장: `assets/clips/week03/`

### curriculum.js 필드

```js
"clips": [
  {
    "label": "이미지 불러오기",
    "src": "assets/clips/week03/ref-import.mp4"
  }
]
```

### week.html UI

- `<video autoplay loop muted playsinline>` 인라인 임베드
- 클릭: 일시정지/재생 토글
- 복수 클립: 탭 전환
- 위치: 스텝 이미지 자리 (image 필드와 배타적 또는 병렬)

## 2. ShowMe 업데이트

### 기존 유지
- `image-reference` — 이미 등록됨, 내용 보강 (Canvas 애니메이션으로 뷰포트 배치 원리)
- `mirror-modifier` — 기존 개념 설명 유지

### 신규 제작
- `mirror-workflow` — 절반 삭제 → Mirror 추가 → Clipping → 편집의 전체 워크플로우를 단계별 Canvas 애니메이션으로 시각화. 범용 모듈.

## 3. curriculum.js 구조 변경 (Week 3)

현재 Step 1 "기본형 만들기"가 레퍼런스 설정 + Edit Mode 작업을 모두 포함. 분리:

### Step 1: 레퍼런스 이미지 설정
- clips: 001 영상에서 3클립
- showme: "image-reference"
- copy: Blender 5.0 기준으로 업데이트

### Step 2: 기본형 만들기
- clips: 002 영상 전반부 2클립
- showme: "edit-mode-tools"

### Step 3: Mirror
- clips: 002 영상 후반부 2클립
- showme: ["mirror-modifier", "mirror-workflow"]

### Step 4-8: 기존 유지
- Subdivision Surface, Solidify, Array, Boolean 등

## 4. 파일 변경 목록

| 파일 | 변경 |
|------|------|
| `week.html` | 클립 플레이어 컴포넌트 CSS + JS 추가 |
| `data/curriculum.js` | Week 3 steps 구조 변경, clips 필드 추가 |
| `assets/showme/_registry.js` | mirror-workflow 등록 |
| `assets/showme/mirror-workflow.html` | 신규 ShowMe 위젯 |
| `assets/clips/week03/*.mp4` | 추출된 클립 파일 |

## 5. 신규 스킬: `/clip`

영상 클립 추출 자동화:
```
/clip week 3 001.mov 0:30-0:55 "이미지 불러오기"
```
- ffmpeg 구간 추출 → 720p 압축 → assets/clips/ 저장
- curriculum.js clips 엔트리 자동 추가

## 6. Blender 버전
- 대상: Blender 5.0.1
- ShowMe 내 UI 참조는 5.0 기준으로 작성
