# RPD 콘텐츠 QA 감사 보고서

감사 일시: 2026-06-02
감사 범위: course-site/data/, course-site/assets/showme/, course-site/library.html, course-site/week.html, syllabus.md

---

## 1. 외부 URL 유효성

### 1-1. 404 (실제 깨진 링크)

| 우선순위 | 유형 | 위치(파일:라인) | 문제 | 현재값 | 제안 | 수정경로 |
|---|---|---|---|---|---|---|
| 높음 | 링크 | data/curriculum.js:1710 / data/overrides.json:299 / assets/showme/_catalog.js:926 / assets/showme/_supplements.js:854 | 404 - sculpting-in-blender 트레이닝 폐기 | https://studio.blender.org/training/sculpting-in-blender/introduction/ | https://studio.blender.org/training/sculpting-in-blender/ 또는 Blender 공식 문서로 교체 | overrides.json (데이터 소스) / Notion (원본 생성) |
| 높음 | 링크 | assets/showme/_catalog.js:941 / assets/showme/_catalog.json:966 | 404 - sculpting-in-blender/brushes/ 폐기 | https://studio.blender.org/training/sculpting-in-blender/brushes/ | https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/index.html 로 교체 | overrides.json / Notion |
| 중간 | 링크 | assets/showme/blender-mcp.html:350,407,613 | 404 - GitHub 저장소 삭제됨 | https://github.com/ahuja312/blender-mcp | 현재 활성 blender-mcp 저장소로 교체 (예: https://github.com/nagi1/blender-mcp 등 검증 후) | 해당 showme HTML 직접 편집 가능 |

### 1-2. 도메인 소실 (DNS 실패)

| 우선순위 | 유형 | 위치(파일:라인) | 문제 | 현재값 | 제안 | 수정경로 |
|---|---|---|---|---|---|---|
| 높음 | 링크 | data/notion-blocks/week12.json:1208,1220 | DNS 실패 - 도메인 소실 | https://blenrig.com/ | Blender 리깅 공식 문서로 교체: https://docs.blender.org/manual/en/latest/animation/armatures/index.html | Notion (SSoT) |

### 1-3. URL 변경으로 인한 리다이렉트 (200 응답이지만 목적지가 달라짐)

아래 URL들은 HTTP 200을 반환하지만, 특정 페이지 대신 상위 목록 페이지로 리다이렉트됨.

#### studio.blender.org - 개별 chapter 페이지 소실 (메인 training 페이지로 리다이렉트)

| 우선순위 | 유형 | 위치(파일:라인) | 문제 | 현재값 | 최종 도달 URL | 제안 | 수정경로 |
|---|---|---|---|---|---|---|---|
| 낮음 | 링크(리다이렉트) | data/curriculum.js:1971 / data/overrides.json:365 / assets/showme/_catalog.js:642 | 개별 lesson 없어짐, 메인 training 페이지로 redirect | https://studio.blender.org/training/blender-2-8-fundamentals/materials-and-shading/ | https://studio.blender.org/training/blender-2-8-fundamentals/ | 현재 URL 유지 가능 (사용자는 training 페이지에 도달함). 정확한 챕터 링크 원하면 Notion에서 수정 | Notion |
| 낮음 | 링크(리다이렉트) | data/curriculum.js:3226 / data/overrides.json:641 / assets/showme/_catalog.js | 동일 | https://studio.blender.org/training/blender-2-8-fundamentals/armature-and-rigging/ | https://studio.blender.org/training/blender-2-8-fundamentals/ | 동일 | Notion |
| 낮음 | 링크(리다이렉트) | data/curriculum.js:3454 / data/overrides.json:698 | 동일 | https://studio.blender.org/training/blender-2-8-fundamentals/importing/ | https://studio.blender.org/training/blender-2-8-fundamentals/ | 동일 | Notion |
| 낮음 | 링크(리다이렉트) | data/curriculum.js:1427 / data/overrides.json:229 / assets/showme/_catalog.js:여러 곳 | 동일 | https://studio.blender.org/training/blender-2-8-fundamentals/modifiers/ | https://studio.blender.org/training/blender-2-8-fundamentals/ | 동일 | Notion |

#### studio.blender.org - chapter URL 변경 (200, 다른 경로로 리다이렉트)

