# RPD 카드 SSoT 시스템 설계

**날짜:** 2026-05-18
**범위:** ShowMe 카드를 Notion DB SSoT 기반 모듈 카드 시스템으로 전환. 퀴즈 제거. steps + videos sidecar 추가. Card DB + Week 인라인 공존.
**상태:** Draft (User review pending)

---

## 1. 목표

수업 콘텐츠를 **재사용 가능한 모듈 카드**로 구조화한다. 카드 1개 = 한 개념·도구·기법. 콘텐츠는 Notion이 SSoT, 레이아웃·인터랙티브 위젯은 repo가 소유. 생성기가 둘을 결합해 ShowMe HTML을 빌드. 커리큘럼은 카드 ID 시퀀스로 주차를 조립한다.

목적:
- 같은 개념(Mirror, Array 등)을 여러 주차에서 중복 작성하는 비용 제거
- Blender 5.x 변경 시 카드 1곳 수정으로 전 주차 반영
- 단축키·따라하기 절차·추천 영상·흔한 실수를 카드별로 표준화
- 학생이 카드 단위 검색·복습 가능

비목표:
- 인터랙티브 위젯(Canvas/Three.js) 코드를 Notion에 넣지 않는다 — repo 유지
- 기존 79 ShowMe HTML을 한 번에 전부 마이그레이션하지 않는다 — 점진 이전
- 퀴즈 시스템은 제거 (사용자 결정 2026-05-18)

## 2. 현재 상태 (조사 결과)

| 항목 | 현황 |
|---|---|
| ShowMe HTML 카드 수 | 79개 (`course-site/assets/showme/{id}.html`) |
| 메타데이터 | `_registry.js` (id, label, icon, week) |
| 보충 설명 | `_supplements.json` (analogy, before_after, confusion, takeaway) — brainstormC 산출물 |
| 카테고리 매핑 | `_catalog.json` |
| 커리큘럼 연결 | `course-site/data/curriculum.js`에 `"showme": "{id}"` 문자열 |
| Week 페이지 (Notion) | 콘텐츠 인라인 — 비유표·단축키·추천영상·흔한실수 모두 본문에 직접 |
| ShowMe 카드 전용 Notion DB | **없음** |
| 카드 간 관계 (prerequisites, related) | **없음** |
| Step-by-step 절차 카드 | **없음** (Week 페이지 본문에만 존재) |
| 추천 영상 카드 단위 | **없음** (Week 페이지에 인라인) |
| 퀴즈 | 모든 ShowMe HTML 탭 4 (75% 통과) — **제거 대상** |

## 3. 아키텍처

### 3.1 데이터 흐름

```
[Notion Card DB]                       [Repo]
    │                                   │
    │ card_id, concept, usage,          │ assets/showme/{id}.canvas.js
    │ pitfall, steps, videos,           │ assets/showme/_template.html
    │ widget_id, week[]                 │ assets/showme/styles/*.css
    │                                   │
    └──────────────┬────────────────────┘
                   │
                   ▼
            [showme-build]
            (생성기 스크립트)
                   │
                   ▼
       course-site/assets/showme/
       ├── {id}.html  (DB + widget 결합)
       ├── _registry.js  (DB로부터 재생성)
       └── _catalog.json (DB로부터 재생성)
```

### 3.2 책임 분리

| 영역 | SSoT | 편집 도구 |
|---|---|---|
| 카드 텍스트 (concept/usage/pitfall) | Notion Card DB | Notion UI 또는 MCP |
| Step-by-step 절차 | Notion Card DB (JSON 필드) | Notion UI |
| 추천 영상 목록 | Notion Card DB (relation 또는 JSON) | Notion UI |
| 위젯 코드 (Canvas/Three.js 인터랙션) | repo | 코드 에디터 |
| HTML 레이아웃·CSS | repo (`_template.html`) | 코드 에디터 |
| 커리큘럼 시퀀스 | Notion Week 페이지 + `curriculum.js` | 기존 `/curriculum sync` |
| 메타 인덱스 (`_registry.js`) | DB로부터 생성 (파생물) | 생성기 자동 |

## 4. Notion Card DB 스키마

DB 이름: **ShowMe Cards**
위치: `studio.soluta — 수업자료 허브` 산하 신규 DB

