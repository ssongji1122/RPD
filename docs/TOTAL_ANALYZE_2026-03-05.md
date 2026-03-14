# FriendsPick Total Analyze Report

작성일: 2026-03-05  
대상: `/Users/ssongji/Developer/Workspace/thegoodfriends/frontend/v0-friendspick`  
분석 범위: 디자인, UI/UX, 보안, 기술부채, 구조, 품질, 운영성

## 1. 결론 요약
- 제품 완성도는 높고(실서비스 가능한 수준), 모바일 중심 UX 방향성도 명확함.
- 다만 인증/권한 경계(특히 관리자), API 식별 모델, 운영 거버넌스에서 리스크가 큼.
- 현 시점 최우선은 기능 확장보다 보안 경계 정리와 품질 게이트 강화.

## 2. 검증 실행 결과
- `pnpm typecheck`: 통과
- `pnpm build`: 통과 (Next.js 16.1.6)
- `pnpm exec playwright test`: 13/13 통과
- `pnpm lint`: 실패 (3 errors, 6 warnings)
- `pnpm test`: 실패 (256개 중 1개 실패)
- 코드 규모: TS/TSX 305 files, 약 53k LOC
  - `app`: 74 files / 22,012 lines
  - `components`: 113 files / 15,535 lines
  - `hooks`: 30 files / 6,382 lines
  - `lib`: 65 files / 5,868 lines

## 3. 핵심 리스크 (우선순위)

### P0
1. 관리자 인증 경계가 클라이언트 저장소 + JS 쿠키에 의존
   - `lib/admin-store.ts`, `proxy.ts`, `app/admin/layout.tsx`
   - `sessionStorage` 토큰을 쿠키로 주입하고, 프록시는 쿠키 존재만 확인
2. 사용자 식별 헤더(`X-User-ID`)와 클라이언트 저장값 기반 식별 흐름
   - `lib/api/shared.ts`, `lib/auth/session.ts`, `lib/api/orders.ts`
   - 서버측 JWT 주체 검증이 약하면 IDOR 가능성

### P1
1. 리뷰 테스트 로그인 API 라우트가 서버에 상시 존재
   - `app/api/review-login/route.ts`
2. 보안 헤더 세트 불충분
   - `next.config.mjs`
   - `X-XSS-Protection`(deprecated) 사용, CSP/Permissions-Policy 부재
3. 의존성 보안 부채
   - `pnpm audit --prod` 결과: high 3, moderate 1
   - 경로: `@eslint/eslintrc@3.3.3 -> minimatch@3.1.2`, `ajv@6.12.6`

### P2
1. 대형 페이지/훅 집중으로 구조 복잡도 증가
   - 예: `app/admin/inventory/page.tsx`(1194 lines), `hooks/use-cart-page.ts`(890 lines)
2. 문서-코드 불일치(Analytics)
   - `components/analytics/index.ts`가 stub (`return null`)
   - 문서가 참조하는 `lib/analytics-events.ts` 파일 부재
3. SEO 자산/경로 불일치
   - 메타의 `og-image.png`, JSON-LD의 `logo.png`, `/search` 경로와 실제 리소스/라우트 불일치

### P3
1. 품질 드리프트(테스트/코드 불일치)
   - `__tests__/components/product-card.test.tsx`는 `SOLD OUT` 기대
   - 실제 `components/product-card.tsx`는 `품절` 렌더링
2. dead code/unused vars 존재
   - `components/product-card.tsx`, `components/product-card-skeleton.tsx`

## 4. 디자인/UIUX 평가

### 강점
- 브랜드 토큰 시스템이 비교적 체계적 (`app/globals.css`, `docs/BRAND_TOKENS.md`)
- 모바일 터치 타깃/안전영역/가독성 고려가 코드에 반영됨
- 주요 사용자 플로우(탐색→상세→장바구니→결제)의 UI 스토리라인이 일관적

