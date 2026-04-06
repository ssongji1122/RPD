# RPD 사이트: Archive → Edu Home 전환 설계 명세

**작성일**: 2026-04-05  
**담당**: CPO (RPD-4)  
**상태**: Draft v1  
**산출물**: IA 설계 + SoT 경계 + 단계적 마이그레이션 플랜

---

## 0. 현황 요약 (As-Is)

### 현재 사이트 구조

| 페이지 | 파일 | 현재 역할 | 문제점 |
|--------|------|-----------|--------|
| Archive/Home | `index.html` | 주차 카드 갤러리 | 학습 경로 불명확, Archive 레이블이 정체성 혼란 유발 |
| Class | `inha.html` | 인하대 전용 뷰 | 일반 학습자 배제, Notion 대시보드와 역할 중복 |
| Studio | `studio.html` | 개인 덱 관리 | localStorage만, 진도 트래킹 미연동 |
| Library | `library.html` | Show Me 카드 검색 | 주차 맥락 없이 카드만 나열 |
| Shortcuts | `shortcuts.html` | Blender 단축키 DB | 주차 학습 흐름과 단절 |
| Week Detail | `week.html?week=N` | 주차 상세 | Notion 참고자료(`references.json`)가 별도 탭으로만 접근 가능 |

### 주요 통증 포인트

1. **이중 관리 위험**: 콘텐츠 변경 시 사이트 JSON ↔ Notion 간 sync 깨짐 가능
2. **왕복 이동 강요**: "이 주차에서 뭘 공부해야 하나?" → 사이트 week 페이지 + Notion 참고자료 두 곳 탐색 필요
3. **Archive 포지셔닝**: 학습 도구가 아닌 저장소처럼 인식되어 참여 유도 실패
4. **개인화 없음**: 수강생/공개 학습자/교수자 세 페르소나가 동일 진입점 사용

---

## 1. 목표 (To-Be)

> **Edu Home**: RPD의 모든 학습 자산에 대한 단일 진입점.  
> 수강생(인하대), 공개 학습자, 교수자(Course OS) 모두를 포괄하는 통합 학습 허브.

### 성공 기준

| 지표 | 목표 |
|------|------|
| 사이트 → Notion 왕복 이동 감소 | 주차 참고자료를 사이트에서 직접 접근 가능 |
| 콘텐츠 sync 오류율 | SoT 경계 명확화로 이중 수정 제거 |
| 신규 방문자 "다음 할 것" 파악 시간 | 3초 이내 (Cognitive UI 원칙 준수) |
| 주차 완주율 | 통합 학습 경로로 단계 이탈 감소 |

---

## 2. Source of Truth 전략: Hybrid (옵션 C)

브레인스토밍에서 결정된 핵심 아키텍처 결정.

### SoT 경계 정의

| 데이터 유형 | Canonical Source | 동기화 방향 |
|------------|-----------------|------------|
| **구조 데이터** | 사이트 JSON (`curriculum.json`, `references.json`) | 사이트 JSON → 렌더링 |
| 주차 메타데이터 (week, status, title, duration) | `curriculum.json` | 사이트 JSON이 최종 |
| 카드 목록 (Show Me, Library) | `curriculum.json` | 사이트 JSON이 최종 |
| 순서 및 관계 (week-step-task 계층) | `curriculum.json` | 사이트 JSON이 최종 |
| 참고자료 링크 목록 | `references.json` | Notion → pull → JSON cache |
| **서술형 콘텐츠** | Notion | Notion → pull → JSON cache |
| 주차 설명 (summary, 핵심 개념 본문) | Notion 주차 페이지 | Notion → pull → JSON cache |
| 튜토리얼 본문 | Notion 참고자료 페이지 | Notion → pull → JSON cache |
| 과제 안내 상세 | Notion 과제 마스터 DB | Notion → pull → JSON cache |
| 공지사항 | Notion 공지사항 DB | Notion → pull → JSON cache |

### 핵심 원칙

