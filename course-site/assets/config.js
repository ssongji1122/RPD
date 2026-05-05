/* course-site/assets/config.js
   RPD 전역 설정 — localStorage 키 상수 모음
   모든 파일에서 리터럴 문자열 대신 이 상수를 참조하세요. */

window.RPD_KEYS = {
  USER:         'rpd-user',        // user-profile.js — 게스트 프로필 객체
  USER_NAME:    'rpd-user-name',   // auth.js — Supabase 로그인 시 표시 이름
  DECKS:        'rpd-decks',       // deck-store.js / sync.js — 덱 배열
  SYNCED_UID:   'rpd-synced-uid',  // sync.js — 마이그레이션 완료 uid
  DIVISION:     'rpd-division',    // division-select.js — 선택된 분반 (게스트 폴백)
  RAIL:         'rpd-rail',        // layout.js — 사이드 레일 열림/닫힘
  IS_ADMIN:     'rpd-is-admin',    // admin-role.js — 관리자 여부 세션 캐시
  ADMIN_DEV:    'rpd-admin',       // admin-role.js — 개발용 관리자 강제 설정
  THEME:        'rpd-theme',       // site-shell.js — 컬러 테마
  LANG:         'rpd-lang',        // i18n.js — UI 언어
};