| 속성 | 타입 | 설명 | 예시 |
|---|---|---|---|
| `card_id` | Title | kebab-case 고유 식별자 | `array-modifier` |
| `label` | Text | 한국어 표시 라벨 | `Array Modifier 이해` |
| `icon` | Text | Lucide 아이콘명 (이모지 금지) | `repeat-2` |
| `category` | Select | modeling / edit-mode / modifier / object / scene / material / ai / sculpt / animation / rigging / render | `modifier` |
| `week` | Multi-select | 1-15 (재사용 시 복수) | `3, 4` |
| `priority` | Select | P0 / P1 / P2 | `P0` |
| `status` | Select | planned / draft / published / deprecated | `published` |
| `concept_md` | Rich text | 비유 + 핵심 개념 설명 (Markdown) | "거울 앞에 서면 반대편이..." |
| `usage_md` | Rich text | 언제 쓰는지 (Markdown) | "좌우 대칭 모델링..." |
| `pitfall_md` | Rich text | 흔한 실수 + 해결 (Markdown) | "Clipping 꺼져 있으면..." |
| `steps_json` | Rich text | Step 절차 JSON | (스키마 4.1) |
| `videos_relation` | Relation → Videos DB | 추천 영상 (다중 카드 공유) | |
| `widget_id` | Text | repo의 인터랙티브 위젯 식별자 | `array-modifier` |
| `blender_version` | Text | 검증된 Blender 버전 | `5.0` |
| `official_docs` | URL | Blender 공식 docs | https://docs.blender.org/... |
| `prerequisites` | Relation → 자기 DB | 선행 카드 | `edit-mode-enter` |
| `related` | Relation → 자기 DB | 관련 카드 | `mirror`, `subdivision-surface` |

### 4.1 `steps_json` 스키마

```json
{
  "blender_version": "5.0",
  "platform_note": "macOS는 Ctrl → Cmd로 대체 가능",
  "steps": [
    {
      "n": 1,
      "action": "Cube 추가",
      "hotkey": "Shift + A",
      "menu": "Add → Mesh → Cube",
      "screenshot": "steps/array-01.png",
      "note": null
    },
    {
      "n": 2,
      "action": "Modifier Properties 열기",
      "hotkey": null,
      "menu": "Properties → 🔧 Modifier 탭",
      "screenshot": "steps/array-02.png",
      "note": "렌치 아이콘"
    }
  ]
}
```

### 4.2 Videos DB (별도)

DB 이름: **ShowMe Videos**

| 속성 | 타입 | 설명 |
|---|---|---|
| `title` | Title | 영상 제목 |
| `url` | URL | YouTube 또는 Blender Studio URL |
| `channel` | Text | 채널명 |
| `duration_sec` | Number | 길이 (초) |
| `language` | Select | ko / en / etc |
| `blender_version` | Text | 영상 기준 Blender 버전 |
| `official` | Checkbox | Blender Studio 공식 여부 |
| `recommended_reason` | Text | 추천 사유 (1줄) |
| `last_verified` | Date | 마지막 링크 유효성 확인일 |

**관계:** 카드 → 영상 = N:M. 한 영상이 여러 카드에 추천될 수 있음 (예: Blender Guru 모디파이어 영상 = Array + Mirror + Boolean).

## 5. 생성기 (`showme-build`)

### 5.1 위치

`scripts/showme/build.py` (Python). Notion MCP 또는 notion-client SDK 사용.

### 5.2 동작

```
1. Notion Card DB 전체 fetch (status != deprecated)
2. 각 row마다:
   a. _template.html 로드
   b. {{LABEL}}, {{CONCEPT}}, {{USAGE}}, {{PITFALL}}, {{STEPS}}, {{VIDEOS}}, {{DOCS}} 치환
   c. widget_id 있으면 → assets/showme/widgets/{widget_id}.js를 <script> include
   d. 출력: course-site/assets/showme/{card_id}.html
3. _registry.js 재생성: [{id, label, icon, week, category, status}]
4. _catalog.json 재생성: category → [card_ids]
5. _supplements.json은 deprecated (pitfall_md로 흡수)
6. 검증: 모든 widget_id에 해당 JS 파일 존재 확인, 모든 official_docs URL 200
```

### 5.3 HTML 탭 구조 (퀴즈 제거 후)