- **구조는 사이트가 소유**: 주차 순서, 카드 배치, 탐색 구조 변경은 JSON 수정 → 커밋
- **본문은 Notion이 소유**: 교수자가 Notion에서 서술형 콘텐츠 편집 → `sync_*.py` pull → JSON cache 갱신
- **사이트 → Notion 쓰기 없음**: 사이트는 읽기 전용 렌더러. 양방향 sync 불허.

---

## 3. Edu Home 정보 아키텍처 (To-Be IA)

### 3.1 네비게이션 재설계

**현재 탭 구조** (Archive / Class / Studio) → **새 탭 구조** (홈 / 주차 / 라이브러리)

| 탭 | 연결 페이지 | 대상 |
|----|-----------|------|
| **홈** | `index.html` (개편) | 전체 — 학습 허브 랜딩 |
| **주차** | `week.html?week=N` | 전체 — 주차별 통합 학습 뷰 |
| **라이브러리** | `library.html` | 전체 — Show Me 카드 검색 |
| ~~Class~~ | `inha.html` → Class 탭 제거, 인하대 필터 레이어로 흡수 | 수강생 |
| **스튜디오** | `studio.html` | 개인 학습자 |

> **Note**: `inha.html`은 장기적으로 `week.html`에 인하대 컨텍스트 레이어(수업일, 분반 정보)로 통합. Phase 2에서 처리.

### 3.2 Rail (사이드바) 재구성

**홈 탭 Rail**:
```
홈 (index.html)
현재 주차 바로가기 (week.html?week=current)
전체 커리큘럼 (커리큘럼 타임라인)
참고자료 (references 통합 뷰)
```

**주차 탭 Rail**:
```
Week 1: 수업 시작 준비
Week 2: Blender 기초
Week 3-5: 모델링
... (동적 생성, curriculum.json 기반)
```

**라이브러리 탭 Rail**:
```
카드 찾기 (library.html)
단축키 (shortcuts.html)
```

### 3.3 홈 랜딩 페이지 (index.html 개편)

**목표**: 신규 방문자가 3초 안에 "지금 뭘 해야 하나"를 파악.

**레이아웃 구조** (Cognitive UI 원칙 적용):

```
┌─────────────────────────────────────────┐
│ Hero Section (상단 고정, 뷰포트 40%)    │
│ "이번 주: Week N — [주차 제목]"         │
│ [주차 시작 CTA] [과제 보기 CTA]        │
├─────────────────────────────────────────┤
│ 커리큘럼 타임라인 (스크롤)             │
│ Week 1 ● Week 2 ● ... Week 15          │
│ (현재 주차 하이라이트, done/todo 상태)  │
├─────────────────────────────────────────┤
│ 참고자료 섹션                           │
│ [현재 주차 관련 Notion 참고자료 카드]   │
│ (references.json의 해당 주차 tutorials) │
├─────────────────────────────────────────┤
│ 공지사항 (선택적, Notion pull)         │
│ 최신 공지 2-3건                        │
└─────────────────────────────────────────┘
```

**Hero Section 로직**:
- `curriculum.json`에서 `status: "in_progress"` 또는 가장 최근 `done` 이후 주차를 "현재 주차"로 계산
- 인하대 수강생: `notion-mapping.json`의 수업 일정 기반 현재 주차 오버라이드 가능

### 3.4 주차 통합 뷰 (week.html 개편)

**핵심 목표**: Show Me 카드 + Notion 참고자료 + 과제를 하나의 학습 경로로 통합.

**현재 week.html 구조** → **새 구조**:

```
[현재]                          [To-Be]
──────────────────────          ──────────────────────────────
주차 헤더                       주차 헤더 + 한 줄 요약 (Notion pull)
단계별 실습 카드                 단계별 실습 카드 (curriculum.json)
  └ 각 단계 내용만                 └ + 관련 Show Me 카드 인라인 임베드
                                  └ + 단계별 참고자료 링크 (references.json)
과제 섹션                        과제 섹션
  └ curriculum.json 과제 체크리스트  └ + Notion 과제 상세 본문 (pull)
[별도 탭] 참고자료               참고자료 섹션 (통합, 별도 탭 불필요)
                                  └ tutorials[] 카드 그리드
                                  └ video_collections[] 토글
```

