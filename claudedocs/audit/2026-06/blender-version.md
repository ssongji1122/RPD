# Blender 버전 정합성 감사 보고서

감사일: 2026-06-02  
기준 버전: Blender 5.0(.1)  
방법: grep + 직접 문맥 읽기  
감사자: Claude Code (Sonnet 4.6)

---

## 1. Stray 목록 (수정 대상)

| 우선순위 | 파일:위치 | 현재 텍스트 | 분류 | 판단 근거 | 제안 수정 | 수정경로 |
|---------|-----------|------------|------|-----------|-----------|---------|
| 중간 | `course-site/data/notion-blocks/pages/cd654d65-4971-837c-a634-01d321ff5527.json` (두 단락) | `Blender 4.4에서 사용하지 않는 머테리얼을 깔끔하게 삭제하려면 아래의 방법을 따라 하세요.` / `이 방법들을 활용하면 Blender 4.4에서 사용하지 않는 머테리얼을 효과적으로 정리할 수 있습니다.` | stray | 페이지 제목: "Blender에서 사용하지 않는 머테리얼 지우는 방법". 현재 수업 기준을 5.0으로 안내해야 하는 How-to 가이드인데 4.4로 특정. 머테리얼 Purge 기능은 5.0에서 동일하게 존재하므로 수정 안전 | `Blender 5.0에서` | Notion |

**Stray 총 1건**

---

## 2. 의도적이라 유지해야 하는 패턴

### 패턴 A: 버전 경고 — "4.x 이하는 안 됩니다"

**예시: `syllabus.md` line 15**
> "이전 버전(4.x 이하)은 UI 및 기능 차이로 인해 실습 진행이 어려울 수 있습니다."

판단: 5.0 기준 수업임을 강조하기 위해 4.x를 대조 대상으로 명시. 의도적.

---

### 패턴 B: LTS vs 최신 버전 비교표

**예시: `course-site/data/notion-blocks/week02.json` (table_row)**
> 표 열 구조: `LTS (Long Term Support) | 최신 버전 (Latest)`  
> 현재 버전 행: `4.5 LTS | 5.0`

판단: LTS 트랙과 최신 트랙의 현재 버전을 나란히 비교하는 표. 두 숫자가 다른 것이 정상 (LTS와 최신은 다른 릴리즈 트랙). 5.0이 최신 버전 칸에 올바르게 표시되어 있음. 유지.

---

### 패턴 C: 기능 도입 이력 — "X 버전부터 추가"

**예시: `course-site/data/notion-blocks/week07.json`**
> "Blender 4.3 버전부터 세 가지 새로운 UV 언래핑 방법이 추가되었습니다: Angle Based, Conformal…"

판단: 5.0에 포함된 기능의 도입 시점 안내. 학생이 "왜 구버전 튜토리얼엔 이 옵션이 없지?"를 이해하도록 필요한 문맥. 유지.

**예시: `course-site/data/notion-blocks/week05.json`**
> "Blender 4.1 이하 주요 방식. 4.2+에서도 계속 지원"  
> "Extension (신규) — 원클릭 설치 (Blender 4.2+)"

판단: Add-on vs Extension 변경 이력. 구버전 설치 방식을 설명해 학생이 외부 튜토리얼과 비교할 때 혼동을 줄임. 유지.

**예시: `course-site/data/notion-blocks/week06.json`**
> "─── Blender 4.5 간편 리토폴로지 (Farrukh 3D) ───"

판단: 외부 YouTube 강의 제목을 그대로 인용한 섹션 구분자. 유지.

---

### 패턴 D: 기본값·단축키 변경 이력

**예시: `course-site/data/notion-blocks/week09.json` / `week13.json`**
> "AgX — Blender 4.0+ 기본값"  
> "(Blender 4.0+에서 기본 View Transform)"

판단: AgX가 언제부터 기본값이 됐는지 설명. 학생이 예전 튜토리얼과 차이를 이해하는 데 필요. 유지.

**예시: `course-site/data/notion-blocks/week12.json`**
> "Blender 4.0+ 단축키 변경: Weight Paint 모드에서 본 선택은…"

판단: 단축키 변경 이력. 구버전 튜토리얼 참조 시 혼동 방지. 유지.

---

### 패턴 E: 외부 도구·애드온 자체 요구사항

**예시: `course-site/assets/showme/blender-mcp.html` (line 322)**
> `<li><strong>Blender 4.0+</strong> — blender.org에서 최신 버전</li>`

