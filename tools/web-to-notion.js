#!/usr/bin/env node

/**
 * Student progress sync is intentionally disabled.
 *
 * 공개 사이트는 읽기 전용이며, 학생/학습자 식별 데이터는
 * 인증 체계가 준비되기 전까지 브라우저 로컬 저장소에서만 유지합니다.
 */

console.error("❌ node tools/web-to-notion.js 는 현재 비활성화되어 있습니다.");
console.error("   이유: 학생 진행도/퀴즈 서버 동기화는 인증 체계 도입 전까지 허용하지 않습니다.");
console.error("   현재 정책: 공개 사이트는 local-only progress, 관리자 작업만 private API에서 처리합니다.");
process.exit(1);
