# Notion ↔ 웹 동기화 시스템

빠른 시작 가이드

## 설치 완료 파일

- ✅ `tools/notion-sync.js` - Notion → 웹 동기화
- ✅ `tools/web-to-notion.js` - 웹 → Notion 동기화
- ✅ `tools/sync-config.json` - 주차별 페이지 ID 설정
- ✅ `start-admin.sh` - 통합 관리 스크립트 (업데이트됨)
- ✅ `tools/SYNC_GUIDE.md` - 상세 설명서

## 빠른 시작

```bash
# Notion → 웹 동기화 (모든 주차)
./start-admin.sh sync-from-notion

# 웹 → Notion 동기화 (모든 주차)
./start-admin.sh sync-to-notion

# 양방향 동기화
./start-admin.sh sync-all

# 특정 주차만 동기화
NOTION_TOKEN="your_token_here" \
node tools/notion-sync.js --week 3
```

## 필수 설정 확인

### 1. Notion API 토큰

파일: `course-site/data/notion-config.json`

```json
{
  "enabled": true,
  "token": "your_notion_api_token_here",
  "databaseId": "d27c5dfdac27433284a4a6be1b6d8801"
}
```

✓ 기본값 포함됨 - 필요시 업데이트

### 2. 주차별 페이지 ID

파일: `tools/sync-config.json`

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

✓ 모든 15개 주차 ID 매핑됨

## 동작 방식

### Notion → 웹 (`notion-sync.js`)

```
Notion 페이지 읽기
    ↓ (제목, 단락, 북마크, 이미지 블록)
콘텐츠 분류
    ↓ (status, summary, videos, steps, explore)
curriculum override 데이터 생성
    ↓
overrides.json 업데이트
```

**Notion 페이지 섹션:**
- `상태` → status (done/active/upcoming)
- `요약` → summary
- `비디오` → videos (북마크)
- `단계` → steps (제목 + 이미지 + 불릿)
- `탐색` → explore (불릿 리스트)

### 웹 → Notion (`web-to-notion.js`)

```
student-progress.json 읽기
    ↓
주차별 진행도 추출
    ↓
Notion 페이지 블록 업데이트
    ├─ 기존 블록 삭제
    ├─ 진행도 정보 추가
    ├─ 체크리스트 작성
    └─ 동기화 메타데이터 기록
```

## 구조도

```
course-site/data/
├── notion-config.json       ← Notion API 토큰
├── curriculum.js            ← 메인 커리큘럼 (수동 편집)
├── overrides.json           ← Notion에서 동기화됨 (자동 갱신)
└── student-progress.json    ← Notion으로 동기화됨 (자동 갱신)

tools/
├── notion-sync.js           ← 동기화 스크립트 (Notion → 웹)
├── web-to-notion.js         ← 동기화 스크립트 (웹 → Notion)
├── sync-config.json         ← 페이지 ID 매핑
├── SYNC_GUIDE.md            ← 상세 설명서
└── README-SYNC.md           ← 이 파일

시작 스크립트:
├── start-admin.sh           ← 통합 관리 명령 (업데이트됨)
```

## 주요 기능

### 오류 처리
- ✅ API 실패해도 기존 데이터 보존
- ✅ 개별 주차 실패해도 다른 주차는 계속 진행
- ✅ 상세한 오류 메시지 제공

### 변경 추적
- ✅ 변경사항만 저장 (불필요한 업데이트 방지)
- ✅ 종료 코드: 0 = 변경됨, 2 = 변경 없음, 1 = 오류

### 로깅
- ✅ 각 주차별 진행 상황 표시
- ✅ 수집된 데이터 통계 (요약, 비디오, 단계 개수)
- ✅ 최종 결과 요약

## 응용 예제

### 예제 1: Notion에서 Week 3 편집 후 웹에 반영

```bash
# Notion UI에서 Week 3 페이지 수정
# → 대시보드에서 다음 명령 실행:

./start-admin.sh sync-from-notion

# → course-site/data/overrides.json 자동 업데이트
# → 웹 페이지 새로고침하면 변경사항 반영됨
```

### 예제 2: 학생 진행도를 Notion에 기록

```bash
# 학생 진행도를 course-site/data/student-progress.json에 저장
# (LocalStorage에서 내보내기 등)

./start-admin.sh sync-to-notion

# → Notion 페이지에 진행도 정보 기록됨
# → 교사가 Notion에서 전체 학생 진행도 한눈에 확인 가능
```

### 예제 3: 정기적 자동 동기화 (cron)

```bash
# /etc/crontab에 추가 (매일 자정)
0 0 * * * cd /path/to/RPD && ./start-admin.sh sync-all >> /var/log/sync.log 2>&1

# 또는 시스템 타이머 (systemd)
sudo systemctl enable notion-sync.timer
```

## 파일 포맷 참고

### overrides.json 구조
```json
{
  "weeks": {
    "3": {
      "status": "active",
      "summary": "설명...",
      "videos": [{"title": "...", "url": "..."}],
      "steps": {
        "0": {
          "image": "assets/...",
          "done": ["체크리스트 항목"]
        }
      },
      "explore": [{"title": "...", "hint": "..."}]
    }
  }
}
```

### student-progress.json 구조
```json
{
  "weeks": {
    "3": {
      "status": "active",
      "checklist": [
        {
          "id": "w3-t1",
          "label": "작업 설명",
          "completed": false
        }
      ]
    }
  }
}
```

## 문제 해결

| 문제 | 원인 | 해결 |
|------|------|------|
| "API error: 401" | 토큰 만료/유효하지 않음 | `notion-config.json` 토큰 갱신 |
| "페이지 ID가 없습니다" | sync-config.json 설정 부재 | Notion URL에서 페이지 ID 추출해 추가 |
| "블록을 찾을 수 없습니다" | Notion 페이지 비어있음 | 페이지에 콘텐츠 추가 |
| "저장 실패" | 파일 권한 문제 | `chmod 755 course-site/data/` 실행 |

## 보안

⚠️ **중요:** Notion API 토큰은 비밀 정보입니다.

- `.gitignore`에 `notion-config.json` 추가
- 환경 변수로 토큰 관리 권장
- 토큰 주기적 갱신

```bash
# 환경 변수 사용 (권장)
export NOTION_TOKEN="ntn_..."
./start-admin.sh sync-from-notion
```

## 다음 단계

1. **상세 설명서 읽기**: `tools/SYNC_GUIDE.md`
2. **테스트**: `./start-admin.sh sync-from-notion --week 3`
3. **Notion 구조 확인**: Week 3 페이지에서 섹션 레이아웃 검증
4. **정기 동기화 설정**: cron 또는 GitHub Actions 구성

## 지원

문제 발생 시:
1. `SYNC_GUIDE.md` 문제 해결 섹션 참고
2. 콘솔 로그 확인 (오류 메시지 상세함)
3. sync-config.json과 notion-config.json 설정 재확인
