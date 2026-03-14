# FriendsPick Deep Analyze & Improvement Plan

작성일: 2026-03-05  
대상 코드베이스: `/Users/ssongji/Developer/Workspace/thegoodfriends/frontend/v0-friendspick`

---

## 0. Executive Summary

- 현재 제품은 기능 커버리지와 UX 완성도가 높고, 배포 안정성(`build`, `e2e`)도 확보되어 있습니다.
- 그러나 아키텍처 관점에서 **인증/권한 경계**, **API 식별 모델**, **운영 거버넌스(CI/문서/관측)**가 뒤처져 있습니다.
- 지금 단계에서 가장 중요한 의사결정은 “기능 추가”가 아니라 “플랫폼 안정화”입니다.

핵심 판단:
1. Admin/Auth 경계는 즉시 재설계 필요 (`P0`).
2. `X-User-ID` + client storage 의존 모델은 단계적으로 제거 필요 (`P0`).
3. 문서-코드 드리프트(Analytics/SEO/경로)가 커서 운영 신뢰도 저하 (`P1/P2`).
4. 구조 복잡도가 빠르게 증가 중이므로 도메인 모듈화 없이는 이후 속도 저하 확실 (`P2`).

---

## 1. Scope, Method, Evidence

### 1.1 분석 범위
- UX: 홈/상품상세/장바구니/체크아웃/마이/관리자
- 보안: 인증, 세션, 권한, 브라우저 저장소, 헤더, 민감정보 노출면
- 구조: `app`, `components`, `hooks`, `lib`, `docs`, CI
- 품질: lint/test/typecheck/build/e2e, 테스트 구조 및 게이트
- 운영: 문서 최신성, 분석(analytics), 배포/환경 일관성

### 1.2 실행 근거
- 코드 정적 점검 + 실행 검증
  - `pnpm typecheck` pass
  - `pnpm build` pass
  - `pnpm exec playwright test` pass (13/13)
  - `pnpm lint` fail
  - `pnpm test` fail (1 case)
- 보안/업데이트 점검
  - `pnpm audit --prod`: high 3 / moderate 1
  - `pnpm outdated`: 대규모 minor/major drift

### 1.3 프로젝트 규모 지표
- TS/TSX 총 305 files / 약 53k LOC
  - `app`: 74 files / 22,012 lines
  - `components`: 113 files / 15,535 lines
  - `hooks`: 30 files / 6,382 lines
  - `lib`: 65 files / 5,868 lines
- `fetch(` 호출: 88
- `localStorage|sessionStorage|document.cookie` 접근: 74
- `use*Store` 사용(전역 상태 결합도 지표): 74

---

## 2. Deep Findings

## 2.1 Security & Auth (최우선)

### F-SEC-01 (`P0`) Admin 인증 경계가 클라이언트 저장값에 의존
- 증거:
  - `lib/admin-store.ts:32-39` sessionStorage 토큰 hydrate
  - `lib/admin-store.ts:37,52` JS에서 `document.cookie`로 `staff-token` 설정
  - `proxy.ts:27-33` 쿠키 존재 여부만으로 `/admin/*` 통과
  - `app/admin/layout.tsx:293-295` 클라이언트 state `isAdmin` 기반 렌더 분기
- 리스크:
  - XSS/토큰 유출 시 권한 상승 가능
  - 서버 권한 경계가 약하고 회복 불가 세션 패턴 발생 가능
- 개선 방향:
  - 서버 발급 `httpOnly + Secure + SameSite` admin session으로 전환
  - Edge Proxy는 “쿠키 존재”가 아닌 “서명 검증/세션 조회” 기반으로 통과

### F-SEC-02 (`P0`) 고객 영역 식별이 client-asserted ID에 의존
- 증거:
  - `lib/api/shared.ts:28-30` `getUserIdForApi()`가 local state 기반
  - `lib/auth/session.ts:90-99` user/memberId를 localStorage 파싱
  - `lib/api/orders.ts:131,164,190,239` `X-User-ID` 헤더 전송
  - `lib/api/orders.ts:167,193,242,273` 일부 API는 `credentials: "omit"`
- 리스크:
  - 서버가 JWT 주체 검증을 강제하지 않으면 IDOR 공격 표면
  - 인증 모델이 endpoint마다 달라 취약점 탐지 난이도 증가
- 개선 방향:
  - 서버 단일 신원 소스(세션/JWT claims)로 식별, `X-User-ID` 제거
  - 고객 API `credentials` 정책 일관화 (`include` + 서버 검증)

### F-SEC-03 (`P1`) review-login route 운영 노출
- 증거:
  - `app/api/review-login/route.ts:16-45` 서버 route 존재
  - `app/auth/login/page.tsx:237-245` UI만 env 조건으로 노출 제어
- 리스크:
  - UI 숨김과 무관하게 엔드포인트 호출 가능
- 개선 방향:
  - 서버측 env guard (`if PROD -> 404`), rate limit, IP allowlist

### F-SEC-04 (`P1`) 헤더 정책 미완성
- 증거:
  - `next.config.mjs:83-89` 일부 헤더만 설정
  - `next.config.mjs:86` `X-XSS-Protection` (deprecated)
- 리스크:
  - CSP 미설정으로 script injection 대응 약함
- 개선 방향:
  - CSP, Permissions-Policy, COOP/COEP 필요성 검토 후 도입
  - deprecated 헤더 제거

### F-SEC-05 (`P1`) 새 탭 열기 보안 누락 지점 존재
- 증거:
  - `components/share-button.tsx:102` `window.open(..., "_blank", "width=...")`
  - `components/auth/terms-agreement.tsx:109` `target="_blank"` + `rel` 없음
- 리스크:
  - `window.opener` 관련 tabnabbing 위험
- 개선 방향:
  - `noopener,noreferrer` 강제 유틸 도입

### F-SEC-06 (`P1`) tenant config script 주입 이스케이프 부재
- 증거:
  - `app/layout.tsx:123` `dangerouslySetInnerHTML` with raw `JSON.stringify`
  - 대비 사례: `components/json-ld.tsx`는 `</script` 이스케이프 처리
- 리스크:
  - backend data가 오염되면 script-breakout 가능성
- 개선 방향:
  - `<` 치환 (`replace(/</g, "\\u003c")`) 포함 safe serializer 적용

---

## 2.2 Architecture & Technical Debt

### F-ARC-01 (`P2`) 모놀리식 페이지/훅 집중
- 근거:
  - `app/admin/inventory/page.tsx` 1194 lines
  - `hooks/use-cart-page.ts` 890 lines
  - `app/checkout/page.tsx` 727 lines
- 영향:
  - 변경 충돌 증가, 회귀 확률 증가, 온보딩 난이도 증가
- 개선 방향:
  - `view-model`/`domain service`/`ui section` 단위 분해

### F-ARC-02 (`P2`) API 계층 일관성 부족
- 증거:
  - 공통 wrapper 존재: `lib/admin-fetch.ts`
  - 우회 직접 호출: `lib/api/display-settings.ts`, `lib/api/products/admin.ts`
- 영향:
  - 인증/에러/로깅 정책 분산, 보안 패치 확산 비용 증가
- 개선 방향:
  - `lib/http/client.ts` + `auth policy` + `error contract` 통합

### F-ARC-03 (`P2`) local fallback 전략이 도메인에 침투
- 증거:
  - cart/wishlist/reservations/orders/customer alerts 다수에 `ENABLE_API` 분기
  - `lib/api/customer/reservations.ts:37-39` 네트워크 시 local fallback
  - `lib/stores/gonggu-store.ts` Phase 0 localStorage 전제
- 영향:
  - 데이터 일관성 저하, 환경별 버그 재현 어려움
- 개선 방향:
  - fallback 정책을 인프라 계층으로 격리
  - 기능 플래그 + 환경 정책 문서화

