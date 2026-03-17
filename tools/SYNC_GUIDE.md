# Notion ↔ 웹 동기화 시스템 가이드

## 개요

이 시스템은 Notion 데이터베이스와 웹 커리큘럼 사이의 양방향 동기화를 제공합니다.

- **Notion → 웹**: `notion-sync.js` - Notion 페이지에서 콘텐츠를 읽어 `overrides.json` 업데이트
- **웹 → Notion**: `web-to-notion.js` - 학생 진행도를 Notion 페이지에 동기화

## 파일 구조

```
tools/
├── notion-sync.js          # Notion → overrides.json 동기화
├── web-to-notion.js        # 웹 → Notion 동기화
├── sync-config.json        # 주차별 페이지 ID 매핑
└── SYNC_GUIDE.md           # 이 파일

course-site/data/
├── notion-config.json      # Notion API 토큰
├── curriculum.js           # 메인 커리큘럼 데이터
├── overrides.json          # 주차별 오버라이드 (Notion에서 동기화됨)
└── student-progress.json   # 학생 진행도 (Notion으로 동기화됨)
```

## 설정

### 1. Notion API 토큰 확인

`course-site/data/notion-config.json`에 Notion API 토큰이 저장되어 있습니다.

```json
{
  "enabled": true,
  "token": "your_notion_api_token_here",
  "databaseId": "d27c5dfdac27433284a4a6be1b6d8801"
}
```

### 2. 주차별 페이지 ID 확인

`tools/sync-config.json`에서 각 주차의 Notion 페이지 ID를 확인/수정할 수 있습니다.

```json
{
  "weeks": {
    "1": "31354d654971812e9f48f392f2de551b",
    "2": "31354d6549718179a709cabf829a5971",
    "3": "31354d6549718193a446f3b9d02fb790",
    ...
  }
}
```

**Notion에서 페이지 ID 찾는 방법:**
1. Notion에서 해당 주차 페이지 열기
2. URL에서 `https://notion.so/31354d6549718193a446f3b9d02fb790` 형식에서 마지막 부분이 페이지 ID

## 사용 방법

### 방법 1: 셸 스크립트 (권장)

```bash
# Notion → 웹 (overrides.json 업데이트)
./start-admin.sh sync-from-notion

# 웹 → Notion (학생 진행도 업데이트)
./start-admin.sh sync-to-notion

# 양방향 동기화
./start-admin.sh sync-all
```

### 방법 2: Node.js 직접 실행

**Notion → 웹 동기화:**

```bash
# 모든 주차 동기화
NOTION_TOKEN="your_notion_api_token_here" \
node tools/notion-sync.js --all

# 특정 주차만 동기화 (예: 3주차)
NOTION_TOKEN="your_notion_api_token_here" \
node tools/notion-sync.js --week 3
```

**웹 → Notion 동기화:**

```bash
# 모든 주차 동기화
NOTION_TOKEN="your_notion_api_token_here" \
node tools/web-to-notion.js --all

# 특정 주차만 동기화 (예: 3주차)
NOTION_TOKEN="your_notion_api_token_here" \
node tools/web-to-notion.js --week 3
```

## Notion 페이지 구조

각 주차 페이지는 다음과 같은 섹션으로 구성되어야 합니다:

### 예: Week 3 페이지

```
# Week 03: 모델링 기초

## 상태
active

## 요약
레고 조립처럼, Edit Mode로 블록을 깎고 Modifier로 대칭·곡면·반복 효과를 얹는 흐름을 배워요.

## 비디오
### Blender Studio - Modeling Introduction
[bookmark: https://studio.blender.org/.../modeling-introduction/]

### Blender Studio - Object and Edit Mode
[bookmark: https://studio.blender.org/.../object-and-edit-mode/]

## 단계

### Step 0: 기본형 만들기
[image: assets/images/week03/base-form.png]
- 몸통과 주요 덩어리가 잡혔다
- 대칭이 올바르게 설정됐다

### Step 1: Mirror 적용
[image: assets/images/week03/mirror.png]
- Mirror Modifier를 추가했다
- 양쪽이 동일하게 나타난다

## 탐색
- 로봇 몸체 만들기 → 큐브 → Edit Mode로 기본형 → Mirror → Subdivision으로 부드럽게
- 패널 구조 만들기 → Plane → Solidify → Boolean으로 홈 추가
- 반복 파츠 만들기 → Cube 또는 Cylinder → Array로 6~10개 반복
```

