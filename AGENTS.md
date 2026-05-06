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
├── course-site/      # GitHub Pages 학습 허브
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
_last sync: 2026-05-06_

- codex
<!-- END:WIKI -->

## Recent Decisions

<!-- BEGIN:DECISIONS -->
_last sync: 2026-05-06_

| 2026-03-23 | Fraser 패턴을 workspace 레벨에 적용 | 프로젝트별 분리보다 cross-project 맥락 유지가 더 가치 있음. Fraser의 회사 단위 = 우리 workspace 단위 | 전체 |
| 2026-03-23 | Notion 유지 (학생 대면), memory 시스템 강화 (운영) | Notion에 이미 수업 구조 구축됨. 학생 접근성 때문에 이전 비용 > 이익 | RPD |
| 2026-03-23 | Obsidian vault 도입 (사람용) + memory/ 유지 (기계용) | ssonji가 직접 memory/ 파일을 편집하지 않음. Claude가 관리하는 memory/와 ssonji가 탐색하는 vault를 분리 | 전체 |
| 2026-03-09 | 자료방 구버전을 교수자 페이지 하위로 이동 | 삭제 대신 보존. 학생 메인에서는 제거하되 참조 가능하게 | RPD |
| 2026-03-27 | AI News Scout 에이전트 도입 | Claude Code 생태계 변화를 빠르게 캐치하여 프로젝트에 즉시 적용. Python cron 대신 기존 MCP 인프라(scheduled-tasks) 활용이 효율적. 출력: claudedocs+Obsidian+Notion 3곳 동기화. 적용 방식: 분석+가이드+PR까지 자동→ssonji 승인 후 적용 | 전체 |
| 2026-04-12 | Advisor 패턴 도입 (모델 비용 최적화) | Anthropic Advisor Tool(2026-04-09 공개) 개념을 Claude Code + Paperclip에 적용. Sonnet을 기본 Executor로, Opus를 플래닝/리뷰 전용으로 배정. SWE-bench 기준 72.1→74.8% 성능 향상 + 비용 절감. CLAUDE.md에 모델 선택 가이드 추가 완료. | 전체 |
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