### F-ARC-04 (`P2`) 타입 모델 중복/불일치
- 증거:
  - `lib/types.ts`의 `Order`와 `app/admin/types.ts`의 `Order` 이중 정의
  - snake_case + camelCase 필드 혼용 (`shipping_company` vs `shippingCompany`)
- 영향:
  - 매핑 코드 증가, 타입 안전성 하락
- 개선 방향:
  - canonical DTO + mapper 강제
  - API boundary 타입 패키지화

### F-ARC-05 (`P2`) JSON 파싱 안전성 불균형
- 증거:
  - `lib/api/products/mapper.ts:46` `JSON.parse(apiProduct.detailImages)` try/catch 없음
- 영향:
  - 불량 데이터 입력 시 런타임 크래시 가능
- 개선 방향:
  - `safeParseJson` 유틸 전역 적용

---

## 2.3 UX, Accessibility, Design Ops

### F-UX-01 (`P2`) 정책/토큰 문서는 좋지만 자동검증 부재
- 강점:
  - `app/globals.css`, `docs/BRAND_TOKENS.md` 정교
- 갭:
  - 접근성 자동 검증(axe), contrast regression, keyboard flow CI 없음

### F-UX-02 (`P2`) 테스트가 desktop 중심, 모바일 우선 전략과 불일치
- 증거:
  - `playwright.config.ts:16-18` Desktop Chrome only
- 영향:
  - 모바일 전용 회귀(하단 네비, safe-area, sticky CTA) 탐지 누락

### F-UX-03 (`P3`) 품질 드리프트 신호
- 증거:
  - 실제 UI `품절` vs test 기대 `SOLD OUT`
  - lint unused vars
- 영향:
  - 테스트 신뢰도 저하

---

## 2.4 Analytics, SEO, Observability

### F-DATA-01 (`P1`) 분석 체계 문서-코드 분리
- 증거:
  - 문서: `docs/GA4_CUSTOM_DEFINITIONS_SPEC_2026-02.md` (정교한 스키마)
  - 코드: `components/analytics/index.ts` stub (`return null`)
  - 문서가 참조하는 `lib/analytics-events.ts` 부재
- 영향:
  - KPI 보고 신뢰성 낮음, 실험 불가

### F-DATA-02 (`P2`) 문서 경로와 실제 저장소 불일치
- 증거:
  - 다수 docs에 과거 사용자 절대 경로(`/Users/jeeheesong/...`)
- 영향:
  - 협업/운영 재현성 저하

### F-SEO-01 (`P2`) 메타/자산/라우트 정합성 문제
- 증거:
  - `app/layout.tsx` `og-image.png` 참조, 실제 public에 없음
  - `lib/seo.ts` `logo.png`, `/search` 경로 참조 불일치
  - `app/sitemap.ts`가 slug route 대신 query category URL 생성
- 영향:
  - 검색/공유 품질 하락

---

## 2.5 CI/CD & Quality Governance

### F-CI-01 (`P1`) package manager와 CI 실행 체계 불일치
- 증거:
  - `package.json` `packageManager: pnpm@...`
  - `.github/workflows/ci.yml`는 `npm ci`, `npm run ...`
  - `playwright.config.ts` webServer command도 `npm run dev`
- 영향:
  - lockfile 일관성 저하, CI/로컬 결과 편차 가능

### F-CI-02 (`P2`) CI 게이트에 테스트(E2E/Unit) 미포함
- 증거:
  - CI는 lint/typecheck/build만 실행
- 영향:
  - 회귀가 main 브랜치까지 유입될 가능성 높음

---

## 3. Target Architecture (권장)

## 3.1 목표 상태
1. 인증
- Admin: server session + RBAC + audit log
- Customer: session/JWT subject only (header asserted identity 제거)

2. API
- 단일 HTTP client 계층
- 정책: timeout/retry/error mapping/logging/auth refresh

3. 도메인
- `domain/*` 순수 비즈니스 규칙
- `application/*` use-case orchestration
- `ui/*` view logic + components