### 주요 섹션 설명

| 섹션 | 형식 | 필수 | 설명 |
|------|------|------|------|
| **상태** | 텍스트 (done/active/upcoming) | 선택 | 주차 진행 상태 |
| **요약** | 단락 | 선택 | 주차 요약 설명 |
| **비디오** | 북마크 목록 | 선택 | 참고 비디오 링크 |
| **단계** | 제목 + 이미지 + 불릿 | 선택 | 학습 단계별 정보 |
| **탐색** | 불릿 리스트 | 선택 | 자유로운 탐색 과제 |

## overrides.json 구조

동기화된 데이터는 다음 구조로 저장됩니다:

```json
{
  "_comment": "어드민 전용 필드. 노션 동기화 시 이 값이 우선함.",
  "weeks": {
    "1": {
      "status": "done",
      "summary": "Blender 설치, Mixboard로 컨셉 설정.",
      "videos": [
        {
          "title": "Blender Studio - First Steps",
          "url": "https://studio.blender.org/..."
        }
      ],
      "steps": {
        "0": {
          "image": "assets/images/week01/install.png",
          "done": [
            "Blender가 정상적으로 열린다",
            "버전 번호를 확인했다"
          ]
        },
        "1": {
          "image": "assets/images/week01/mixboard.png",
          "done": [
            "Mixboard에 적어도 3개 이상 이미지가 있다"
          ]
        }
      },
      "explore": [
        {
          "title": "로봇 몸체 만들기",
          "hint": "큐브 → Edit Mode로 기본형 → Mirror → Subdivision으로 부드럽게"
        }
      ]
    }
  }
}
```

## 학생 진행도 형식

`course-site/data/student-progress.json`의 예:

```json
{
  "studentId": "user123",
  "weeks": {
    "1": {
      "status": "done",
      "checklist": [
        {
          "id": "w1-t1",
          "label": "blender.org 에서 다운로드 완료",
          "completed": true
        },
        {
          "id": "w1-t2",
          "label": "Blender 처음 실행 완료",
          "completed": true
        }
      ]
    },
    "2": {
      "status": "active",
      "checklist": [
        {
          "id": "w2-t1",
          "label": "Preferences 직접 열어보기",
          "completed": true
        },
        {
          "id": "w2-t2",
          "label": "Input → Emulate 3 Button Mouse 켜기",
          "completed": false
        }
      ]
    }
  }
}
```

## 동기화 흐름

### Notion → 웹 (notion-sync.js)

```
Notion 페이지
    ↓
    ├─ 블록 가져오기 (제목, 단락, 북마크, 이미지, 불릿)
    ├─ 섹션별로 분류 (status, summary, videos, steps, explore)
    ├─ curriculum override 데이터로 변환
    └─ overrides.json 업데이트 (변경사항만)

웹 페이지 로드 시:
    curriculum.js + overrides.json → 최종 콘텐츠
```

### 웹 → Notion (web-to-notion.js)

```
student-progress.json
    ↓
    ├─ 주차별 진행도 읽기
    ├─ 체크리스트 완료 정보 추출
    └─ Notion 페이지 블록 업데이트
        ├─ 기존 블록 삭제
        ├─ 진행도 섹션 추가
        ├─ 체크리스트 재작성
        └─ 동기화 메타데이터 추가
```

## 오류 처리

### 네트워크 오류
- Notion API 호출 실패 시 경고하고 계속 진행
- 기존 데이터 손실 방지