판단: 이 ShowMe는 커뮤니티 애드온 `ahujasid/blender-mcp`의 사전 준비물을 설명하는 탭. 해당 애드온이 실제로 Blender 4.0+와 호환된다는 소프트웨어 사실 기술. `resources/blender-mcp-setup.md`의 "방법 B: 서드파티 애드온 (권장, Blender 4.x ~ 5.0)"과 동일한 사실. 유지. (단, 학생이 "4.0이면 충분하다"고 오해할 여지가 있으므로, 해당 요구사항 아래 "수업 기준: Blender 5.0" 주석 추가는 UX 개선 관점에서 검토 가능 — 이는 버전 stray와 별개)

**예시: `resources/blender-mcp-setup.md`**
> "방법 A: 공식 애드온 (Blender 5.1 이상)"  
> "방법 B: 서드파티 애드온 (권장, Blender 4.x ~ 5.0)"

판단: 공식 MCP 애드온(5.1 요구)과 커뮤니티 애드온(4.x~5.0 호환)의 호환성을 각각 사실 기술. 유지.

**예시: `weeks/week10-animation/lecture-note.md` / `course-site/data/notion-blocks/week10.json`**
> "MCP 활용 심화 — Blender 5.1 + Claude Code 공식 Connector"  
> "Blender 5.1 이상 필요. 이전 버전(5.0 포함)은 공식 MCP add-on을 지원하지 않음"

판단: 공식 Connector의 요구사항(외부 사실). "5.0 포함 불가"를 명시하므로 학생이 오해할 소지 낮음. 유지.

---

### 패턴 F: 외부 자료 버전 표기

**예시: `course-site/data/notion-blocks/pages/7c954d65...json` (Mixamo 페이지)**
> "공식 Adobe 배포(Blender 3.6 계열)"  
> "Rigify가 포함된 Blender 2.80 이상 권장"

판단: Mixamo 애드온 자체 요구사항 및 버전 이력. 외부 소프트웨어 사실 기술. 유지.

**예시: `course-site/data/notion-blocks/pages/68254d65...json` (Weight Painting 서브페이지)**
> "Blender 4.0 기준 최신 워크플로우와 테크닉을 빠짐없이 소개"

판단: 외부 튜토리얼 자료 설명. 해당 영상이 4.0 기준으로 제작된 것을 명시. 유지.

---

### 패턴 G: 트러블슈팅 이력 문서

**예시: `course-site/data/notion-blocks/pages/62254d65...json` (파티클 트러블슈팅 서브페이지)**
> "일부 Blender 4.3 초기 릴리즈에서는 파티클 및 컴포지터 노드 관련 문제가 보고된 바 있습니다."

**예시: `course-site/data/notion-blocks/pages/ad554d65...json` (섀도우 트러블슈팅 서브페이지)**
> "Blender 4.3 Eevee-Next 엔진 이슈: …"  
> "Blender 4.1/4.2 안정 버전 또는 4.4 Daily Build에서 테스트"

판단: 수업 당시 특정 버전 환경에서 발생한 버그 이력 문서. 아카이브성이므로 수정하면 이력이 소실. 유지.

---

### 패턴 H: 단축키 버전 주석 (curriculum 데이터)

**예시: `course-site/data/curriculum.json`, `weeks/site-data.json`, `course-site/data/curriculum-notion.json`**
> `"action": "→ Keyframe 삽입 (Blender 4.1+)"`

판단: 단축키 `K`가 4.1부터 변경된 것을 주석으로 표시. 5.0에서도 유효하며, 구버전 튜토리얼 혼동 방지. 유지.

---

## 3. 감사 범위 외 항목 (기록용)

**`claudedocs/research/mirror-modifier-brief.md` (line 2, 78)**
> `> 생성일: 2026-03-17 | Blender 4.3+ 기준`  
> `| ... | Blender 4.3 기본값 확인 | ...`

감사 범위(`syllabus.md`, `course-site/`, `docs/*.md`, `weeks/`, `Blender_2026/`)에 포함되지 않는 `claudedocs/research/` 하위 파일. 날짜 명시된 연구 아카이브이므로 버전 표기는 당시 기준. 범위 외로 처리.

---

## 4. 검색 커버리지 요약

검색 키워드: `Blender [23456789]\.[0-9]`, `4\.[0-9]`, `5\.1`, `3\.[0-9]`, `2\.[0-9]`  
검색 범위: syllabus.md, course-site/ (HTML, JSON, JS), docs/*.md, weeks/ (MD), Blender_2026/ (py, txt)  
총 비-5.0 버전 언급 위치: 약 60여 건  
분류 결과: stray 1건, 의도적 유지 다수