```
<nav class="tabs">
  탭 1: 개념        (concept_md 렌더)
  탭 2: 따라하기     (steps_json 렌더 — 단축키 키캡 + 스크린샷)
  탭 3: 인터랙션    (widget_id 있을 때만 표시. canvas + controls)
  탭 4: 언제 쓰나요  (usage_md + pitfall_md + related 카드 링크)
  탭 5: 영상        (videos_relation 렌더)
</nav>
```

위젯 없는 카드 (Step-only, Concept-only)는 탭 3 자동 숨김.

### 5.4 incremental build

```
showme-build --card array-modifier   # 단일 카드
showme-build --week 3                # Week 3 카드 전체
showme-build --all                   # 전체 (CI/배포 전)
showme-build --check                 # 변경된 카드만 재생성 (last_edited_time 비교)
```

## 6. 스킬 카탈로그

### 6.1 신규

| 스킬 | 역할 |
|---|---|
| `/showme-build` | Notion DB → HTML 생성. 단일·주차·전체 모드 |
| `/showme-new {card_id}` | Notion에 신규 row 생성 (템플릿 채워서) |
| `/showme-migrate {card_id}` | 기존 `{id}.html` 파싱 → Notion row 생성 (마이그레이션) |
| `/showme-video-add {card_id} {url}` | 영상 후보 검증 → Videos DB row + 카드 relation |

### 6.2 변경

| 스킬 | 변경 |
|---|---|
| `/showme` | DB row 생성 후 `/showme-build {card_id}` 호출하는 wrapper로 변경. 기존 카드 직접 작성 모드는 deprecated 경고 |
| `/showme verify` | sidecar 대신 DB 무결성 검증 (필수 필드, widget_id 존재, official_docs 응답) |
| `/brainstormC` | 출력 대상을 `_supplements.json` → Card DB `pitfall_md` 필드로 변경. 마이그레이션 완료 후 deprecate |
| `/rpd-check` | Phase 1.3 = DB row ↔ HTML 일관성 검증 |

### 6.3 유지

| 스킬 | 변경 없음 |
|---|---|
| `/curriculum sync` | `curriculum.js`의 `"showme": "{id}"` 그대로 유효 |
| `/sync` | 사이트 발행 그대로 |
| `/capture` | 스크린샷 캡처 그대로. `steps_json`의 `screenshot` 필드 채우는 용도 |

## 7. 마이그레이션 계획

### Phase 1 — 인프라 (1-2일)

1. Notion에 **ShowMe Cards** DB 생성 (4장 스키마)
2. Notion에 **ShowMe Videos** DB 생성 (4.2)
3. `scripts/showme/build.py` PoC — Card DB 1 row → HTML 1개 생성
4. `_template.html` 퀴즈 탭 제거 + steps 탭 추가 변형
5. 신규 카드 1개 (`collection-outliner`) 전체 작성으로 검증

### Phase 2 — 신규 백로그 (3-5일)

ShowMe 신규 카드 보강 계획 백로그 (Notion `32754d65-4971-81fc-b832-f8cbb3388e66`) 8개 신규 작성:

P0: `collection-outliner`, `modifier-stack-order`, `shade-smooth-auto-smooth`, `merge-by-distance`, `bridge-edge-loops`
P1: `duplicate-vs-linked-duplicate`, `face-orientation-normals`, `apply-modifier-vs-keep-procedural`

각 카드 = 신규 DB row + 위젯 코드(필요 시) + 스크린샷 캡처.

### Phase 3 — 기존 79카드 마이그레이션 (1주)

자동 마이그레이션:
1. HTML 파싱: 탭 1 → `concept_md`, 탭 2 위젯 코드 → repo `widgets/{id}.js`로 분리, 탭 3 → `usage_md`, 탭 4 퀴즈 → 폐기
2. `_supplements.json` 매칭 → `pitfall_md` 필드 채움
3. `_registry.js` → `label`, `icon`(이모지→Lucide 변환표), `week` 채움
4. 우선순위: 재사용 빈도 높은 카드부터 (Mirror, Array, Boolean, Subdivision, Extrude 등)

수동 보강 필요 항목 (`steps_json`, `videos_relation`):
- 마이그레이션 자동화 불가
- 카드별 별도 작업. Week 페이지 인라인의 추천 영상을 Videos DB로 추출

### Phase 4 — Week 페이지 정리 (1주)

각 주차 Notion 페이지에서:
- 카드화된 콘텐츠 (Mirror, Array 등) 인라인 → 카드 link/embed로 교체
- 추천 영상 인라인 → Videos DB 참조로 교체
- 인라인으로 남는 것: 학습 목표, 흐름 설명, 종합 실습, 과제, 단축키 퀵 레퍼런스