### 개선 포인트
- 접근성은 정책 문서 대비 자동 검증(axe 등)이 부족
- 상태 관리가 단일 컴포넌트에 집중된 화면이 있어 UX 회귀 가능성 높음
- 분석 이벤트 기반 실험/검증 루프가 현재 동작하지 않음(analytics stub)

## 5. 보안 평가

### 현재 상태
- 일부 기본 헤더 적용 (`nosniff`, `frame deny`, `HSTS`)은 긍정적
- 그러나 인증/권한 모델이 프론트 상태에 상대적으로 의존

### 우선 개선
1. 관리자 인증을 서버 발급 `httpOnly + Secure + SameSite` 세션으로 이관
2. 고객 API에서 `X-User-ID` 의존 제거, 서버 세션 주체 기반으로 통일
3. review-login 운영 노출 차단(환경 분리 + 서버 가드 + rate limit)
4. CSP/Permissions-Policy/Referrer policy 정비

## 6. 기술부채/구조 평가

### 관찰
- 기능은 넓게 확장됐으나, 도메인 경계가 일부 흐릿함
- 거대한 화면 파일/훅이 다수 존재, 유지보수 비용 증가
- 테스트는 양이 충분하지만 기준 불일치로 신뢰도 하락 신호 존재

### 권고
1. API 클라이언트 단일화(`lib/http/client`)로 인증/에러 처리 정책 통합
2. 대형 페이지 분해: 화면 컴포넌트/도메인 로직/데이터 훅 분리
3. CI에 `lint + test + typecheck + e2e` 필수 게이트 적용

## 7. 30/60/90 개선 계획

### 0-30일
- 관리자 인증 모델 서버 세션 기반으로 전환
- `X-User-ID` 제거/축소 및 서버 권한 검증 강화
- lint/test 깨짐 0건 복구
- 보안 헤더 강화(CSP, Permissions-Policy), deprecated 헤더 제거
- `pnpm audit` high 이슈 제거

### 31-60일
- checkout/cart/admin 도메인별 리팩터링
- 공통 API 계층/에러 모델/리트라이 정책 수립
- Analytics 실구현(GA4/Mixpanel) 및 이벤트 스키마 단일화
- SEO 자산/메타 정합성 정리

### 61-90일
- 접근성 자동검증(axe) CI 도입
- 성능 SLO(Core Web Vitals) 운영지표화
- 분기 단위 보안 점검(OWASP API Top 10 기준)
- 의존성 업데이트 자동화(Renovate/Dependabot) + SLA

## 8. 즉시 실행 체크리스트
- [ ] `review-login` 운영 차단
- [ ] 관리자 토큰 클라이언트 저장 제거
- [ ] `credentials: "omit"` 사용 API 재검토
- [ ] `product-card` 테스트/문구 불일치 수정
- [ ] analytics stub 제거 및 실제 이벤트 송신 연결
- [ ] `og-image.png`, `logo.png`, `/search` 정합성 보정

## 9. 참고한 공식 문서/기준
- Next.js 16.1: https://nextjs.org/blog/next-16-1
- Next.js Support Policy: https://nextjs.org/support-policy
- Next.js Security Update (2025-12-11): https://nextjs.org/blog/security-update-2025-12-11
- Next.js proxy convention: https://nextjs.org/docs/app/api-reference/file-conventions/proxy
- React 19.2: https://react.dev/blog/2025/10/01/react-19-2
- React RSC Security Update: https://react.dev/blog/2025/12/11/denial-of-service-and-source-code-exposure-in-react-server-components
- Tailwind CSS v4: https://tailwindcss.com/blog/tailwindcss-v4
- WCAG 2.2: https://www.w3.org/WAI/news/2023-10-05/wcag22rec/
- Core Web Vitals: https://web.dev/articles/vitals
- OWASP Top 10 (2021): https://owasp.org/Top10/2021/
- OWASP API Top 10 (2023): https://owasp.org/API-Security/editions/2023/en/0x11-t10/
- OWASP IDOR Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html
- OWASP HTML5 Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html
- MDN X-XSS-Protection (Deprecated): https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection

