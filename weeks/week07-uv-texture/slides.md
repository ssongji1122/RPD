---
marp: true
theme: rpd
paginate: true
---

# Week 07: UV Unwrapping + AI Texture

## 로봇프러덕트 디자인

2026 Spring | 인하대학교 | 송지희

---

## UV란?

- 3D 표면을 **2D 평면으로 펼치는 것**
- **선물 포장지 비유:** 3D 상자를 감싼 포장지를 펼치면 2D 종이가 됨
- U, V는 2D 좌표축 이름 (3D의 X, Y, Z와 구분)
- 2D 이미지(텍스처)를 3D 표면에 정확히 매핑하기 위해 필요

---

## UV가 필요한 이유

**UV 없이 텍스처 적용:**
- 이미지가 늘어나거나 왜곡됨
- 의도한 위치에 패턴이 매핑되지 않음

**UV를 설정한 후:**
- 2D 텍스처가 3D 표면에 정확하게 매핑됨
- 게임, 영화, 제품 디자인 등 모든 3D 파이프라인에서 필수 과정

---

## Seam 개념

- 3D 모델을 2D로 펼칠 때 **잘라야 할 선**
- 종이 상자를 접착 면에서 잘라 펼치는 것과 같은 원리
- Seam 위치에 따라 UV 결과가 크게 달라짐

**설정 방법:**
- Edge 선택 > Ctrl+E > **Mark Seam** (빨간색 선 표시)
- 제거: Ctrl+E > **Clear Seam**

---

## Mark Seam 사용법

**작업 순서:**
1. Edit Mode 진입 (Tab)
2. Edge 선택 모드 (숫자 2 키)
3. Seam을 배치할 Edge 선택
4. Ctrl+E > Mark Seam
5. 전체 Face 선택 (A)
6. U > Unwrap
7. UV Editor에서 결과 확인

---

## Unwrap 방법들

| 방법 | 특징 | 적합한 형태 |
|------|------|------------|
| Unwrap | Seam 기반 수동 Unwrap, 가장 정교 | 모든 형태 |
| Smart UV Project | 자동 Seam + Unwrap, 간편 | 빠른 작업 시 |
| Cube Projection | 6방향 투영 | 육면체 형태 |
| Cylinder Projection | 원통 투영 | 원기둥 형태 |
| Sphere Projection | 구형 투영 | 구형 형태 |

---

## UV Editor 인터페이스

- Editor Type > **UV Editor**로 전환
- **UV Island:** Seam 기준으로 분리된 UV 조각
- UV Island 편집: G (이동), R (회전), S (스케일)
- UV가 **0~1 범위** 정사각형 안에 들어가야 올바르게 매핑
- 겹치는 UV Island가 없도록 정리

---

## 좋은 Seam 전략

**배치 원칙:**
- **눈에 안 보이는 곳:** 뒷면, 안쪽, 접히는 부분
- **자연스러운 경계선:** 파츠 사이, 색상이 바뀌는 곳
- 관절 부분은 자연스러운 Seam 위치

**주의:**
- Seam이 너무 적으면 UV가 심하게 왜곡됨
- Seam이 너무 많으면 UV Island가 지나치게 분리됨

---

## Texture Painting 기초

**설정:**
1. Shader Editor에서 Image Texture 노드 추가 > New Image 생성
2. 이미지 크기: 1024x1024 또는 2048x2048

**작업:**
- Texture Paint 모드로 전환
- 브러시 색상, 크기, 강도 조절
- 3D 모델 위에 직접 페인팅
- Image > Save로 자주 저장

---

## AI 텍스처 생성

**Meshy AI (meshy.ai):**
- 3D 모델 업로드 후 AI가 텍스처 자동 생성
- 다양한 스타일 선택 가능

**나노바나나 (nanobananas.ai):**
- 텍스처 패턴 이미지 생성
- 프롬프트 예시:
  - "seamless robot skin texture, metallic blue, circuit patterns"
  - "glowing energy pattern, neon blue lines, seamless tile"

---

## AI 텍스처를 UV에 적용

**적용 순서:**
1. AI 도구에서 텍스처 이미지 다운로드
2. Shader Editor에서 Image Texture 노드 추가
3. Open으로 이미지 로드
4. Color -> Principled BSDF의 Base Color에 연결
5. UV가 올바르게 설정되어 있으면 자동 매핑

**조정:**
- UV Editor에서 UV Island 위치를 조절하여 텍스처 배치 수정

---

## 텍스처 저장과 관리

**저장:**
- Blender 내부 텍스처: Image > Save As로 외부 파일 저장
- 저장하지 않으면 파일을 닫을 때 텍스처 소실 주의
- 포맷: PNG (투명도) / JPG (용량 절약)

**Pack Resources:**
- File > External Data > Pack Resources
- 외부 이미지를 Blender 파일에 포함
- 파일 이동 시에도 텍스처가 깨지지 않음

---

## 과제 안내

- **제출처:** 본인 학생 페이지에 업로드
- **내용:**
  - 렌더 이미지 2장 (서로 다른 각도)
  - UV 전개도 스크린샷 1장
  - 한줄 코멘트
- **평가:** UV 작업 품질 30% / 텍스처 활용 40% / 완성도 30%

---

## 다음 주: 중간고사 안내

**Week 08: 중간고사**

- **범위:** 모델링 + 텍스처 완성본 제출
- **준비물:** 로봇/캐릭터 모델에 Material과 텍스처가 적용된 완성본
- **평가:** 모델링 완성도 + Material 활용 + 텍스처 품질

이번 주 과제를 통해 중간고사 준비를 병행할 것!
