# Week 05 Sculpt/Remesh 도구 상세 설명 + ShowMe 카드 링크 매칭

**Date**: 2026-03-31
**Status**: Draft
**Scope**: Notion Week 05 페이지 내 빨간색 도구 이름에 디테일 설명 추가 + ShowMe 카드 연결

---

## 1. 목적

Week 05 노션 페이지의 Sculpt Mode 기초/심화/Remesh 섹션에 있는 빨간색 도구 이름들(Draw, Grab, Smooth, Clay Strips, Crease, Inflate, Snake Hook, Remesh, Decimate, QRemeshify)에:
1. **디테일 설명** (5~8줄 + 공식 문서 스크린샷 + YouTube 임베드) 추가
2. **ShowMe 카드 링크** 매칭 (기존 카드 활용, 신규 생성 없음)

## 2. 대상 페이지

- Notion Page ID: `31354d65-4971-811e-85fe-ed7681421e37`
- 제목: "Week 05: AI 3D 생성 + Sculpting"

## 3. 카드 매칭 맵

| 노션 빨간 도구 이름 | ShowMe 카드 ID | 비고 |
|---------------------|---------------|------|
| Draw | `sculpt-basics` | 기존 카드 |
| Grab | `sculpt-basics` | 기존 카드 |
| Smooth | `sculpt-basics` | 기존 카드 |
| Clay Strips | `sculpt-brushes` | 기존 카드 |
| Crease | `sculpt-brushes` | 기존 카드 |
| Inflate | `sculpt-brushes` | 기존 카드 |
| Snake Hook | `sculpt-brushes` | 기존 카드 |
| Remesh | `remesh-modifier` | 기존 카드 |
| Decimate | `decimate-modifier` | 기존 카드 |
| QRemeshify | - | 외부 애드온, 노션만 상세 설명 |
| Mesh Cleaner 2 | - | 외부 애드온, 노션만 상세 설명 |

## 4. 캡처 이미지 계획

### 신규 캡처 필요 (7장)

| 도구 | 파일명 | Blender 공식 문서 URL |
|------|--------|---------------------|
| Draw | `sculpt-draw.png` | `https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/draw.html` |
| Grab | `sculpt-grab.png` | `https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/grab.html` |
| Smooth | `sculpt-smooth.png` | `https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/smooth.html` |
| Clay Strips | `sculpt-clay-strips.png` | `https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/clay_strips.html` |
| Crease | `sculpt-crease.png` | `https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/crease.html` |
| Inflate | `sculpt-inflate.png` | `https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/inflate.html` |
| Snake Hook | `sculpt-snake-hook.png` | `https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/snake_hook.html` |

저장 디렉토리: `course-site/assets/images/week05/`

### 이미 캡처 완료 (재사용)

| 도구 | 파일명 |
|------|--------|
| Remesh | `blender-remesh-official.png` |
| Decimate | `blender-decimate-official.png` |
| QRemeshify | `qremeshify-github.png` |

## 5. 노션 콘텐츠 구조

각 빨간색 도구 이름 근처에 `<details>` 토글로 추가:

```markdown
<details>
<summary>{이모지} {도구명} 상세</summary>

{5~8줄 설명: 용도, 주요 파라미터/옵션, 실전 팁}

![{도구명} 공식 문서](GitHub raw URL)

> [{도구명} — Blender 공식 문서](Blender docs URL)

{YouTube 영상 URL — 자동 임베드}

> ShowMe 카드에서 인터랙티브 학습 → {course-site ShowMe 링크}

</details>
```

### 섹션별 배치

**Sculpt Mode 기초** (기존 체크리스트 아래):
- Draw 상세 토글
- Grab 상세 토글
- Smooth 상세 토글
- → ShowMe: `sculpt-basics` 링크 1개 (섹션 하단)

**Sculpt 브러시 심화** (기존 체크리스트 아래):
- Clay Strips 상세 토글
- Crease 상세 토글
- Inflate 상세 토글
- Snake Hook 상세 토글
- → ShowMe: `sculpt-brushes` 링크 1개 (섹션 하단)

**Remesh + Decimate + 메쉬 정리** (기존 체크리스트 아래):
- 이미 인라인 Remesh 가이드 존재 (이전 세션에서 추가됨)
- → ShowMe: `remesh-modifier` + `decimate-modifier` 링크 (섹션 하단)

## 6. YouTube 영상 선정 기준

- Blender 공식 또는 인지도 높은 채널 우선 (Blender Studio, Grant Abbitt, Blender Guru)
- 해당 도구에 집중하는 짧은 영상 (5분 이내 권장)
- 웹 검색으로 최적 영상 선정

## 7. 구현 순서

1. **캡처**: `/capture` 스킬로 7개 브러시 공식 문서 페이지 스크린샷
2. **Git 커밋 + 푸시**: 스크린샷을 GitHub에 올려 raw URL 확보
3. **YouTube 리서치**: 각 도구별 최적 영상 검색
4. **노션 업데이트**: `notion-fetch` → `notion-update-page`로 10개 도구 상세 + 카드 링크 추가
5. **검증**: 노션 페이지 재조회로 결과 확인

## 8. ShowMe 카드 링크 URL 패턴

```
https://ssongji1122.github.io/RPD/course-site/week.html?week=5&showme={card-id}
```

## 9. 범위 외 (하지 않는 것)

- 새 ShowMe 카드 생성 (기존 카드 활용)
- Step 4~6 (무드보드, AI 생성, AI 정리) 섹션 수정
- curriculum.js 수정 (이미 showme 필드 매핑 완료)
- 기존 Remesh 인라인 가이드 재작성
