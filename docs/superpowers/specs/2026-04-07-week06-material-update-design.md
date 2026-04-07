# Week 6 Material Update Design

**Date:** 2026-04-07
**Based on:** 블렌더 6주차 노드 기반 PBR 텍스처 수업 보완 가이드(2).pdf
**Scope:** Notion Week 6 page + curriculum.js CURRICULUM[5]

## Overview

PDF 9개 섹션(§0~§9)을 Week 6 구조에 직접 매핑. 기존 7 Step → 9 Step으로 확장.
신규 Step: §3 머티리얼 소스 활용, §4 Shader Editor 실습, §7 EEVEE Next vs Cycles.

## Step 구조 매핑

| Step | PDF 섹션 | 내용 | 변경 |
|------|---------|------|------|
| Step 1 | §0 | 체크리스트 / 준비물 | 보강 |
| Step 2 | §1~§2 | 머티리얼 기초 + Principled BSDF | 보강 |
| Step 3 | 신규 | 머티리얼 소스 활용 (BlenderKit, withpoly, ambientcg) | 신규 |
| Step 4 | §4 | Shader Editor 노드 실습 3종 | 신규 |
| Step 5 | §5 | Poly AI PBR 텍스처 (withpoly.com) | 보강 |
| Step 6 | §6 | 렌더링 (라이팅 + 카메라) | 보강 |
| Step 7 | §7 | EEVEE Next vs Cycles 비교 | 신규 |
| Step 8 | §8 | Blender MCP 실습 | 보강 |
| Step 9 | §9 | 과제 제출 기준 | 보강 |

## Step별 세부 설계

### Step 3 — 머티리얼 소스 활용 (신규)
- BlenderKit 내장 애드온: 검색 → 클릭 → 적용 워크플로우
- 무료 PBR 사이트: withpoly.com, ambientcg.com
- 치트시트는 "이해용" — 다운받은 머티리얼의 값 읽는 법
- 재질 이름 규칙: 영문 + 언더바 (MCP 자동화 이유)

### Step 4 — Shader Editor 노드 실습 (신규)
- 레시피 1: Noise Texture → Color Ramp → Principled BSDF (절차적 텍스처)
- 레시피 2: Image Texture → BSDF Base Color (이미지 텍스처)
- 레시피 3: Emission BSDF + Principled BSDF → Add Shader → Material Output (발광)

### Step 7 — EEVEE Next vs Cycles (신규)
- EEVEE Next: 실시간, 수업 권장, Screen Space Reflections 활성화
- Cycles: 물리 정확, 렌더 시간 김, 최종 포트폴리오용
- 권장: 수업 중 EEVEE Next, 제출 전 Cycles

## 구현 대상

1. **Notion**: `31354d65-4971-818c-8cb5-e7814445e3eb` (Week 6 page)
   - 신규 Step 블록 추가 (Step 3, 4, 7)
   - 기존 Step 블록 내용 보강

2. **curriculum.js**: `/course-site/data/curriculum.js` CURRICULUM[5].steps
   - 7개 → 9개 step objects
   - goal/tasks/showme 업데이트
