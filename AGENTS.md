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
_last sync: 2026-05-20_

- [[agents-md-sst]] — AGENTS.md SSoT 전략 (symlink, .cursorrules deprecated) | 2026-05-06
- [[gemini-cli-agents-md]] — Gemini CLI context.fileName 설정 | 2026-05-06
- [[sync-wiki-pipeline]] — Obsidian→AGENTS.md 자동 주입 파이프라인 | 2026-05-06
- [[agent-init-template]] — 프로젝트 멀티 에이전트 초기화 자동화 | 2026-05-06
- [[http-status-codes]] — HTTP 상태 코드 레퍼런스 (2xx~5xx, 실무 처리 패턴) | 2026-05-12
- [[ai-automation-5mode-policy]] — AI 자동화 5-mode 정책 (₩22,029 사고 후 도입) | 2026-05-11
- [[gstack-ship-workflow-notes]] — /ship 워크플로우 운영 노트 (pre-commit hook, 장기 브랜치) | 2026-05-11
- [[karpathy-llm-wiki-pattern]] — Karpathy LLM Wiki 패턴 + 1인 사업가 필터 (5도메인 재설계 출처) | 2026-05-13
- [[2026-W20-lint-report]] — 2026-05-11 W20 리포트 (격차 6개, draft 4개)
- [[creative-engine-score-gate]] — Creative Engine P4-P6 점수 게이트 아키텍처·버그 이력 | 2026-05-11
- [[vitest-fork-pool-pitfall]] — vitest pool:forks + jest-dom 초기화 pitfall (`frontend/v0-friendspick`) | 2026-05-11
- [[prompt-upgrade-8-techniques]] — AI 프롬프트 8기법 + 만능 템플릿 (CGAFC 5요소, 8개 복사 가능 템플릿) | M2 | 2026-05-13
- 2026-05-13: **도메인 재설계** — Karpathy LLM Wiki 패턴 + ssonji 1인 사업가 필터. wiki/concepts + wiki/tools → wiki/00_meta로 흡수. 5개 도메인 분할 + 도메인별 `_schema.md` 작성. SCHEMA.md에 도메인 라우팅 트리 추가. wiki-promote.sh 도메인 인식.
- 2026-05-12: wiki/concepts/http-status-codes 추가
- 2026-05-11: W20 lint 리포트, concepts/tools 4개 ingest
- 2026-05-06: vault bootstrap (SCHEMA.md, _index.md, log.md, tools 4개)
<!-- END:WIKI -->

## Recent Decisions

<!-- BEGIN:DECISIONS -->
_last sync: 2026-05-20_

| 2026-03-23 | Obsidian vault 도입 (사람용) + memory/ 유지 (기계용) | ssonji가 직접 memory/ 파일을 편집하지 않음. Claude가 관리하는 memory/와 ssonji가 탐색하는 vault를 분리 | 전체 |
| 2026-03-09 | 자료방 구버전을 교수자 페이지 하위로 이동 | 삭제 대신 보존. 학생 메인에서는 제거하되 참조 가능하게 | RPD |
| 2026-03-27 | AI News Scout 에이전트 도입 | Claude Code 생태계 변화를 빠르게 캐치하여 프로젝트에 즉시 적용. Python cron 대신 기존 MCP 인프라(scheduled-tasks) 활용이 효율적. 출력: claudedocs+Obsidian+Notion 3곳 동기화. 적용 방식: 분석+가이드+PR까지 자동→ssonji 승인 후 적용 | 전체 |
| 2026-04-12 | Advisor 패턴 도입 (모델 비용 최적화) | Anthropic Advisor Tool(2026-04-09 공개) 개념을 Claude Code + Paperclip에 적용. Sonnet을 기본 Executor로, Opus를 플래닝/리뷰 전용으로 배정. SWE-bench 기준 72.1→74.8% 성능 향상 + 비용 절감. CLAUDE.md에 모델 선택 가이드 추가 완료. | 전체 |
| 2026-05-06 | AGENTS.md SSoT + CLAUDE.md symlink 전략 채택 | 멀티 에이전트(Claude/Codex/Gemini/Cursor) 혼용 시 컨텍스트 drift 방지. 공식 문서 크로스체크: .cursorrules deprecated, Gemini CLI는 settings.json 필요, Claude Code는 CLAUDE.md 우선. | 전체 |
| 2026-05-06 | sync-wiki.sh SessionEnd hook 자동 실행 | 세션 종료 시 Obsidian wiki → AGENTS.md 자동 갱신. 복리학습 파이프라인 완성. | 전체 |
| 2026-05-06 | agent-init 템플릿 ~/.dotfiles/agent-template/ 구축 | 신규 프로젝트마다 수동 설정 비용 제거. /agent-init 슬래시 커맨드로 접근. thegoodfriends의 3-way drift는 CLAUDE.md→AGENTS.md 승격 + AGENTS.paperclip.md 분리로 해결. | 전체 |
| 2026-05-10 | AI 자동화/수동 작업 5-mode 분리 정책 확정 | ₩22,029 Gemini 사고 후 안전장치. agent-council(Codex+Gemini) 검토로 모델 이름 중심에서 권한·실행방식 축으로 재정의. ops-safe / ops-summary / manual-review / protected-review / code-exec 5단계. 무인 자동화 외부 AI fallback 금지(break-glass 포함), protected에 무료 라우터 금지. 정책 본문: reference_ai_automation_policy.md. CLAUDE.md "유료 API 사전 확인" 섹션에 요약 통합. | 전체 |
| 2026-05-10 | crontab Paperclip heartbeat (매시간) + reset-errors (매 30분) 제거 | 5-mode 정책 적용. heartbeat는 `--source timer --trigger system`으로 무인 Coder agent invoke = 외부 Gemini API 호출 패턴 (사고 재현). reset-errors는 스크립트 파일 부재로 dead cron. 백업: ~/.claude/backups/crontab-2026-05-10-pre-policy.bak | 전체 |
| 2026-05-10 | Hermes RPD 보고 cron job — Gemini free 현재 유지 (정책 예외) | 비용 0, Notion read-only, 주 1회, production 수정 없음, cron_mode:deny 적용으로 8개 hard rules 충족. SOUL.md 예외 목록에 명시. | 전체 |
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