4. 관측
- Analytics typed schema + runtime validator
- Core Web Vitals + error budget

---

## 4. Deep Improvement Plan

아래는 실행 우선순위 기준의 Workstream입니다.

## WS-A: Security Hardening

### A1. Admin auth 재설계 (`P0`, 1-2주)
- 작업:
  - JS 저장소 토큰 제거
  - `/admin/session` 발급/검증 API + proxy 강제검증
  - admin action audit log 기본 필드(`who/when/what`) 저장
- 완료 기준:
  - `document.cookie`로 staff-token 설정 코드 제거
  - 인증 우회 시나리오 테스트 추가

### A2. Customer identity 모델 정리 (`P0`, 1-2주)
- 작업:
  - `X-User-ID` 제거
  - server-side principal에서 memberId 결정
  - 고객 API credential 정책 통일
- 완료 기준:
  - `X-User-ID` 전송 0건
  - IDOR 회귀 테스트 추가

### A3. 공개 엔드포인트 방어 (`P1`, 2-3일)
- 작업:
  - review-login production block
  - rate limit + abuse monitoring
- 완료 기준:
  - prod에서 404/403 보장

### A4. Header/CSP 정책 (`P1`, 3-5일)
- 작업:
  - CSP report-only -> enforce 단계 적용
  - `X-XSS-Protection` 제거
- 완료 기준:
  - 보안 스캔 기준 충족

## WS-B: Architecture Refactor

### B1. HTTP client 통합 (`P1`, 1주)
- 작업:
  - `lib/http/client.ts` 신설
  - admin/customer fetch wrapper 통합
  - 에러 규약(`APP_ERROR_CODE`) 표준화
- 완료 기준:
  - 직접 `fetch` 사용량 50% 이상 감소

### B2. 타입 정규화 (`P2`, 1주)
- 작업:
  - `Order` canonical model 단일화
  - snake_case는 boundary mapper에서만 허용
- 완료 기준:
  - `shipping_company`/`shippingCompany` 이중모델 제거

### B3. 대형 모듈 분해 (`P2`, 2-3주)
- 우선 파일:
  - `hooks/use-cart-page.ts`
  - `app/checkout/page.tsx`
  - `app/admin/inventory/page.tsx`
- 완료 기준:
  - 파일당 400 line 이하(권장)
  - 도메인 로직 unit test 확보

### B4. fallback 정책 격리 (`P2`, 1주)
- 작업:
  - `ENABLE_API` 분기 제거/축소
  - offline mode를 adapter 계층으로 이동
- 완료 기준:
  - business code에서 localStorage fallback 직접 호출 70% 감소

## WS-C: Quality & Testing

### C1. 테스트 신뢰성 복구 (`P1`, 2-3일)
- 작업:
  - `product-card` 텍스트 불일치 수정
  - lint 오류/경고 정리
- 완료 기준:
  - `lint/test/typecheck` 100% pass

### C2. CI 일관화 (`P1`, 2-3일)
- 작업:
  - CI를 `pnpm` 기준으로 통일
  - unit/e2e를 PR 게이트에 포함
- 완료 기준:
  - CI에서 `pnpm install --frozen-lockfile`, `pnpm lint`, `pnpm typecheck`, `pnpm test`, `pnpm exec playwright test`

### C3. 모바일 e2e 추가 (`P2`, 3-5일)
- 작업:
  - iPhone/Android viewport 프로젝트 추가
  - 하단네비/체크아웃 sticky 영역 검증
- 완료 기준:
  - 모바일 회귀 케이스 최소 8개

## WS-D: Analytics/SEO/Docs Ops

### D1. Analytics 실구현 (`P1`, 1주)
- 작업:
  - `components/analytics/index.ts` 실제 script/provider 연결
  - typed event registry (`lib/analytics-events.ts`) 신설
  - docs와 이벤트 스키마 동기화
- 완료 기준:
  - DebugView event 수집 확인
  - KPI SQL 재현 가능

