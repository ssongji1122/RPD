---
title: W05 콘텐츠 감사 — 결재 대기열
last_updated: 2026-07-20
status: pending
---

# Week 05 콘텐츠 감사 — 결재 대기

**감사 대상:** weeks/week05-ai3d-sculpting/lecture-note.md, course-site 이미지 참조
**감사일:** 2026-07-20

## 자동 반영됨 (기록용)

| # | 항목 | 근거 |
|---|------|------|
| ① | "Blender 5.0: SDF 기반 스컬프팅" 섹션 삭제 (본문 + 핵심 정리 표) | Blender 5.0 공식 릴리스 노트(developer.blender.org/docs/release_notes/5.0/sculpt/)에 SDF 스컬프팅 기능 부재 — 환각 |
| ② | Mask 브러시 단축키 "M 키로 마스크 해제 / Alt+M으로 반전" → "Alt+M으로 마스크 해제(Clear Mask) / Ctrl+I로 마스크 반전(Invert Mask)" | docs.blender.org/manual/en/latest/sculpt_paint/sculpting/editing/mask.html |
| ③ | W05 플레이스홀더 이미지 참조 4건 제거 (ai-3d-generation.png, sculpt-mode.png, sculpt-brushes.png, remesh.png) | 파일이 tofu 플레이스홀더·빈 캡처 |

## 결재 대기 (수치·판단)

| # | 위치 | 현재 서술 | 검증 결과 | 제안 수정 | 근거 URL |
|---|------|-----------|-----------|-----------|----------|
| 1 | lecture-note.md 도구 비교표 | "Meshy AI \| ... \| 월 200 크레딧" | 무료 플랜 실제 100 크레딧 | "월 100 크레딧"으로 수정 | [meshy.ai/pricing](https://www.meshy.ai/pricing), [help.meshy.ai 15696428](https://help.meshy.ai/en/articles/15696428) (2026-07-20 확인) |
| 2 | 같은 표 | "Tripo AI \| ... \| 월 500 크레딧" | 공식 200 크레딧, 출처별 200~300 편차 | "월 200 크레딧" 또는 "월 200~300 크레딧(변동)"으로 수정 | [tripo3d.ai/pricing](https://www.tripo3d.ai/pricing) |
| 3 | 같은 표 | "Luma Genie \| ... \| 제한적 무료" | 접속 경로 불안정(메인 페이지로 리다이렉트), 서비스 유지 여부 불명확 | 행 삭제, 또는 3D AI Studio 등 대체 도구로 교체 | 접속 확인 결과 자체 (2026-07-20) |
| 4 | 과제 섹션 | "Blender 로 다운받은 경우( hyper 3d GEN 1.5 버전은 다운로드 가능)" | 현행 최신은 Gen-2.5, 1.5는 legacy. 무료 플랜은 생성 무제한·다운로드 시 크레딧 차감(가입 시 10크레딧) | "hyper 3d GEN 2.5 버전(2026-07 기준 최신)" 및 무료 크레딧 조건 명시로 수정 | [hyper3d.ai](https://hyper3d.ai), [developer.hyper3d.ai](https://developer.hyper3d.ai) |
| 5 | Meshy 관련 서술 | 무료 다운로드 제한 언급 없음 | 무료 플랜은 최신 엔진 생성물 한정 + 월 다운로드 개수 제한 있음 | 각주 추가 검토 | help.meshy.ai |
| 6 | Tripo 관련 서술 | "넉넉한 무료 크레딧" | 다운로드 월 15회 제한 존재 | 표현 완화 검토 ("무료 크레딧 제공, 다운로드는 월 15회 제한") | tripo3d.ai/pricing |
| 7 | 실습 단계 체크리스트 | "Ctrl+Tab으로 Sculpt Mode 전환" | 공식 문서에서 확인 안 됨 (Blender 기본 매핑은 Tab 단일키 + 모드 pie 메뉴가 일반적) | 재확인 필요, 확인 전까지 [Unknown] 태그 유지 | 불확실 — 재확인 대상 |
| 8 | 실습 이미지 | 제거된 플레이스홀더 4장 대체 필요 | 실캡처 부재 | Meshy UI·Sculpt Mode·브러시·Remesh 실캡처 4장 신규 제작 | — |
| 9 | 참고 자료 "Blender Studio - Introduction to Sculpting" | 출처 링크만 존재 | 해당 코스는 Blender 4.5 LTS 기준 | 수업 실제 사용 Blender 버전 표기와 일치 여부 확인 | [studio.blender.org](https://studio.blender.org/training/blender-fundamentals-45-lts/sculpting_introduction/) |

반영 절차: 결재 후 lecture-note 수정 → notion-push 워크플로우(weeks: 5)로 Notion 반영.
