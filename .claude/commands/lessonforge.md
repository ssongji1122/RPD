---
description: "LessonForge 영상 제작 파이프라인. 예: /lessonforge review week02, /lessonforge narrate week03, /lessonforge build week02"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python3:*), Bash(cd:*), Bash(ls:*), Bash(wc:*), Bash(pip:*), Agent
---

## Context

- 프로젝트 루트: !`git rev-parse --show-toplevel 2>/dev/null`
- LessonForge 위치: !`ls tools/lessonforge/src/lessonforge/cli.py 2>/dev/null && echo "✅ 설치됨" || echo "❌ 없음"`
- Config: !`ls tools/lessonforge/lessonforge.config.yaml 2>/dev/null && echo "✅ 있음" || echo "❌ 없음"`
- 강의노트 디렉토리: !`ls -d weeks/week* 2>/dev/null | wc -l | tr -d ' '`개
- 출력 디렉토리: !`ls -d tools/lessonforge/output/week* 2>/dev/null | wc -l | tr -d ' '`개
- TTS 엔진: Edge TTS (ko-KR-SunHiNeural)
- 영상 설정: 1920x1080, 30fps, 세그먼트당 20-30분
- YouTube: unlisted, playlist "RPD 2026 Spring"

## Task

인자: `$ARGUMENTS`

---

### 모드 분기

---

#### `review {week}` — 강의 내용 리뷰 (빌드 전 필수)

영상 빌드 전에 강의노트 내용을 확인합니다.

**실행:**
```bash
cd tools/lessonforge && python3 -m lessonforge review {week}
```

**출력 내용:**
- 학습 목표 리스트
- 이론 섹션 구조
- 실습 단계 테이블 (제목, 예상시간, 단축키, 소제목 수)
- 영상 세그먼트 계획 (ID, 제목, 블록 수, 예상시간)
- 녹화 현황 (week_video_map.yaml 참조: reuse/partial/new)
- 총 예상 수업 시간

---

#### `parse {week}` — 강의노트 파싱

lecture-note.md를 파싱하여 구조를 트리로 출력합니다.

**실행:**
```bash
cd tools/lessonforge && python3 -m lessonforge parse {week}
```

**확인 사항:**
- 학습 목표 (완료/미완료)
- 이론/실습 섹션 구분
- 각 Step: 번호, 제목, 예상 시간, 액션 타입, 단축키, URL, 세부 단계 수

---

#### `narrate {week} [--dry-run]` — TTS 나레이션 생성

강의노트에서 나레이션 스크립트를 생성하고 TTS 오디오를 합성합니다.

**실행:**
```bash
cd tools/lessonforge && python3 -m lessonforge narrate {week} [--dry-run]
```

**`--dry-run`**: 스크립트만 출력하고 오디오 생성 안 함

**출력물:**
- `output/week{NN}/segments/{seg_id}/audio/` — TTS 오디오 파일들
- `output/week{NN}/segments/{seg_id}/script.json` — 나레이션 스크립트

**설정값:**
- 엔진: Edge TTS
- 음성: ko-KR-SunHiNeural
- 속도: +5%

---

#### `build {week} [--segments N] [--dry-run]` — 영상 빌드 (전체 파이프라인)

parse → slides → narrate → compose 전체 파이프라인을 실행합니다.

**실행:**
```bash
cd tools/lessonforge && python3 -m lessonforge build {week} [--segments 1,2] [--dry-run]
```

**옵션:**
- `--segments 1,2`: 특정 세그먼트만 빌드
- `--dry-run`: 빌드 계획만 출력

**출력물:**
- `output/week{NN}/segments/{seg_id}/video.mp4` — 최종 영상

---

#### `record {week} [--segment N] [--dry-run]` — 녹화 계획

실습 단계별 스크린 녹화 계획을 분석합니다.

**실행:**
```bash
cd tools/lessonforge && python3 -m lessonforge record {week} [--dry-run]
```

**분석 내용:**
- 각 Step의 녹화 모드 (SLIDE / BLENDER_SCRIPTED / BLENDER_MCP / BROWSER / MIXED)
- 필요한 도구 확인 (Blender, Playwright, FFmpeg)
- 예상 시간

---

#### `subtitle {source} [--notes file] [--burn-in]` — 자막 생성

무음 튜토리얼 클립에 자막을 자동 생성합니다.

**실행:**
```bash
cd tools/lessonforge && python3 -m lessonforge subtitle-clips {source} [--notes file] [--burn-in]
```

**옵션:**
- `--notes`: 자막 가이드 파일 (video_notes.md 또는 week_video_map.yaml)
- `--burn-in`: 자막이 입혀진 MP4도 생성