### 파일 오류
- 파일을 찾을 수 없으면 기본값 사용
- JSON 파싱 오류 시 경고하고 빈 객체로 처리

### API 오류
- 개별 주차 실패해도 다른 주차는 계속 동기화
- 상세한 오류 메시지 출력 (console.warn)

## 로깅 및 디버깅

### 로그 레벨

- `✓`: 성공 (녹색)
- `⚠`: 경고 (노란색)
- `✗` / `❌`: 오류 (빨간색)
- `📋`, `📥`, `📤`, `🔄`: 진행 중 (파란색)

### 예제 출력

```
📋 Notion → overrides.json 동기화
   주차: 3
   동기화 설정: 15개 주차 매핑됨

  → Week 3 로드 중...
    ✓ Week 3: 요약=true, 비디오=6개, 단계=5개
    → 변경됨

✓ 저장 완료: /path/to/overrides.json
✓ 1개 주차가 업데이트되었습니다.
```

## 제약 사항

### 현재 제한사항

- Node 18+에서만 기본 제공 fetch API 사용 (추가 npm 패키지 없음)
- Notion API v1 사용
- 텍스트 기반 콘텐츠만 지원 (데이터베이스 프로퍼티 아님)
- 블록 타입: paragraph, heading, bookmark, image, bulleted_list_item

### 확장 가능성

- 숫자/날짜/선택 프로퍼티 추가 가능
- 데이터베이스 쿼리로 자동 주차 감지
- 웹훅을 통한 실시간 동기화 가능

## 문제 해결

### Q: "Notion API error: 401"

A: Notion API 토큰이 유효하지 않거나 만료됨.
- `notion-config.json`에서 토큰 확인
- Notion Integrations 페이지에서 새 토큰 생성

### Q: "페이지 ID가 sync-config.json에 없습니다"

A: `sync-config.json`에 해당 주차의 페이지 ID를 추가하세요.
- Notion URL에서 페이지 ID 추출
- 32자의 16진수 문자열

### Q: "블록을 찾을 수 없습니다"

A: Notion 페이지에 콘텐츠가 없거나 로드 실패.
- Notion 페이지가 존재하는지 확인
- API 토큰에 페이지 읽기 권한이 있는지 확인
- 네트워크 연결 확인

### Q: "overrides.json 저장 실패"

A: 파일 시스템 권한 문제.
```bash
# 디렉토리 권한 확인
ls -la /path/to/course-site/data/
# 필요시 권한 변경
chmod 755 /path/to/course-site/data/
```

## 보안 고려사항

⚠️ **주의**: Notion API 토큰은 민감한 정보입니다.

- `.gitignore`에서 `notion-config.json` 제외
- 환경 변수 사용 권장
- 토큰 평문 저장 금지
- 주기적으로 토큰 갱신

```bash
# 안전한 사용 예제
export NOTION_TOKEN="ntn_..."
./start-admin.sh sync-from-notion
```

## 성능 고려사항

- 모든 주차 동기화: ~15-30초 (API 요청 수에 따라)
- 특정 주차만 동기화: ~2-5초
- Notion API 레이트 리밋: 일반적으로 문제 없음 (3 req/sec)

## 자동화

### 정기적 동기화

```bash
# cron을 사용한 자동 동기화 (매일 자정)
0 0 * * * cd /path/to/RPD && ./start-admin.sh sync-all >> /var/log/sync.log 2>&1
```

### GitHub Actions (선택사항)

`.github/workflows/sync.yml` 파일 생성:

```yaml
name: Notion Sync
on:
  schedule:
    - cron: '0 0 * * *'  # 매일 자정

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - env:
          NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
        run: node tools/notion-sync.js --all
      - uses: actions/commit@v3
        with:
          message: 'chore: sync from Notion'
```

## 참고 문서

- [Notion API Documentation](https://developers.notion.com/reference)
- [Notion Integration Guide](https://developers.notion.com/docs/getting-started)
- [Course Site Documentation](../course-site/CONTENT_GUIDE.md)