| 우선순위 | 유형 | 위치(파일:라인) | 문제 | 현재값 | 최종 도달 URL | 제안 | 수정경로 |
|---|---|---|---|---|---|---|---|
| 낮음 | 링크(리다이렉트) | 여러 곳 | /lighting/ -> /chapter/lighting/ 경로 변경 | https://studio.blender.org/training/blender-2-8-fundamentals/lighting/ | https://studio.blender.org/training/blender-2-8-fundamentals/chapter/lighting/ | 200 응답이므로 긴급도 낮음. Notion 수정 시 chapter/ 경로 사용 권장 | Notion |
| 낮음 | 링크(리다이렉트) | 여러 곳 | /animation/ -> /chapter/animation/ 경로 변경 | https://studio.blender.org/training/blender-2-8-fundamentals/animation/ | https://studio.blender.org/training/blender-2-8-fundamentals/chapter/animation/ | 동일 | Notion |
| 낮음 | 링크(리다이렉트) | 여러 곳 | /rendering/ -> /chapter/rendering/ 경로 변경 | https://studio.blender.org/training/blender-2-8-fundamentals/rendering/ | https://studio.blender.org/training/blender-2-8-fundamentals/chapter/rendering/ | 동일 | Notion |

#### antigravity.codes → agentpedia.codes 도메인 이전

| 우선순위 | 유형 | 위치(파일:라인) | 문제 | 현재값 | 최종 도달 URL | 제안 | 수정경로 |
|---|---|---|---|---|---|---|---|
| 낮음 | 링크(리다이렉트) | notion-blocks (week14 등) | 도메인 이전 (200 응답이나 도메인 바뀜) | https://antigravity.codes/mcp 등 | https://agentpedia.codes/mcp | 200 유지되므로 당장 조치 불필요. Notion에서 최신 도메인으로 교체 권장 | Notion |

#### 기타 리다이렉트 (정보성)

| URL | 최종 도달 | 비고 |
|---|---|---|
| https://withpoly.com | https://poly.app/ | 200, 서비스 리브랜딩 |
| https://blendergrid.com/learn/articles/realistic-lighting-in-blender | https://blendergrid.com/articles/realistic-lighting-in-blender | 200, URL 구조 변경 |

---

## 2. 이미지 참조 무결성

curriculum.js와 overrides.json에서 참조하는 step.image 파일 중 실제 파일이 없는 항목.

| 우선순위 | 유형 | 위치(파일:라인) | 문제 | 현재값 | 제안 | 수정경로 |
|---|---|---|---|---|---|---|
| 중간 | 이미지 | data/curriculum.js:1523 / data/overrides.json:329 | 파일 없음 | assets/images/week05/mesh-cleanup.png | 실제 이미지 파일 추가 또는 overrides.json에서 image 키 제거 | 이미지 추가: 직접 / 참조 제거: overrides.json |
| 중간 | 이미지 | data/curriculum.js:1877 / data/overrides.json:412 | 파일 없음 | assets/images/week06/texture-node.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:1900 / data/overrides.json:418 | 파일 없음 | assets/images/week06/shading-modes.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:2101 / data/overrides.json:470 | 파일 없음 | assets/images/week07/smart-uv.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:2158 / data/overrides.json:482 | 파일 없음 | assets/images/week07/texture-paint.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:2801 / data/overrides.json:608 | 파일 없음 | assets/images/week10/rotation-scale.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:2860 / data/overrides.json:621 | 파일 없음 | assets/images/week10/graph-editor.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:2884 / data/overrides.json:628 | 파일 없음 | assets/images/week10/loop-animation.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:3125 / data/overrides.json:677 | 파일 없음 | assets/images/week11/pose-mode.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:3154 / data/overrides.json:684 | 파일 없음 | assets/images/week11/weight-paint.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:3294 / data/overrides.json:721 | 파일 없음 | assets/images/week12/export-prep.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:3379 / data/overrides.json:740 | 파일 없음 | assets/images/week12/nla-editor.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:3578 / data/overrides.json:789 | 파일 없음 | assets/images/week13/compositing.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:3607 / data/overrides.json:796 | 파일 없음 | assets/images/week13/animation-render.png | 동일 | overrides.json |
| 중간 | 이미지 | data/curriculum.js:3630 / data/overrides.json:802 | 파일 없음 | assets/images/week13/ai-postprocess.png | 동일 | overrides.json |

