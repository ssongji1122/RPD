# Handoff: CSS 아키텍처 리팩터 + 덱 기반 리디자인
> Created: 2026-03-19T23:00:00+09:00
> Branch: claude/mystifying-perlman
> Worktree: mystifying-perlman

## 작업 목표
RPD 수업 사이트의 인라인 CSS를 외부 파일로 분리하고, 디자인 토큰을 확장하여 일관성을 높인다. 이후 사이트를 덱 기반 모듈형 학습 플랫폼으로 재구성한다.

## 완료된 작업
- [x] tokens.css에 font-weight 토큰 추가 (--fw-normal/medium/semi/bold)
- [x] tokens.css에 border-radius 토큰 확장 (--radius-xl/2xl/pill)
- [x] tokens.css에 글래스 효과 테마 인식 토큰 추가 (dark+light 모두)
- [x] components.css 생성 — 공유 컴포넌트 (glass-panel, glass-card, filter-chip, search-input 등)
- [x] 전 HTML 페이지에 components.css 연결
- [x] shortcuts.html 인라인 CSS → page-shortcuts.css 분리 + 토큰 적용
- [x] index.html 인라인 CSS → page-index.css 분리 + 토큰 적용
- [x] 프로토타입 완성 (prototype.html) — 레일, 카드 대시보드, 덱 뷰, 단축키 뷰
- [x] 디자인 시스템 + 디렉터 에이전트 설계 문서 작성

## 진행 중인 작업
- [ ] DESIGN_SYSTEM.md 실제 파일 생성
  - 현재 상태: 설계 문서(docs/plans/2026-03-19-design-system-director-design.md)에 내용 확정됨
  - 다음 단계: docs/DESIGN_SYSTEM.md 파일로 작성
- [ ] design-agent.md 커맨드 업그레이드
  - 현재 상태: 설계 완료 (pre-check, post-verify, system-check 모드 추가)
  - 다음 단계: .claude/commands/design-agent.md 파일 수정

## 남은 작업
- [ ] tokens.css를 디자인 시스템 스케일에 맞게 정리 (스페이싱 4/8/12/16/24/32/48, radius 통일, fw 통일)
- [ ] library.html 인라인 CSS → page-library.css 마이그레이션
- [ ] week.html → deck.html 리네임 + 덱 시스템 구현
- [ ] FOUC 방지 스크립트 통일 (library, shortcuts)
- [ ] 접근성 보강 (skip-link, aria 레이블, focus-visible)
- [ ] 전체 시각 회귀 검증
- [ ] 프로토타입 → 실제 페이지 구현 (별도 구현 플랜 필요)
- [ ] Supabase + Google OAuth 연동 (향후)

## 변경된 파일 목록
| 파일 | 변경 유형 | 설명 |
|------|-----------|------|
| course-site/assets/tokens.css | 수정 | fw/radius/glass 토큰 35줄 추가 |
| course-site/assets/components.css | 신규 | 공유 컴포넌트 CSS 171줄 |
| course-site/assets/page-shortcuts.css | 신규 | shortcuts 인라인 CSS 분리 274줄 |
| course-site/assets/page-index.css | 신규 | index 인라인 CSS 분리 648줄 |
| course-site/shortcuts.html | 수정 | style 블록 제거 + CSS link 추가 + rpd 클래스 적용 |
| course-site/index.html | 수정 | style 블록 제거 + CSS link 추가 + rpd 클래스 적용 |
| course-site/library.html | 수정 | components.css link 추가 |
| course-site/week.html | 수정 | components.css link 추가 |
| course-site/admin.html | 수정 | components.css link 추가 |
| course-site/prototype.html | 신규 | 리디자인 프로토타입 1251줄 |
| docs/plans/2026-03-19-css-architecture-refactor.md | 신규 | CSS 리팩터 구현 플랜 (12 tasks) |
| docs/plans/2026-03-19-design-system-director-design.md | 신규 | 디자인 시스템 + 디렉터 설계 문서 |

## 핵심 결정사항
- **덱 시스템**: Show Me 카드를 조합해 "덱"으로 저장. localStorage + URL 공유. 15주 커리큘럼 = 프리셋 덱
- **week.html → deck.html**: 범용 덱 뷰어로 리네임. 아무 덱이든 열 수 있음
- **카드 디자인**: 기본 상태 = 아이콘 + 제목만 (1행). 설명은 hover/모달로
- **덱별 키컬러**: 6색 (blue/green/purple/amber/rose/cyan). dot/아이콘에만 사용
- **사이드 레일**: 56px 접힘 / 220px 펼침. 모바일 → 하단 탭바
- **디자인 디렉터**: 수정 전(pre-check) + 수정 후(post-verify) 전체 밸런스 검증
- **DESIGN_SYSTEM.md가 source of truth**: 스페이싱 8단계, radius 6단계, fw 4단계만 허용
- **admin.html**: 퍼블릭과 동일 디자인 + 편집 오버레이
- **인증**: Google OAuth + Supabase (향후)

## 주의사항
- CSS 마이그레이션(Task 8-12)은 아직 미완 — library.html, week.html의 인라인 CSS가 아직 남아있음
- prototype.html은 실제 페이지가 아닌 디자인 프로토타입 — 프로덕션 코드 아님
- 기존 CSS 마이그레이션 플랜(2026-03-19-css-architecture-refactor.md)의 Task 8-12는 디자인 시스템 확정 후 재작성 필요
- font-weight 650→700 변환은 미세한 시각 변화 있음 (의도된 통일)
- 스페이싱 스케일을 4/8/12/16/24/32/48로 통일하면 기존 10px, 14px, 18px 등의 값이 바뀜 — 전체 페이지 영향

## 재개 명령
```bash
# 새 세션에서 이 명령으로 시작
cat .claude/handoff/HANDOFF.md
```
