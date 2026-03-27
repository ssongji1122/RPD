/* course-site/assets/supabase-config.js
   ──────────────────────────────────────────────────────────
   Supabase 프로젝트 자격증명 설정 파일

   TODO: supabase.com에서 프로젝트 생성 후 아래 두 값을 채워주세요.
   Settings → API 탭에서 확인할 수 있어요.

   Google OAuth 활성화:
     Supabase 대시보드 → Authentication → Providers → Google
     → Google Cloud Console에서 OAuth 앱 생성 후 클라이언트 ID/Secret 입력

   Redirect URL: https://[your-project].supabase.co/auth/v1/callback
   (Supabase가 자동으로 처리 — 별도 설정 불필요)
   ────────────────────────────────────────────────────────── */

window.SUPABASE_URL  = 'https://YOUR_PROJECT_ID.supabase.co'; // TODO: 실제 URL로 교체
window.SUPABASE_ANON = 'YOUR_ANON_KEY';                       // TODO: 실제 anon key로 교체

/* 설정 완료 여부를 확인하는 헬퍼 — 미설정 시 auth 기능 비활성화 */
window.SUPABASE_CONFIGURED =
  window.SUPABASE_URL  !== 'https://YOUR_PROJECT_ID.supabase.co' &&
  window.SUPABASE_ANON !== 'YOUR_ANON_KEY';