**단계-카드 연결 방식**:
- `curriculum.json`의 각 step에 `showme_cards: ["slug1", "slug2"]` 필드 추가 (Phase 2)
- 현재는 step 제목 키워드로 관련 Show Me 카드 자동 매칭 (Phase 1 임시)

### 3.5 참고자료 통합 뷰

**현재**: `references.json`이 `week.html` 하단에 별도 섹션으로만 존재  
**To-Be**: week.html의 단계 흐름 내에 인라인 삽입 + 독립 탐색 뷰

```
참고자료 카드 컴포넌트:
┌────────────────────────┐
│ [Notion 아이콘]        │
│ 튜토리얼 제목          │
│ Week N 관련            │
│ [Notion에서 열기 →]    │
└────────────────────────┘
```

---

## 4. 데이터 플로우 설계

### 4.1 전체 플로우 다이어그램

```
┌─────────────────────────────────────────────────────────────┐
│                        Notion Workspace                      │
│  📚 참고자료 페이지  │  주차 마스터 DB  │  과제 마스터 DB   │
└──────────┬──────────────────┬──────────────────┬────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
   sync_references.py   sync_course_content.py  (Phase 2: 신규 스크립트)
           │                  │                  │
           ▼                  ▼                  ▼
   references.json      curriculum.json     assignments.json (Phase 2)
           │                  │                  │
           └──────────────────┴──────────────────┘
                              │
                         course-site/data/
                              │
                    ┌─────────┴──────────┐
                    │   JavaScript       │
                    │   렌더링 레이어    │
                    │ (curriculum.js,    │
                    │  week.js 등)       │
                    └─────────┬──────────┘
                              │
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
          index.html      week.html      library.html
         (Edu Home)    (통합 학습 뷰)  (카드 검색)
```

### 4.2 동기화 트리거

| 이벤트 | 트리거 | 대상 스크립트 | 출력 |
|--------|--------|-------------|------|
| 참고자료 추가/수정 | 수동 (교수자 요청 or CI) | `sync_references.py` | `references.json` |
| 커리큘럼 내용 변경 | 수동 (교수자 요청 or CI) | `sync_course_content.py` | `curriculum.json` |
| 공지사항 업데이트 | Phase 2: GitHub Actions cron (매일 1회) | `sync_announcements.py` (신규) | `announcements.json` |
| 과제 상세 변경 | Phase 2 | `sync_assignments.py` (신규) | `assignments.json` |

### 4.3 캐시 전략

- 모든 Notion pull 결과는 `course-site/data/*.json`에 정적 파일로 캐시
- 브라우저가 JSON을 직접 fetch — Notion API key 노출 없음
- 갱신은 서버/CI에서 스크립트 실행 → 커밋 → 배포 주기로 관리

---

## 5. 단계적 마이그레이션 플랜

### Phase 1: 홈 랜딩 개편 (Edu Home v1)

**범위**: `index.html` 전면 개편. 다른 페이지 변경 없음.  
**예상 공수**: 2-3일

**작업 목록**:

1. **Hero 섹션 구현**
   - `curriculum.json`에서 현재 주차 자동 계산 로직
   - "현재 주차" 카드: 제목 + duration + 주요 토픽 3개
   - CTA: [주차 시작하기] → `week.html?week=N`, [과제 보기] → `week.html?week=N#assignment`

2. **커리큘럼 타임라인**
   - 15주 타임라인 컴포넌트 (현재 index.html의 주차 카드 갤러리를 선형 타임라인으로 전환)
   - 상태 뱃지: `done` (완료), `in_progress` (진행중), `todo` (예정)
   - 클릭 → `week.html?week=N`

3. **현재 주차 참고자료 미리보기**
   - `references.json`에서 현재 주차에 해당하는 `tutorials[]` 최대 4개 노출
   - "더보기" → `week.html?week=N#references`