**출력물:**
- `subtitles/srt/` — SRT 자막 파일
- `subtitles/burned/` — 자막 입힌 영상 (--burn-in 시)
- `subtitles/subtitle_manifest.json` — 매니페스트

---

#### `outline {source} [--notes file]` — 목차 카드 생성

영상에 목차 개요 카드 이미지를 생성합니다.

**실행:**
```bash
cd tools/lessonforge && python3 -m lessonforge outline-cards {source} [--notes file]
```

**출력물:**
- `outline_cards/` — PNG 목차 카드 이미지

---

#### `chapter {source} [--notes file] [--opener-seconds 4]` — 챕터 오프닝 삽입

목차 카드를 영상 앞에 자동 삽입합니다.

**실행:**
```bash
cd tools/lessonforge && python3 -m lessonforge chapter-openers {source} [--notes file] [--opener-seconds 4]
```

**출력물:**
- `chapter_openers/cards/` — 챕터 카드 이미지
- `chapter_openers/videos/` — 오프닝 포함 영상

---

#### `publish {week} [--segments N] [--privacy unlisted] [--dry-run]` — YouTube 업로드

빌드된 영상을 YouTube에 업로드합니다.

**실행:**
```bash
cd tools/lessonforge && python3 -m lessonforge publish {week} [--dry-run]
```

**필수 준비:**
- `client_secrets.json` (Google Cloud Console → YouTube Data API v3)
- 첫 실행 시 브라우저 OAuth2 인증

**YouTube 설정:**
- Playlist: "RPD 2026 Spring"
- Category: 27 (Education)
- Language: ko
- Privacy: unlisted (기본)
- 기본 태그: 블렌더, Blender, Blender 5.0, 3D모델링, 로봇디자인, 인하대학교, AI, MCP

---

#### `voices` — 사용 가능 TTS 음성 목록

한국어 Edge TTS 음성 목록을 출력합니다.

**실행:**
```bash
cd tools/lessonforge && python3 -m lessonforge voices
```

---

#### `status {week}` — 빌드 상태 확인

해당 주차의 출력 디렉토리 내용을 트리로 출력합니다.

**실행:**
```bash
cd tools/lessonforge && python3 -m lessonforge status {week}
```

---

#### 인자 없음 — 도움말

전체 워크플로우 가이드를 출력합니다.

**권장 워크플로우:**
```
1. /lessonforge review weekNN     ← 강의 내용 확인
2. /lessonforge narrate weekNN --dry-run  ← 스크립트 미리보기
3. /lessonforge narrate weekNN    ← TTS 생성
4. /lessonforge build weekNN      ← 영상 빌드
5. /lessonforge publish weekNN --dry-run  ← 업로드 미리보기
6. /lessonforge publish weekNN    ← YouTube 업로드
```

---

### 핵심 파일 경로

| 파일 | 역할 |
|------|------|
| `tools/lessonforge/src/lessonforge/cli.py` | CLI 진입점 (Click 기반) |
| `tools/lessonforge/lessonforge.config.yaml` | 프로젝트 설정 (해상도, TTS, YouTube) |
| `tools/lessonforge/week_video_map.yaml` | 주차별 영상 메타데이터 (reuse/partial/new) |
| `weeks/weekNN-*/lecture-note.md` | 강의노트 원본 |
| `tools/lessonforge/output/` | 빌드 출력 디렉토리 |

### LessonForge 모듈 구조

```
src/lessonforge/
├── cli.py          — Click CLI 그룹
├── config.py       — YAML 설정 로더
├── manifest.py     — 빌드 매니페스트
├── subtitles.py    — 자막 생성 + SRT + burn-in
├── parser/         — lecture-note.md 파서 + 스크립트 생성
├── narration/      — Edge TTS + ElevenLabs 엔진
├── recording/      — Blender/Browser agent + OBS + scene planner
├── compositor/     — FFmpeg 합성 + 타이틀 카드
└── publisher/      — YouTube 메타데이터 + 업로드
```

### 설치 확인

```bash
cd tools/lessonforge && pip install -e . 2>/dev/null
# 또는
cd tools/lessonforge && python3 -m lessonforge --help
```

필요 패키지: `click`, `rich`, `edge-tts`, `pyyaml`, `Pillow`
선택 패키지: `ffmpeg-python` (영상 합성), `google-api-python-client` (YouTube)

## 실행 로그
실행 완료 시 아래 형식으로 기록:
```bash
echo "[$(date '+%Y-%m-%d %H:%M')] mode=$MODE result=$RESULT target=$TARGET" >> .claude/skill-logs/lessonforge.log
```

## Gotchas ⚠️
> Claude가 이 스킬을 쓸 때 실수했던 것들. 새 함정 발견 시 여기에 추가.

1. (아직 없음 — 사용하면서 추가)
