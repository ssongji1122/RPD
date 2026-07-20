# AGENTS.md — RPD (로봇프러덕트 디자인)

> **Single Source of Truth** for all AI agents (Claude, Codex, Gemini, Cursor).
> CLAUDE.md, GEMINI.md, .cursorrules는 이 파일의 symlink.

## Project Overview

인하대학교 디자인테크놀로지학과 **로봇프러덕트 디자인 (DET3012-001)** 2026 Spring 수업 운영 플랫폼.
- **강의**: 화요일 10:00–15:00, 60주년기념관 908호
- **도구**: Blender 5.0, AI 3D 생성 (Meshy/Tripo/Luma Genie), Blender MCP + Claude
- **운영자**: ssongji (강사)

## Stack

- **Course site**: 바닐라 HTML/CSS/JS, GitHub Pages 배포
- **Admin**: Node.js 기반, Playwright 테스트
- **DB**: Supabase (학생 진도/제출물)
- **3D**: Blender 5.0, MCP integration
- **Repo**: github.com/ssongji1122/RPD

## Layout

```
RPD/
├── course-site/      # GitHub Pages 학습 허브 (바닐라 HTML, 현행)
├── web/              # Astro 후속 사이트 (rpd.soluta.studio, course-site 대체 예정)
├── 2026_RPD_01/      # 1학기 운영 자료
├── 2026_RPD_02/      # (예비)
├── Blender_2026/     # Blender 실습 파일
├── weeks/            # 주차별 콘텐츠
├── templates/        # 카드/슬라이드 템플릿
├── supabase/         # DB 스키마, migrations
├── tools/            # 운영 자동화 스크립트
├── tests/            # Playwright e2e
├── DESIGN.md         # 디자인 시스템 (Flat Outline, Mint accent)
└── syllabus.md       # 16주 강의계획
```

## Commands

```bash
# Admin 서버 실행
./start-admin.sh

# Playwright 테스트
npx playwright test

# (course-site는 GitHub Pages 자동 배포)

# Astro 후속 사이트 (web/)
cd web && npm install && npm run dev    # localhost:4321
cd web && npm run build                  # dist/ 생성
# 배포: rpd.soluta.studio, GitHub Actions wiring 필요 (현재 미연결)
```

## Design System

상세: [DESIGN.md](./DESIGN.md)

- **방향**: Flat Outline (2026.04 전환). Linear/Raycast 톤. 콘텐츠가 주인공.
- **금지**: gradient overlay, radial-gradient glow, backdrop-filter blur, inset glow ring, box-shadow halo
- **Accent**: Mint (`--key: #00bfa5`)
- **Surface**: Dark 기본 (`--bg: #0a0a0a`)
- **Font**: Noto Sans KR

## Curriculum (16주 요약)

| 단계 | 주차 | 핵심 |
|------|------|------|
| 기초 | 1–4 | OT, Blender UI, Edit Mode + Modifier, 하드서피스 디테일 |
| 디테일 | 5–7 | AI 3D 생성, Material/Shader, UV + AI Texture |
| 중간 | 8 | 중간 프로젝트 발표 (배점 35%) |
| 고급 | 9–14 | Lighting, Animation, 최종 프로젝트 |
| 마무리 | 15–16 | 발표/평가 |

전체: [syllabus.md](./syllabus.md)

## Conventions

- 학생 제출물: Discord
- 주차별 자료: `weeks/weekNN/` 구조
- 스크린샷/이미지: `output/` (gitignored)
- AI 도구 사용 시 프롬프트 로깅 (재현 가능성)

## Knowledge Pointers

<!-- BEGIN:WIKI -->
_last sync: 2026-07-18_

