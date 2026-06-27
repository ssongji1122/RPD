# RPD 2026-06 업데이트 후보 통합 (검증 반영)

- 감사일: 2026-06-02
- 축: Blender 버전 정합성 · 외부 AI 도구 최신성 · 콘텐츠 QA(링크/이미지)
- 상세 원본: `blender-version.md`, `ai-tools.md`, `content-qa.md`
- 검증 반영: ahuja312 오타 / 이미지 dead code / 404 재확인 (아래 "검증 메모")

## 게이팅 (먼저 읽을 것)

- **Sync가 게이트이고 현재 다운**: `NOTION_TOKEN` 미설정 확인. Notion 본문(week{N}.json 등)을 connector로 고쳐도 `notion-sync.py`가 막혀 **웹사이트엔 미반영**. → 버킷 B는 "Notion만 최신화 + sync 대기" 또는 "토큰 복구 후 반영" 중 택1.
- **직접 편집 = 즉시 반영**: `syllabus.md`, `docs/*.md`, `course-site/assets/showme/*.html`, `course-site/data/overrides.json`은 repo 직접 편집 가능(GitHub Pages push로 반영).

---

## 버킷 A — 기계적 수정 · 직접 편집 · 즉시 반영 가능

| # | 항목 | 위치 | 조치 | 근거 |
|---|------|------|------|------|
| A1 | blender-mcp repo username 오타 | `course-site/assets/showme/blender-mcp.html` (3곳) | `ahuja312` → `ahujasid` | ahujasid/blender-mcp=200, ahuja312=404 (검증함). 삭제 아님 |
| A2 | ElevenLabs Music 명칭 | syllabus.md 등 | "Eleven Music"으로 정정 | 정식명 변경(2025-08). 무료 7곡/일 |
| A3 | 나노바나나 정체 각주 | syllabus.md 등 | "= Gemini 2.5 Flash Image 별칭" 명시 | 단일 모델→패밀리 별칭 |
| A4 | Meshy "AI Texture" 표기 | syllabus.md W7 | 별도 도구 아닌 Meshy 기능으로 정정 | — |

> A2~A4는 syllabus.md 내 실제 표기 위치 확인 후 수정. syllabus는 직접 편집 가능.

---

## 버킷 B — Notion 콘텐츠 · sync 대기 (토큰 복구 전 사이트 미반영)

| # | 항목 | 위치 | 조치 | 수정경로 |
|---|------|------|------|---------|
| B1 | Blender 버전 stray 1건 | `notion-blocks/pages/cd654d65-…json` "Blender 4.4" | "Blender 5.0"으로 (기능은 5.0에도 동일) | Notion |
| B2 | blenrig.com 죽은 링크 | `notion-blocks/week12.json:1208` | docs.blender.org armature 매뉴얼로 교체 | Notion |
| B3 | sculpting-in-blender 404 (본문) | `curriculum.js:1710` (generated) | studio.blender.org 유효 트레이닝 URL로 교체 | Notion |
| B4 | sculpting-in-blender 404 (override/카드) | `overrides.json:299`, `assets/showme/_catalog.js:926·941` | 유효 URL로 교체 | overrides.json·_catalog.js = **직접 가능** |

> B4는 overrides.json/_catalog.js라 직접 편집 가능(즉시). B1~B3은 Notion 경유라 sync 대기.

---

## 버킷 C — 교육 설계 판단 필요 (강사 결정, 자동 수정 대상 아님)

| # | 항목 | 발견 | 권장(강사 판단) |
|---|------|------|----------------|
| C1 | **Skybox (W9)** | 무료로 HDRI export 자체 불가, HDRI는 $48/월~ [High, 공식] | 무료는 "생성 체험"만, 실제 조명은 **Poly Haven 무료 HDRI(CC0)**로 재설계 |
| C2 | **Veo (W13)** | 무료 Gemini로 사용 불가, Google AI Pro($19.99/월)~ [High] | Kling을 무료 주력으로, Veo는 "유료/선택" 명시 |
| C3 | **Luma Genie (W5)** | 단독 제품 deprioritize, 진입점 모호 [Medium] | Meshy+Tripo 주력, Genie 강등/제거 |
| C4 | **Blender MCP 공식 커넥터 (W2)** | 2026-04 Anthropic 공식 출시, 무료 플랜 OK, 드래그앤드롭 [High] | W2 설치 가이드를 공식 커넥터로 갱신(진입장벽 하락) + 안전 주의 |
| C5 | **Mixamo (W12)** | 무료 유지하나 Adobe 방치 + 장애 이력 [High] | 백업 플랜(Rigify/사전 다운로드) 준비, 계정 필요 사전 안내 |
| C6 | 무료 제약 고지 | Kling(워터마크/720p/5초), Suno(비상업), Tripo(공개+CC BY), Meshy(월10·CC BY) | 각 주차에 무료 한계 한 줄 고지 |

---

## 버킷 D — dead code / 정보성 (사이트 영향 거의 없음)

| # | 항목 | 비고 |
|---|------|------|
| D1 | 누락 이미지 15건 | week05·06·07·10·11·12·13 모두 notion-blocks 캐시 보유 → overrides image는 **dead code**. 정리는 위생 목적(선택) |
| D2 | showme 19개 카드 미등록 | `_catalog.js` 미등록이라 library 미노출. 등록은 선택 |
| D3 | 리다이렉트 경고 | studio.blender.org 일부 챕터 fallback, antigravity.codes→agentpedia.codes (낮음) |
| D4 | syllabus↔curriculum 정합성 | curriculum.js W2 steps에 MCP 설치 step 부재 (ai-tools 감사가 관찰) — 별도 점검 |

---

## 검증 메모 (원본 audit 대비 교정)

1. **content-qa "ahuja312 삭제→링크 제거"는 오판**: 실제 username 오타(`ahujasid`). 교정으로 변경 → A1.
2. **content-qa "이미지 15건 수정"은 과대평가**: 해당 주차 notion-blocks 캐시 존재 확인 → dead code(D1)로 강등.
3. **404 재검증 통과**: blenrig.com=DNS 소실(000), sculpting-in-blender=브라우저 UA로도 404. 봇 차단 아님 → 진짜 교체 대상.
4. **버전 stray는 1건뿐**: 비-5.0 언급 60여 건 중 나머지는 의도적 대조/경고(버전 이력, 외부 도구 호환성). 기계적 치환 금지.