**참고:** 위 이미지들은 curriculum.js(Notion-sourced, 편집 금지)에도 참조되어 있지만, 실제 렌더 파이프라인에서 overrides.json의 image 값이 우선 적용되므로 수정경로는 overrides.json 또는 실제 파일 추가.

---

## 3. showme 카드 참조 무결성

### 3-1. _catalog.js 등록 카드 vs 실제 HTML 파일

카탈로그에 등록된 카드는 모두 HTML 파일이 존재함. 이슈 없음.

### 3-2. HTML 파일 존재하나 _catalog.js에 미등록 (정보성)

다음 showme HTML은 파일은 있지만 _catalog.js manualSectionMap에 등록되지 않음. library 페이지에 노출 안 될 수 있음.

| 카드 ID | 상태 | 비고 |
|---|---|---|
| apply-modifier-vs-keep-procedural | _catalog.js 미등록 | _registry.js에는 있음 |
| blender-mcp | _catalog.js 미등록 | _registry.js에 있음 |
| bridge-edge-loops | _catalog.js 미등록 | _registry.js에 있음 |
| bsdf | _catalog.js 미등록 | _registry.js에 미확인 |
| camera-setup | _catalog.js 미등록 | - |
| collection-outliner | _catalog.js 미등록 | _registry.js에 있음 |
| depth-of-field | _catalog.js 미등록 | - |
| dope-sheet | _catalog.js 미등록 | _registry.js에 있음 |
| duplicate-vs-linked-duplicate | _catalog.js 미등록 | _registry.js에 있음 |
| face-orientation-normals | _catalog.js 미등록 | _registry.js에 있음 |
| mcp-concept | _catalog.js 미등록 | - |
| merge-by-distance | _catalog.js 미등록 | _registry.js에 있음 |
| modifier-stack-order | _catalog.js 미등록 | _registry.js에 있음 |
| mood-lighting | _catalog.js 미등록 | - |
| nla-editor | _catalog.js 미등록 | _registry.js에 있음 |
| remesh-decimate | _catalog.js 미등록 | - |
| shade-smooth-auto-smooth | _catalog.js 미등록 | _registry.js에 있음 |
| texture-nodes | _catalog.js 미등록 | - |
| texture-painting | _catalog.js 미등록 | - |

---

## 4. 내부 링크 유효성

| 우선순위 | 유형 | 위치(파일:라인) | 문제 | 현재값 | 제안 | 수정경로 |
|---|---|---|---|---|---|---|
| 낮음 | 내부 | week.html:605 | notion-blocks/weekNN.json 동적 로드 (week01~15 전부 존재 확인됨) | data/notion-blocks/week01.json~week15.json | 정상 | - |
| 낮음 | 내부 | index.html:90 | curriculum.js 참조 (파일 존재 확인됨) | data/curriculum.js | 정상 | - |
| 낮음 | 내부 | index.html:511 | references.json 참조 (파일 존재 확인됨) | data/references.json | 정상 | - |

---

## 5. 정상 확인 항목 요약

- docs.blender.org 모든 URL (52개): 200 OK
- studio.blender.org 현재 존재하는 개별 lesson URL (viewport-navigation, select-transform, extrude, loop-cut, bevel-tool, uv-unwrapping, first-steps 등): 200 OK
- YouTube 영상 링크 (샘플 5개 확인): 200 OK
- docs.polyhaven.com, extensions.blender.org, github.com/ahuja312 제외 GitHub 관련: 200 OK
- decoded.gumroad.com, ksami.gumroad.com: 200 OK
- modelcontextprotocol.io: 200 OK (경로 변경되었으나 200)
- 라이브러리 의존성 (fonts.googleapis.com, cdn.jsdelivr.net): 미체크 (CDN 봇 차단 가능성으로 생략)
- showme _catalog.js 등록 카드 전체 (68개): HTML 파일 존재 확인
- notion-blocks week01~week15.json: 전부 존재

---

## 결론

- **실제 404**: 3건 (sculpting-in-blender 2개 + github ahuja312 1개 + blenrig.com DNS 실패 1건)
- **누락 이미지**: 15건 (week05~13 분포, curriculum.js와 overrides.json 모두 참조)
- **리다이렉트 경고**: studio.blender.org 일부 chapter URL이 메인 페이지로 fallback (사용자 도달은 되나 정확한 챕터 아님)
- **showme 미카탈로그**: 19개 카드가 파일은 있으나 _catalog.js 미등록 (library 노출 영향)