4. **네비게이션 탭 레이블 변경**
   - `Archive` → `홈` (text만 변경, 구조 유지)

**완료 기준**:
- [ ] 신규 방문자가 3초 내 현재 주차와 다음 액션 파악 가능
- [ ] Notion 참고자료가 홈에서 직접 보임
- [ ] 모바일에서 타임라인 스크롤 정상 동작

---

### Phase 2: 주차 통합 뷰 (Week Page 개편)

**범위**: `week.html` 개편 + `references.json` 렌더링 통합 + 선택적 `inha.html` 흡수  
**예상 공수**: 3-4일

**작업 목록**:

1. **주차 헤더 강화**
   - Notion 주차 한 줄 요약 pull (캐시 from `curriculum.json` `summary` 필드 또는 신규 필드)
   - 주차 진도 표시 바 (완료 단계 / 전체 단계)

2. **참고자료 인라인 통합**
   - 각 step 섹션 하단에 관련 `references.json` tutorials 카드 자동 노출
   - 매핑 로직: `references.json`의 `sections[].weeks` 배열과 현재 주차 매칭
   - 주차 하단 "이 주차 전체 참고자료" 그리드 섹션

3. **Show Me 카드 인라인 임베드 (선택적)**
   - `curriculum.json`의 step 내 `showme_links` 필드 신설 (JSON 스키마 확장)
   - 관련 Show Me 카드 축소 버전(thumb) 인라인 노출
   - 클릭 → Show Me 카드 모달 또는 이동

4. **인하대 컨텍스트 레이어**
   - `notion-mapping.json`의 수업 일정 데이터를 `week.html`에 옵셔널 레이어로 추가
   - URL param: `week.html?week=N&class=inha` → 인하대 수업일, 분반 정보 노출
   - `inha.html`을 이 URL로 리다이렉트 처리 (구 URL 유지)

**완료 기준**:
- [ ] week 페이지에서 Notion 참고자료 직접 접근 가능
- [ ] Notion 왕복 이동 없이 주차 전체 학습 가능
- [ ] `inha.html` 기능이 week 페이지 레이어로 대체 가능

---

### Phase 3: 개인화 & Course OS 통합

**범위**: Studio 페이지 강화 + 교수자 도구 통합 + 공지사항 자동 동기화  
**예상 공수**: 5-7일 (장기)

**작업 목록**:

1. **개인 학습 경로 트래킹**
   - 주차별 완료 단계 localStorage 저장 → Studio 페이지에 진도 집계 표시
   - "마지막으로 본 곳" 재개 버튼 (홈 Hero에 노출)

2. **공지사항 자동 동기화**
   - `sync_announcements.py` 스크립트 작성 (Notion 공지사항 DB → `announcements.json`)
   - GitHub Actions cron으로 매일 1회 자동 실행
   - 홈 하단에 공지사항 섹션 추가

3. **과제 상세 Notion 연동**
   - `sync_assignments.py` 스크립트 작성 (Notion 과제 마스터 DB → `assignments.json`)
   - `week.html` 과제 섹션에 Notion 본문 렌더링 (Markdown → HTML)

4. **교수자 Edu Home 뷰**
   - `admin.html`에 "과목 현황" 대시보드 추가: 주차 진행 상태, 제출 현황
   - Course OS 포지셔닝 문서의 KPI 지표 반영

---

## 6. 컴포넌트 명세

### 6.1 CurrentWeekHero

```html
<!-- 위치: index.html Hero Section -->
<section class="edu-hero" aria-label="현재 주차">
  <div class="edu-hero__week-badge">Week N</div>
  <h1 class="edu-hero__title">[주차 제목]</h1>
  <p class="edu-hero__subtitle">[주차 부제목]</p>
  <div class="edu-hero__meta">
    <span>[duration]</span>
    <span>[topic chips max 3개]</span>
  </div>
  <div class="edu-hero__actions">
    <a href="week.html?week=N" class="rpd-btn rpd-btn--primary">주차 시작하기</a>
    <a href="week.html?week=N#assignment" class="rpd-btn rpd-btn--ghost">과제 보기</a>
  </div>
</section>
```

