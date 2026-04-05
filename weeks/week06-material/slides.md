---
marp: true
theme: rpd
paginate: true
---

# Week 06: AI 메쉬 Remesh 정리 + Material & Shader Node

## 로봇프러덕트 디자인

2026 Spring | 인하대학교 | 송지희

---

## Step 1: AI 메쉬 Remesh — 왜 필요한가?

AI(Meshy/Tripo)로 만든 메쉬는 토폴로지가 엉망이에요.

**정리 안 하면:**
- Material 쉐이더가 깨짐
- UV 전개 불가
- Normal 방향 오류

**→ 오늘 Remesh로 '작업 가능한 상태' 먼저 만들기**

---

## Remesh 도구 5종

| 도구 | 용도 |
|------|------|
| **Mesh Cleaner 2** | 중복 버텍스·노멀 원클릭 정리 |
| **Voxel Remesh** | 폴리곤 균일화 |
| **Quad Remesh (Ctrl+R)** | 쿼드 토폴로지 (애니메이션용) |
| **Decimate Modifier** | 고폴리 감량 |
| **QRemeshify** | 삼각형 → 쿼드 변환 |

---

## Remesh 실습 순서

1. **Statistics 켜서 Before 폴리곤 수 기록**
2. **Mesh Cleaner 2 실행** (가장 먼저)
3. **Decimate Modifier → Ratio 0.5**
4. **Quad Remesh (Ctrl+R)** (선택)
5. **Before/After 비교 스크린샷** (Numpad 1 고정)
6. **체크:** Material Preview로 쉐이더 깨짐 없음 확인

---

## Material이란?

- 오브젝트의 **표면 속성**을 정의하는 데이터 블록
- 색상, 반사, 투명도, 거칠기 등 시각적 특성을 결정
- 하나의 오브젝트에 **여러 Material**을 부위별로 할당 가능
- 같은 형태라도 Material에 따라 완전히 다른 느낌

---

## Material 생성 및 할당

**생성:**
- Properties > Material Properties > New

**여러 Material 할당:**
1. Edit Mode 진입
2. 할당할 Face 선택
3. Material 슬롯에서 원하는 Material 선택
4. Assign 버튼 클릭

**Fake User (F 아이콘):** 사용하지 않아도 파일에 Material 유지

---

## Principled BSDF 파라미터

| 파라미터 | 설명 | 범위 |
|---------|------|------|
| Base Color | 기본 색상 | Color / Hex / 텍스처 |
| Metallic | 금속성 | 0=비금속, 1=금속 |
| Roughness | 거칠기 | 0=매끄러움, 1=거침 |
| Specular | 정반사 강도 | 0~1 |
| IOR | 굴절률 | 유리 1.5, 물 1.33 |
| Alpha | 투명도 | 0=투명, 1=불투명 |
| Emission | 자체 발광 | Color + Strength |

---

## Metallic & Roughness 조합 예시

**Metallic = 1 (금속)**
- Roughness 0.1: 거울처럼 반짝이는 크롬
- Roughness 0.3: 광택 있는 금속 (로봇 몸체)
- Roughness 0.7: 무광 금속 (브러시드 메탈)

**Metallic = 0 (비금속)**
- Roughness 0.1: 광택 플라스틱
- Roughness 0.5: 일반 플라스틱
- Roughness 0.8: 매트 플라스틱 (로봇 관절)

---

## 특수 재질: 유리, 발광

**투명 유리:**
- Transmission: 1, IOR: 1.5, Roughness: 0
- 로봇 바이저, 카메라 렌즈에 활용

**자체 발광:**
- Emission Color + Emission Strength 설정
- 로봇의 눈, LED 표시등, 에너지 코어에 활용
- Strength 1~10 범위에서 조절

---

## Blender 5.0: Thin Film Iridescence

- Principled BSDF > **Thin Film** 섹션에서 활성화
- 비눗방울, 기름막 같은 **무지개빛 효과**
- 빛의 간섭 현상을 물리적으로 시뮬레이션

**주요 파라미터:**
- **Film Thickness:** 막의 두께 (200~800nm)
- **Film IOR:** 막의 굴절률 (색상 변화 강도)

**활용:** 로봇 금속 표면에 적용하면 미래적인 느낌

---

## Shader Node Editor 기초

**열기:** Editor Type > Shader Editor (또는 Shading Workspace)

**기본 구성:**
- Principled BSDF -> Material Output

**노드 연결 원리:**
- 출력 소켓 (오른쪽) -> 입력 소켓 (왼쪽) 드래그
- 색상은 노란색, 값은 회색, 벡터는 보라색 소켓

**유용한 노드:**
- Image Texture, Color Ramp, Math, Mix

---

## Image Texture 연결

**기본 텍스처 연결:**
1. Add > Texture > Image Texture
2. Open으로 이미지 파일 로드
3. Color 출력 -> Base Color 입력에 연결

**Color Space 설정:**
- 색상 맵 (Diffuse): sRGB
- 데이터 맵 (Roughness, Normal): Non-Color

**Normal Map 연결:**
- Image Texture -> Normal Map 노드 -> Principled BSDF Normal 입력

---

## Poly Haven PBR 텍스처

**Poly Haven (polyhaven.com):**
- 무료 CC0 라이센스 PBR 텍스처 라이브러리
- 금속, 나무, 돌, 패브릭 등 다양한 재질 제공

**PBR 텍스처 구성:**
- **Diffuse Map:** Base Color에 연결
- **Roughness Map:** Roughness에 연결 (Non-Color)
- **Normal Map:** Normal Map 노드를 거쳐 Normal에 연결
- **Displacement Map:** 표면 디테일 추가 (선택 사항)

---

## 실습: 로봇에 재질 적용

**Material 계획:**
- 몸체: 금속 (Metallic=1, Roughness=0.3)
- 눈: 발광 (Emission Color + Strength)
- 관절: 매트 플라스틱 (Roughness=0.8)
- 금속 파츠: Thin Film Iridescence 적용

**작업 순서:**
1. Material 슬롯에 여러 Material 추가
2. Edit Mode에서 Face 선택 후 Assign
3. Material Preview에서 결과 확인

---

## 과제 안내

- **제출처:** Discord #week06-assignment 채널
- **내용:**
  - Remesh 전후 비교 스크린샷 (Statistics, Numpad 1 고정)
  - 렌더 이미지 1~2장
  - 사용한 재질 종류 설명
  - 한줄 코멘트
- **평가:** Material 활용 다양성 40% / 완성도 30% / 창의성 30%
- **조건:** Remesh 정리 후 3가지 이상의 서로 다른 재질을 적용할 것

---

## 다음 주 예고

**Week 07: UV Unwrapping + AI Texture**

- UV 개념: 3D 표면을 2D로 펼치기
- Seam 설정과 Unwrap 방법
- AI 도구로 텍스처 생성 및 적용
- 로봇에 커스텀 텍스처 입히기