- [[agents-md-sst]] — AGENTS.md SSoT 전략 (symlink, .cursorrules deprecated) | 2026-05-06
- [[gemini-cli-agents-md]] — Gemini CLI context.fileName 설정 | 2026-05-06
- [[sync-wiki-pipeline]] — Obsidian→AGENTS.md 자동 주입 파이프라인 | 2026-05-06
- [[agent-init-template]] — 프로젝트 멀티 에이전트 초기화 자동화 | 2026-05-06
- [[claude-code-subagent-technical-notes]] — subagent frontmatter·isolated context·dispatch 휴리스틱 | 2026-05-22
- [[claude-hooks-pretooluse-defer-pitfall]] — PreToolUse defer → 데스크톱 앱 인터랙티브 위젯 파괴 원인·진단 경로 | 2026-06-10
- [[claude-subagent-cherry-pick-design-decisions]] — 144개 중 8개 cherry-pick 설계결정 5개 (dotfiles SSoT·Karpathy 인라인·marketing 제외) | 2026-05-22
- [[mcp-initialize-prompt-injection]] — MCP initialize instructions 필드로 CLAUDE.md/AGENTS.md 자동수정 유도하는 인젝션 패턴·대응 원칙 | 2026-06-24
- [[memory-vector-search-not-installed]] — memory-vector-search 플러그인 미설치 실측, AGENTS.md SoT 매트릭스 드리프트 확인 | 2026-07-03
- [[goal-loop-stateless-checkpoint-haiku-doublecheck]] — /goal 루프 haiku 독립판정 + git 체크포인트 롤백(Stateless Loop), 검증불가 목표는 시작 안 함 실전판단 | 2026-07-11
- [[http-status-codes]] — HTTP 상태 코드 레퍼런스 (2xx~5xx, 실무 처리 패턴) | 2026-05-12
- [[ai-knowledge-3tier-pipeline]] — AI 지식 3단(Inbox→Curated→Wiki) 파이프라인 + Tier 권한 | 2026-05-20
- [[agent-orchestration-altitude-model]] — 오케스트레이션=altitude 문제, 지휘자 1개·워커만 교체 | 2026-06-04
- [[claude-code-mcp-3tier]] — Claude Code MCP 3-tier 소스(User-level/Plugin/OAuth) + 진단 체크리스트 | 2026-05-18
- [[gemini-cli-hook-format-040]] — Gemini CLI 0.40.x hook 형식 변경(matcher 래퍼 필수), caveman tool명 충돌 | 2026-06-08
- [[macos-launchd-tcc-python]] — macOS cron→launchd 교체, TCC FDA 바이너리 단위 부여, Homebrew python 권장 | 2026-06-05
- [[notion-external-embed-cache-buster]] — Notion 외부 임베드 404 캐시 → URL 끝 `?v=N` 쿼리로 강제 재요청, CDN 무시 보장 | 2026-06-23
- [[slack-integration-3paths]] — Slack 통합 3경로 구분 (MCP·mac-runner 브리지·앱 리스너) + 혼동 패턴·진단법 | 2026-07-03
- [[github-required-conversation-resolution]] — required_conversation_resolution은 REST 미표시, GraphQL reviewThreads로만 진단 + auto-merge 해법 | 2026-07-12
- [[ai-automation-5mode-policy]] — AI 자동화 5-mode 정책 (₩22,029 사고 후 도입) | 2026-05-11
<!-- END:WIKI -->

## Recent Decisions

<!-- BEGIN:DECISIONS -->
_last sync: 2026-07-18_

- 2026-07-10 — 학생 PII(실명·학번) 공개 repo 노출 → A안 전면 정화 (사용자 결재)
- 2026-07-02 — 기말 갤러리 수복: 링크 kind는 영어 저장 + 렌더러 정규화
- 2026-07-02 — canonical(site-data.json) 직접 수정 예외: Notion이 빈 값인 필드
- 2026-05-19 — Notion ↔ Obsidian 양방향 구조 확정
- 2026-05-19 — 콘텐츠 작성 원칙: 정보 기반만
- 2026-05-18 — wiki DB → 일반 DB 전환
- 2026-05-18 — RPD Notion 구조 정리
- 2026-04-06 — SoT(Source of Truth)는 Notion
- 2026-04-28 — curriculum-push.py 영구 비활성화 + Notion body-mirror 인프라
- 2026-04-06 — 주차별 수업 페이지 공통 구조 표준화
<!-- END:DECISIONS -->

---

## Agent Routing Guide

| 작업 | 1순위 | 비고 |
|------|------|------|
| 코스 사이트 UI/UX | Claude Sonnet | DESIGN.md Flat Outline 준수 |
| Blender 스크립트 (Python) | Claude Opus / Codex | MCP 연동 시 Claude 우선 |
| 슬라이드/카드 콘텐츠 작성 | Claude Sonnet | 한국어 톤 |
| Playwright 테스트 | Codex / Claude | git diff 정확도 |
| Supabase 스키마 설계 | Claude Opus | 장기 추론 |

## Universal Rules

- **언어**: 한국어 존댓말 (호칭: ssonji)
- **TDD**: 테스트 가능한 영역(admin, tools)에서 RED-GREEN-REFACTOR
- **Verification**: 작업 완료 선언 전 Playwright 통과 확인
- **금지**: 디자인 anti-pattern (gradient/glow/blur), 마케팅 문구

## 쉬운 언어 절대규칙 (2026-07-20 결재)

수업자료·학생-facing 카피 전체에 적용한다. 대상 독자는 AI·개발 도구 지식이 전혀 없는, 글을 읽을 줄 아는 대학생과 일반인이다.

- 모든 문장은 그 독자가 설명 없이 바로 읽히는 말로 쓴다. 읽고 되물어야 하는 문장은 다시 쓴다.
- `md`, `json`, MCP, 모디파이어 같은 도구 용어는 **첫 등장에 한 줄 풀이**를 붙인다. 예: "`.md` 파일 — 메모장처럼 글자만 담는 문서 파일입니다."
- 내부 제작 용어는 화면에 그대로 내보내지 않는다. 쉬운 말로 바꾸거나, 불가피하면 첫 등장에 풀이한다.
- "지난 세션·오늘·이번 주" 같은 시점 고정 표현을 수업 콘텐츠에 넣지 않는다. 언제 열어도 읽히게 쓴다.

같은 규칙이 studio.soluta AGENTS.md에도 있다.