### D2. SEO 정합성 (`P2`, 2-3일)
- 작업:
  - 누락 OG/logo asset 보강
  - `/search` route 또는 SEO 템플릿 수정
  - sitemap slug 정책 정리
- 완료 기준:
  - Search Console 주요 오류 0건

### D3. Docs hygiene (`P2`, 2-3일)
- 작업:
  - 절대경로 문서 정리
  - runbook를 저장소 상대경로로 통일
- 완료 기준:
  - 팀원이 로컬 경로 의존 없이 재현 가능

---

## 5. 90-Day Delivery Plan

## Phase 1 (Week 1-2): Stabilize Security & Quality
- WS-A1, A2, A3, C1, C2
- 목표 KPI:
  - high vulnerability 0
  - CI gate all green

## Phase 2 (Week 3-6): Unify Architecture
- WS-B1, B2, B4
- 목표 KPI:
  - `fetch` direct calls 88 -> 40 이하
  - identity 관련 보안 예외 0

## Phase 3 (Week 7-10): Reduce Complexity
- WS-B3, C3
- 목표 KPI:
  - top 3 complex files 분해 완료
  - 모바일 e2e 추가

## Phase 4 (Week 11-13): Data/SEO/Ops Maturity
- WS-D1, D2, D3
- 목표 KPI:
  - analytics fill rate 목표 달성
  - SEO 핵심 에러 0

---

## 6. Backlog (우선순위, 난이도, 효과)

| ID | 작업 | 우선순위 | 난이도 | 효과 |
|---|---|---|---|---|
| BKG-001 | Admin auth server-session 전환 | P0 | High | Very High |
| BKG-002 | `X-User-ID` 제거 및 principal 기반 API | P0 | High | Very High |
| BKG-003 | review-login prod 차단 | P1 | Low | High |
| BKG-004 | lint/test 깨짐 복구 | P1 | Low | High |
| BKG-005 | CI pnpm 통일 + test gate | P1 | Medium | High |
| BKG-006 | HTTP client 통합 | P1 | Medium | High |
| BKG-007 | Order 타입 canonical화 | P2 | Medium | Medium |
| BKG-008 | 대형 모듈 분해(checkout/cart/admin) | P2 | High | High |
| BKG-009 | analytics events registry + script 실구현 | P1 | Medium | High |
| BKG-010 | SEO 자산/route 정합화 | P2 | Low | Medium |

---

## 7. Risk Register

1. 서버팀 API 계약 미정
- 영향: 인증 전환 지연
- 대응: 계약서(OpenAPI) 우선 확정

2. 대형 리팩터링 중 기능 회귀
- 영향: 결제/주문 장애
- 대응: PR 단위 작은 배치 + feature flag rollout

3. analytics 적용 시 개인정보 규정 충돌
- 영향: 법적 리스크
- 대응: 이벤트 payload whitelist, PII 차단 정책

---

## 8. Immediate Next Actions (이번 주)

1. `security hotfix PR`
- admin token 저장 제거, review-login prod 차단, rel noopener 일괄 적용

2. `quality gate PR`
- lint/test 실패 케이스 수정, CI를 pnpm 기준으로 전환

3. `architecture kickoff`
- API client 통합 초안 + Order canonical type RFC 작성

---

## 9. Reference Signals (Code)

- Admin token storage: `lib/admin-store.ts:32-53`
- Proxy cookie check: `proxy.ts:27-33`
- Customer identity header: `lib/api/orders.ts:131,164`
- Tenant config script injection: `app/layout.tsx:123`
- Analytics stub: `components/analytics/index.ts:9-18`
- CI package manager mismatch: `.github/workflows/ci.yml:22-25`
- Playwright npm dev command: `playwright.config.ts:21`
- E2E SKU regex coupling: `e2e/buying_flow.spec.ts:20-23`
- Unsafe `_blank` usage: `components/share-button.tsx:102`, `components/auth/terms-agreement.tsx:109`

