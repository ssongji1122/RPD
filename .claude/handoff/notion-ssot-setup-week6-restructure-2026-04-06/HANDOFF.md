# Handoff: Notion MCP 연결 + Week 6 구조 재정비
> Created: 2026-04-06T00:45+09:00
> Branch: main
> Worktree: main

## 작업 목표
1. **SoT를 Notion으로 확정**하고 주차별 수업 페이지 공통 구조를 표준화
2. **Notion MCP 서버를 Claude Code에 연결**해서 제가 직접 Notion 페이지 읽기·편집 가능하게 만들기
3. **Week 6 Notion 페이지를 4파트 표준 구조로 재구성** (Part 1 Remesh / Part 2 Material divider 포함)

## 완료된 작업
- [x] Week 1~5 `lecture-note.md` 구조(헤더만) 분석 완료 — 주차별 섹션 순서/편차/불일치 도출
- [x] 4파트 표준 구조 제안서 작성 (오리엔테이션 → 이론 → 실습 → 정리 → 학생 리소스)
- [x] `decision_log.md` 신규 생성, SoT=Notion(a안) + 공통 구조 표준 2건 기록
  - 경로: `~/.claude/projects/-Users-ssongji-Developer-Workspace-RPD/memory/decision_log.md`
- [x] `MEMORY.md` 인덱스에 Decisions 섹션 추가
- [x] `~/.claude.json` top-level `mcpServers`에 **Notion MCP 서버 추가**
  - `@notionhq/notion-mcp-server` (npx)
  - 토큰은 `.env`의 `NOTION_TOKEN` 값 사용 (`ntn_227733...`)
  - 백업: `~/.claude.json.bak-20260406-004132`

## 진행 중인 작업
- [ ] **Claude Code 재시작 대기 중** (MCP 서버 활성화 필요)
  - 현재 상태: 설정 파일 업데이트 완료, 아직 이 세션에 반영 안 됨
  - 다음 단계: Claude Code 완전 재시작 → 재시작 후 `mcp__notion__*` 도구 사용 가능 확인

## 남은 작업
- [ ] **Notion integration을 상위 페이지에 Connect**
  - 대상 페이지: "03 주차별 강의자료 원본" (`31d54d6549718101af08ea5812e54677`)
  - 절차: 페이지 우측 상단 `···` → Connections → integration 선택 → Connect
  - 한 번만 하면 하위 Week 페이지 전부 접근 가능
- [ ] **Week 6 Notion 페이지 재구성** (page_id: `31354d654971818c8cb5e7814445e3eb`)
  1. `mcp__notion__notion-fetch`로 현재 블록 구조 읽기
  2. 4파트 표준 구조로 블록 재정렬/추가
  3. 실습 섹션 내부에 **Part 1(Remesh) / Part 2(Material) divider** 명확히 배치
  4. Step 번호는 **연속 번호** (Step 1 Remesh → Step 2~6 Material)
- [ ] (선택) Week 1~5도 같은 4파트 구조로 순차 정비

## 변경된 파일 목록
| 파일 | 변경 유형 | 설명 |
|------|-----------|------|
| `~/.claude.json` | 수정 | top-level mcpServers에 notion 서버 추가 |
| `~/.claude/projects/.../memory/decision_log.md` | 신규 | SoT=Notion + 구조 표준화 결정 기록 |
| `~/.claude/projects/.../memory/MEMORY.md` | 수정 | Decisions 섹션 인덱스 추가 |

*(RPD repo 자체에는 변경 없음 — `course-site/assets/layout.css`의 기존 수정은 이 세션과 무관)*

## 핵심 결정사항

### 1. SoT = Notion (a안 채택)
- **Notion이 원본, repo는 출력물**
- 대안: (b) repo=원본, (c) 병행 → 모두 기각
- 이유: 학생 접근성, 실시간 편집, 시각성
- 중장기 리스크: 동기화 파이프라인 관리 필요 (이미 `tools/notion-sync.py` · `curriculum-notion.json` 존재)
- 점검 시점: Week 8쯤

### 2. 주차별 공통 구조 (4파트)
```
Part 0 오리엔테이션: 이전 주차 복습 → 수업 시작 체크리스트 → 학습 목표
Part 1 이론 (XX분)
Part 2 실습 (XX분) — Step 1..N
Part 3 정리: 흔한 실수 → 핵심 정리 → 과제
Part 4 학생 리소스: 단축키 → 자주 막히는 지점 → 공식 영상/문서 → 참고자료 → 프로젝트 체크리스트
```
- "정리 → 과제" 순서 (W5/W6 방식)
- 프로젝트 체크리스트는 **맨 아래** 고정
- Step 번호 **연속 번호** (Part 구분 있어도)

### 3. 구조 분석 결과
- W1~W6 섹션 헤더만 뽑아 비교표 작성
- 주요 불일치: 과제/핵심정리 순서 (W3/W4 vs W5/W6), 체크리스트 위치, "이전 주차 복습" 도입 시점 (W3~)
- W2만 이질적 (레퍼런스 성격, 목차+영상구성 섹션)

## 주의사항

### 재시작 시
- Claude Code를 완전히 종료 후 재실행 필요 (MCP 서버 로드)
- 재시작 후 `mcp__notion__notion-fetch` 등의 도구가 뜨는지 확인

### 토큰 보안
- `.env`의 `NOTION_TOKEN`이 `~/.claude.json`에 평문으로 복사됨 (Authorization 헤더)
- 토큰 변경 시 `~/.claude.json`도 같이 업데이트 필요
- 백업 파일(`.claude.json.bak-20260406-004132`)은 정상 동작 확인 후 삭제 권장

### Notion 작업 시 주의
- `weeks/*/lecture-note.md`는 **이제 출력물** — 직접 편집 지양
- 콘텐츠 수정은 Notion → `tools/notion-sync.py --fetch-only` 재생성 흐름
- 기존 `.claude/commands/curriculum.md` 및 `2026-03-31-notion-ssot-implementation.md` 플랜 참조

### Week 6 재구성 시 유지할 것 (사용자 복원분)
- 사용자가 Week 5 lecture-note.md와 Week 6 lecture-note.md를 이전 버전으로 복원했음
- **내용은 절대 건드리지 않음** — 구조/순서만 재정렬
- Week 6은 이미 "Part 1 Remesh / Part 2 Material" 명시되어 있음 (L8-9)

## 주차 페이지 ID 참조 (tools/notion-mapping.json)
- Parent: `31d54d6549718101af08ea5812e54677` (03 주차별 강의자료 원본)
- Week 1: `31354d654971812e9f48f392f2de551b`
- Week 2: `31354d6549718179a709cabf829a5971`
- Week 3: `31354d6549718193a446f3b9d02fb790`
- Week 4: `31354d65497181918ca1edc92c8f505b`
- Week 5: `31354d654971811e85feed7681421e37`
- **Week 6: `31354d654971818c8cb5e7814445e3eb`** ← 다음 작업 대상

## 재개 명령
```bash
# 새 세션에서 이 명령으로 시작
/handoff open notion-ssot-setup-week6-restructure-2026-04-06
```

재개 시 첫 질문: **"Notion MCP 연결됐고 integration도 Connect 했어. Week 6 재구성 시작해줘"**