**데이터 소스**: `curriculum.json` — `status: "in_progress"` 주차 또는 마지막 `done` 이후

### 6.2 CurriculumTimeline

```html
<!-- 위치: index.html 메인 콘텐츠 -->
<nav class="curriculum-timeline" aria-label="커리큘럼 타임라인">
  <!-- curriculum.json 기반 동적 생성 -->
  <a class="timeline-week timeline-week--done" href="week.html?week=1">
    <span class="timeline-week__num">W1</span>
    <span class="timeline-week__title">수업 시작 준비</span>
    <span class="timeline-week__status">완료</span>
  </a>
  <!-- ... -->
</nav>
```

### 6.3 ReferenceCard

```html
<!-- 위치: index.html 참고자료 섹션, week.html 참고자료 섹션 -->
<a class="reference-card" href="[notion_url]" target="_blank" rel="noopener">
  <span class="reference-card__icon" aria-hidden="true"><!-- Notion SVG icon --></span>
  <span class="reference-card__title">[tutorial.title]</span>
  <span class="reference-card__week">Week [N]</span>
  <span class="reference-card__cta">Notion에서 열기</span>
</a>
```

**데이터 소스**: `references.json` → `sections[].tutorials[]`

---

## 7. 설계 제약 & 원칙 준수

### Cognitive UI 원칙 (COGNITIVE_UI_GUIDE 기반)

| 원칙 | 적용 |
|------|------|
| 3초 파악 | Hero Section이 항상 "현재 주차 + 다음 액션"을 최우선 노출 |
| 단계적 공개 | 홈: 현재 주차 요약만 / 주차 페이지: 상세 단계 / Notion: 전문 본문 |
| 밀집 표면 = 이름 우선 | 타임라인에서 week title만 노출, 상세는 클릭 후 |
| 단일 비교 축 | 홈에서 주차 진행 상태(done/in_progress/todo) 하나만 |

### 디자인 시스템 준수 (DESIGN_SYSTEM.md)

- 모든 스타일은 `tokens.css` 변수 사용
- 아이콘: Lucide SVG (`aria-hidden="true"`, `stroke="currentColor"`)
- 새 컴포넌트는 `.rpd-*` 클래스 네이밍 유지
- 인라인 `<style>` 금지, 하드코딩 rgba 금지

### 한국어 타이포그래피

- 본문 `line-height: 1.7`, UI 레이블 `line-height: 1.4`
- 어조: `~해요/~있어요` 체 유지

---

## 8. 미결 결정 사항 (Open Questions)

| 항목 | 내용 | 결정 필요자 |
|------|------|-----------|
| OQ-1 | Hero의 "현재 주차" 자동 계산 기준: 날짜 기반(수업 일정) vs. `curriculum.json` status 기반? | 교수자 |
| OQ-2 | Phase 2에서 `inha.html`을 완전 제거할지, 리다이렉트만 유지할지? | 교수자 (URL 공유 여부 확인) |
| OQ-3 | 공지사항 sync 주기: 매일 1회 자동 vs. 교수자 수동 트리거? | 운영 편의에 따라 |
| OQ-4 | Show Me 카드 인라인 임베드 시 모달 vs. 페이지 이동 (UX 결정)? | 사용자 테스트 필요 |

---

## 9. 다음 단계

1. **Phase 1 즉시 착수**: `index.html` Hero 섹션 + 타임라인 개편
2. OQ-1, OQ-2를 교수자와 확인 후 Phase 2 계획 확정
3. Phase 2 전 `curriculum.json` 스키마 확장 (showme_links 필드) PR 작성
4. Phase 3 공지사항 sync 스크립트는 별도 이슈로 분리

---

*이 문서는 [RPD-4](/RPD/issues/RPD-4)의 산출물입니다.*
