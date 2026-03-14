---
marp: true
theme: rpd
paginate: true
---

# Week 05: AI 3D 생성 + Sculpting + MCP 활용

## 로봇프러덕트 디자인

2026 Spring | 인하대학교 | 송지희

---

## AI 3D 생성이란?

- **텍스트 to 3D:** 프롬프트 입력 > AI가 3D 모델 생성
- **이미지 to 3D:** 2D 이미지 업로드 > 3D 모델로 변환
- AI 생성 모델의 한계:
  - 토폴로지 품질이 불균일
  - 세밀한 디테일 부족
  - 의도와 다른 형태 가능
- **핵심:** AI로 빠르게 초안 > Blender에서 정밀 수정

---

## 도구 비교: Meshy vs Tripo vs Luma

| 도구 | 특징 | 강점 |
|------|------|------|
| **Meshy AI** | 빠른 생성 속도 | 안정적 결과물, Text to 3D |
| **Tripo AI** | 클린 토폴로지 | 넉넉한 무료 크레딧, Image to 3D |
| **Luma Genie** | 형태 이해도 높음 | 복잡한 형태에 강점 |

- 오늘 실습: **Meshy AI** (Text to 3D) + **Tripo AI** (Image to 3D)

---

## 실습: Meshy AI에서 3D 생성

1. https://meshy.ai 접속 및 로그인
2. **Text to 3D** 선택
3. 프롬프트 입력:
   - "cute mini robot character, round body, simple design"
4. 스타일 선택 및 생성 시작
5. 여러 각도에서 미리보기 확인
6. **GLB/FBX** 형식으로 다운로드

---

## Blender 임포트 및 스케일 조정

1. File > Import > **glTF 2.0 (.glb/.gltf)**
2. 다운로드한 파일 선택 후 Import
3. **S** 키로 스케일 조정
4. Right-click > Set Origin > **Origin to Geometry**
5. **Ctrl+A** > Apply All Transforms
6. **Z** 키 > Wireframe 모드로 토폴로지 확인

---

## AI 모델의 한계점

- **토폴로지 문제:** Ngon, 겹치는 Face, 불균일한 Face 분포
- **디테일 부족:** 세밀한 부분이 뭉개지거나 누락
- **형태 왜곡:** 프롬프트 의도와 다른 결과 가능
- **텍스처 품질:** 해상도가 낮거나 이음새가 보임

**해결 방법: Blender Sculpt Mode로 수정**

---

## Sculpt Mode 진입

- Object Mode에서 오브젝트 선택
- **Tab** 키 또는 상단 모드 메뉴에서 **Sculpt Mode** 선택
- 브러시 기본 조작:
  - 브러시 크기: **F**
  - 브러시 강도: **Shift+F**
  - 더하기/빼기 전환: **Ctrl**

---

## 핵심 브러시: Draw, Clay Strips

**Draw 브러시**
- 표면을 올리거나(+) 내림(-)
- Ctrl로 더하기/빼기 전환
- 가장 기본적인 조각 브러시

**Clay Strips 브러시**
- 점토를 덧붙이듯 볼륨 추가
- 넓은 영역에 효과적
- 큰 형태를 잡을 때 유용

---

## 핵심 브러시: Smooth, Grab

**Smooth 브러시**
- 표면을 부드럽게 정리
- **Shift** 키: 어떤 브러시에서든 임시 Smooth 전환
- 다른 브러시 작업 후 정리용

**Grab 브러시**
- 표면을 잡아서 이동
- 큰 형태를 변형할 때 사용
- Proportional Editing과 유사한 효과

---

## Mask 사용법

- 특정 영역을 **보호** (마스크된 부분은 브러시 영향 없음)
- **M** 키: 마스크 해제 (Clear)
- **Alt+M**: 마스크 반전
- 부분적으로 수정할 때 필수 기능
- 수정하지 않을 영역을 먼저 마스크 > 나머지 영역만 수정

---

## AI 모델을 Sculpt로 수정하기

1. AI 모델을 **Sculpt Mode**로 진입
2. **Smooth** 브러시로 거친 표면 정리
3. **Grab** 브러시로 전체 형태 조정
4. **Draw/Clay Strips**로 디테일 추가
5. **Mask**로 수정하지 않을 영역 보호
6. 반복: 큰 형태 > 중간 디테일 > 세부 디테일

---

## Blender MCP 씬 자동 생성

- Claude에 프롬프트 전송:
  - "Create a studio setup with a white floor plane, 3-point lighting, and a camera at 45 degrees"
- MCP가 Blender에서 **자동으로 씬 구성**
- AI 생성 로봇을 씬 중앙에 배치
- 추가 조정 프롬프트:
  - "Make the key light warmer and brighter"

---

## MCP 활용 예시

**씬 셋업**
- "Create a white background studio with soft lighting"
- "Add a turntable setup for 360 view"

**조명 조절**
- "Make the key light warmer"
- "Add a subtle rim light from the back"

**카메라 설정**
- "Set camera to eye-level, pointing at origin"
- "Switch to orthographic camera view"

---

## 과제 안내 (Before/After)

- **제출:** Discord #week05-assignment 채널
- **형식:**
  - 이미지 2장 (AI 원본 vs Sculpt 수정 후 비교)
  - 사용한 AI 도구 이름
  - 한줄 코멘트

| 평가 항목 | 비율 |
|-----------|------|
| AI 도구 활용 | 30% |
| Sculpt 수정 품질 | 40% |
| 창의성 | 30% |

---

## 다음 주 예고

**Week 06: Material & Shader**

- Blender의 Material 시스템 이해
- Shader Editor와 Node 기반 재질 설정
- PBR (Physically Based Rendering) 기초
- AI 텍스처 생성 도구 활용
