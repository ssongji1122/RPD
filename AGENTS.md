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
_last sync: 2026-06-27_

- [[agents-md-sst]] — AGENTS.md SSoT 전략 (symlink, .cursorrules deprecated) | 2026-05-06
- [[gemini-cli-agents-md]] — Gemini CLI context.fileName 설정 | 2026-05-06
- [[sync-wiki-pipeline]] — Obsidian→AGENTS.md 자동 주입 파이프라인 | 2026-05-06
- [[agent-init-template]] — 프로젝트 멀티 에이전트 초기화 자동화 | 2026-05-06
- [[claude-code-subagent-technical-notes]] — subagent frontmatter·isolated context·dispatch 휴리스틱 | 2026-05-22
- [[claude-hooks-pretooluse-defer-pitfall]] — PreToolUse defer → 데스크톱 앱 인터랙티브 위젯 파괴 원인·진단 경로 | 2026-06-10
- [[claude-subagent-cherry-pick-design-decisions]] — 144개 중 8개 cherry-pick 설계결정 5개 (dotfiles SSoT·Karpathy 인라인·marketing 제외) | 2026-05-22
- [[mcp-initialize-prompt-injection]] — MCP initialize instructions 필드로 CLAUDE.md/AGENTS.md 자동수정 유도하는 인젝션 패턴·대응 원칙 | 2026-06-24
- [[http-status-codes]] — HTTP 상태 코드 레퍼런스 (2xx~5xx, 실무 처리 패턴) | 2026-05-12
- [[ai-knowledge-3tier-pipeline]] — AI 지식 3단(Inbox→Curated→Wiki) 파이프라인 + Tier 권한 | 2026-05-20
- [[agent-orchestration-altitude-model]] — 오케스트레이션=altitude 문제, 지휘자 1개·워커만 교체 | 2026-06-04
- [[claude-code-mcp-3tier]] — Claude Code MCP 3-tier 소스(User-level/Plugin/OAuth) + 진단 체크리스트 | 2026-05-18
- [[gemini-cli-hook-format-040]] — Gemini CLI 0.40.x hook 형식 변경(matcher 래퍼 필수), caveman tool명 충돌 | 2026-06-08
- [[macos-launchd-tcc-python]] — macOS cron→launchd 교체, TCC FDA 바이너리 단위 부여, Homebrew python 권장 | 2026-06-05
- [[notion-external-embed-cache-buster]] — Notion 외부 임베드 404 캐시 → URL 끝 `?v=N` 쿼리로 강제 재요청, CDN 무시 보장 | 2026-06-23
- [[ai-automation-5mode-policy]] — AI 자동화 5-mode 정책 (₩22,029 사고 후 도입) | 2026-05-11
- [[gstack-ship-workflow-notes]] — /ship 워크플로우 운영 노트 (pre-commit hook, 장기 브랜치) | 2026-05-11
- [[karpathy-llm-wiki-pattern]] — Karpathy LLM Wiki 패턴 + 1인 사업가 필터 (5도메인 재설계 출처) | 2026-05-13
- [[claude-cli-subprocess-pattern]] — Claude CLI spawn: non-zero exit → resolve(502) 처리 + --max-budget-usd 1.00 필수, fan-out 저장 실패 fail-fast | 2026-06-24
- [[claude-code-remote-control-401]] — Remote Control 401(구독 정상) = scope 누락·stale credentials, /logout→/login 자동 콜백 해소 | 2026-06-05
<!-- END:WIKI -->

## Recent Decisions

<!-- BEGIN:DECISIONS -->
_last sync: 2026-06-27_