### Phase 5 — Cleanup (1일)

- `_supplements.json` 완전 폐기 (모든 pitfall이 DB로 이전된 후)
- `/brainstormC` deprecated 처리
- ShowMe HTML 퀴즈 코드 제거 (`initQuiz`, `postMessage`)
- `week.html` 모달의 퀴즈 완료 핸들러 제거

## 8. 컴포넌트 경계

| 컴포넌트 | 책임 | 의존성 |
|---|---|---|
| Notion Card DB | 카드 콘텐츠 SSoT | — |
| Notion Videos DB | 영상 메타 SSoT | — |
| `scripts/showme/build.py` | DB → HTML 빌드 | notion-client, repo template |
| `assets/showme/widgets/{id}.js` | 인터랙티브 위젯 코드 | DOM, canvas |
| `assets/showme/_template.html` | HTML 골격 | CSS 토큰 |
| `_registry.js`, `_catalog.json` | 파생 인덱스 (build이 생성) | DB |
| `week.html` 모달 | iframe 로더 + sidecar 섹션 렌더 | `{id}.html` |
| `/showme-build` 스킬 | build.py 호출 + 검증 보고 | build.py |
| `/showme-migrate` 스킬 | HTML 파싱 → DB row 생성 | beautifulsoup4, notion-client |

각 컴포넌트는 단방향 의존. DB → 빌드 → HTML → 페이지 순.

## 9. 에러 처리

| 시나리오 | 처리 |
|---|---|
| `card_id` 중복 | DB unique 제약 + build 시 fail |
| `widget_id`에 해당 JS 파일 없음 | build 경고, 탭 3 숨김 |
| `official_docs` URL 404 | build 경고, DB `status`를 `draft`로 자동 강등 후 PR 생성 |
| `prerequisites` relation에 deprecated 카드 | build 경고 |
| `steps_json` 파싱 실패 | build fail, 해당 카드만 skip |
| Notion API 429 | exponential backoff, 최대 3회 재시도 |
| 같은 카드 multi-week 노출 | 정상. `week` multi-select가 모든 노출 주차 표기 |

## 10. 테스트 전략

- **DB 스키마 valid**: 신규 row 생성 시 필수 필드 누락 → reject
- **build 멱등성**: 같은 DB 상태에서 두 번 build → 출력 동일 (timestamp 제외)
- **마이그레이션 fidelity**: 원본 HTML에서 추출한 concept 텍스트가 다시 build된 HTML에 1:1 등장
- **링크 무결성**: `prerequisites`/`related` relation에 deprecated 카드 없음
- **재생산성**: `_registry.js`, `_catalog.json` 삭제 후 build → 동일 결과
- **퀴즈 코드 부재**: build 결과 HTML에 `initQuiz` 문자열 없음

## 11. 결정 사항 요약

| 결정 | 선택 | 이유 |
|---|---|---|
| SSoT 위치 | Notion (콘텐츠) + repo (위젯·레이아웃) | 사용자 결정 2026-05-18 |
| 퀴즈 | 제거 | 사용자 결정 2026-05-18 |
| 마이그레이션 전략 | 공존 + 점진 이전 | 79카드 + 13주차 동시 이전 리스크 회피 |
| 신규 카드 시작점 | 백로그 8개 | 검증 + 가치 즉시 발생 |
| Videos | 별도 DB (relation) | 영상 다중 카드 공유 + 메타데이터 풍부 |
| Steps | Card DB JSON 필드 | 카드와 1:1, 별도 DB 불필요 |
| 위젯 코드 | repo만 (Notion 미포함) | 코드 편집·버전관리 필요 |
| Icon 표현 | Lucide 아이콘명 (이모지 금지) | 사용자 글로벌 피드백 준수 |

## 12. 미해결 / 후속

- Blender 5.0 단축키 변경분 (4.x → 5.x) 검증은 점진적. 카드 마이그레이션 시 사용자 검수 필요
- Videos DB 초기 시드 — Week 페이지 인라인 추천 영상 수집은 수동 1회 작업
- 학생 검색 UI (`library.html`) 확장 — prerequisites 그래프 시각화는 차후 별도 spec
- ShowMe 카드 다국어 (en) 지원은 비범위