| 2026-05-20 | AGENTS.md 표준 골격 11-section 확정 + agent-init 본문 풍부화 | ~/.dotfiles/agent-template/AGENTS.base.md를 빈 placeholder에서 11-section 골격으로 재작성 (Project Overview, Stack, Dev Servers, Commands, Quality Gates, Protected Files, Conventions, Design System, Karpathy 4원칙, Knowledge Pointers, Recent Decisions). 신규 프로젝트가 /agent-init 한 방으로 thegoodfriends 수준 골격 확보. 기존 4개 프로젝트는 audit 후 실제 갭만 보완 (scrave 골격 추가, studio.soluta Quality Gates). | 전체 |
| 2026-05-20 | busywork 회피 원칙 확립 — 표준화 ≠ 동질화 | audit 결과(grep substring 매트릭스)를 무비판 실행 계획으로 전환 금지. thegoodfriends(404줄) 처럼 이미 풍부한 AGENTS.md는 명칭이 표준과 달라도 정보가 더 풍부하면 그대로 유지. Karpathy 외과적 변경 원칙과 일치. 다음 표준화 작업 시 "실제로 빈 곳만 채움" 가이드. | 전체 |
| 2026-05-20 | friendspick/ rpd-web/ 외부 폴더 정리 — 단일 SoT | friendspick(브랜드명, 빈 폴더) → thegoodfriends(법인명, 실코드)로 흡수. rpd-web(scaffold만, no remote)→ RPD/web/ 흡수. studio.soluta workspace에 떠있던 외딴 디렉토리 제거. 단일 git repo SSoT 유지. | thegoodfriends, RPD |
| 2026-06-05 | Obsidian weekly_retro cron → launchd LaunchAgent 마이그레이션 | cron이 `/usr/bin/python3`(Xcode 3.9.6) 사용 → 이 바이너리는 ~/Documents(TCC 보호 폴더) 읽기 Full Disk Access 없음 → EPERM, 2026-05-24 이후 무동작. **근본원인: macOS TCC는 FDA를 바이너리 단위로 부여.** 실증: launchd 컨텍스트에서 Xcode python=READ_FAIL, Homebrew `/opt/homebrew/bin/python3.14`=READ_OK+WRITE_OK (이미 FDA 보유). 해결: LaunchAgent `com.ssongji.obsidian-weekly-retro`(일 21:00, Homebrew python 직접 실행) 설치, cron 라인 주석처리(`[MIGRATED]`). GUI FDA 부여 단계 불필요. 로그는 ~/Library/Logs/(Documents 밖, launchd가 로그파일 못여는 문제 회피). 취약점: `brew upgrade python@3.14` 시 FDA grant 리셋되면 재발 → stderr 로그로 진단·재부여. cron 대신 launchd 선택 이유: cron은 비-Aqua 세션이라 TCC 더 불안정 + 사용자 15개 LaunchAgent 관례. 백업: ~/.claude/backups/crontab-2026-06-05-pre-retro-migration.bak | 전체 |
| 2026-06-06 | Slack #mac-runner → Paperclip 강한 Coder 풀자동 실행 (automation-safety "무인 자율 코드실행 루프 금지"의 **사용자 명시 승인 예외 EX-2**) | macrunner(Paperclip 우회 자체 executor) 은퇴 후 통합. 사용자 명시("풀자동 켜줘"). 안전봉투: (1)사람이 매 오더 트리거(자가생성·cron 아님) (2)Paperclip 거버넌스—Protected Files 가드→위반 시 [막힘] (3)worktree 격리, main push/배포 0(실증) (4)자동 머지 없음—브랜치 사람 리뷰 (5)구독 비용 per-use 0 (6)kill-switch: 래퍼 --auto-dispatch 제거→게이트. 구성: slack_bridge.py(ingress/egress, ts 6자리 버그fix·reply_broadcast) + paperclip_inbox_daemon.py(--board mac-runner --mirror --auto-dispatch). 상세: reference_ai_automation_policy.md EX-2. | 전체 |
| 2026-06-10 | AI 컨설팅 키트: 글로벌 스킬(aeo-audit) + 로컬 consulting repo 분리, A 트랙(회사 진단) 우선·B 트랙(개인 세팅) 차기 | 컨설팅 요청 증가(작은 회사·1인 브랜드·직장인 개인) 대응. 로직(스킬)과 산출물(repo) 분리 — 스킬은 어디서든 호출, 클라이언트 납품물은 git 이력. consulting repo는 클라이언트 데이터 때문에 로컬 전용. rubric 분기 재검증 규율. friendspick=검증 사례 1호. 스킬은 writing-skills TDD(baseline→스킬→재검증)로 제작 — baseline이 정답지에 없던 신규 이슈(sitemap 커버리지·search 404·categories CSR·오프사이트 0)까지 발견해 rubric에 역흡수 | consulting, thegoodfriends |
| 2026-06-10 | Slack Bot Token을 macOS Keychain + wrapper 구조로 분리 | gitleaks가 settings.json 평문 토큰 커밋을 차단(첫 유출 방지, 히스토리에 비밀 세그먼트 0건·잘린 prefix만 존재해 rewrite 불요). 토큰 값은 Keychain `friendspick-slack-bot-token`에만, MCP는 `~/.claude/scripts/slack-mcp-wrapper.sh`가 실행 시 주입. 등록 위치는 user scope `~/.claude.json`(settings.json mcpServers는 Claude Code가 로드 안 함 — claude mcp list 부재로 실증). 구 토큰은 invalid_auth 확인(이미 rotate 완료), transcript 잔존 평문은 무효 토큰이라 위험 0. 토큰 갱신: `security add-generic-password -U -a ssongji -s friendspick-slack-bot-token -w`. 커밋 2b570a4 | 전체 |
| 2026-06-10 | Hermes VM 모델 체인 복구 — primary kimi-k2.6:free → nemotron-3-super-120b-a12b:free, fallback에 key_env 주입 | 06-08부터 hermes chat 전멸. 근본원인 2중: (1) kimi-k2.6:free upstream(Crucible) 429 지속 (2) hermes credential pool이 429를 credential 단위 exhausted(1h cooldown)로 기록 → fallback resolver `_try_openrouter`가 pool 분기에서 entry 없음 → "provider not configured"로 체인 전체 사망 (env 키 fallthrough는 pool 존재 시 도달 불가). 해법: fallback entry에 `key_env: OPENROUTER_API_KEY` → explicit key 경로로 pool 우회. primary는 ultra(550b) 먼저 시도했으나 38K 시스템 컨텍스트 prefill + 무료 티어 큐로 cron 잡 subprocess timeout 120s를 자주 초과 → super(120b-a12b, ping 23s)로 확정. auto-fallback-free 주간 cron이 못 막은 이유: model.default를 안 건드림 + 카탈로그 가격(=0)만으로 live 판정(429 모델 못 거름) → 실호출 probe 추가. 백업: config.yaml.bak-fallbackfix-20260610-040853 | 전체 |
| 2026-06-16 | Agent hook 겹침(load ~15) 문서화 + push 세션 Stop hook opt-out | Cursor agent가 git push(pre-push: vitest+build) + Stop hook(make check-all) + PostToolUse clasp push를 동시 실행 → load average 15+. Stop hook lock은 pre-push와 비공유. 완화: push·배포 세션 전 `FP_STOP_HOOK_CHECK_ALL=0`, check-all과 push 중복 금지, GAS 연속 Edit·push 겹침 금지. 문서: docs/agents/10-dev-environment.md § Hook 겹침, 70-gas-rules.md § PostToolUse clasp, knowledge/check-all-and-gas-contract-tests.md | thegoodfriends |
| 2026-06-21 | thegoodfriends main 브랜치 보호 정합 — 옵션 C(튜닝된 강화) | 거버넌스 갭 점검 결과 `branch-protection.md`가 명시한 8개 보호항목이 GitHub에 **0개** 적용돼 있었음(classic protection 404, rulesets·effective rules `[]`, 권한 ADMIN이라 부재 확정). CODEOWNERS는 라우팅만·필수리뷰 미강제 → #512/#835 무리뷰 머지(reviewDecision="" 실측). path-filter로 backend/frontend/security skip → 워크플로/문서 PR "hollow green". 적용: **Phase 1(즉시)** PR필수+1approval+code-owner리뷰+dismiss stale+conversation resolution+force-push/deletion차단+`enforce_admins=false`(솔로 self-approval 데드락 회피 break-glass — GitHub은 작성자 self-approval 미인정). **Phase 2(PR #836 머지 후)** ci.yml에 항상 실행 `CI Gate` 잡(backend/frontend/security가 success\|skipped면 통과, fail/cancel이면 차단) 추가 → required status check는 이 잡 하나만 등록(hollow green을 정직한 green으로). PR #836에서 CI Gate=pass 실측. 잔여 갭: protected-files.yml PROTECTED_PATTERNS에 `.github/` 누락(워크플로/CODEOWNERS 변경 미감지). 루프 charter(auto-merge OFF·사람리뷰)와 정렬되어 루프 안 깨짐. 롤백: `gh api -X DELETE .../branches/main/protection` | thegoodfriends |
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
