---
marp: true
theme: rpd
paginate: true
---

# Week 09: Lighting 기초 + MCP 조명 연출

## 로봇프러덕트 디자인

2026 Spring | 인하대학교 | 송지희

---

## 조명의 역할

- **분위기 (Mood):** 따뜻한 vs 차가운 조명으로 감정 전달
- **깊이감 (Depth):** 그림자를 통해 3D 형태 강조, 공간감 부여
- **시각적 무게 (Visual Weight):** 밝은 부분에 시선이 집중

> 같은 모델이라도 조명에 따라 완전히 다른 느낌을 전달할 수 있다.
> **조명 = 분위기의 80%**

---

## Blender 조명 4가지 타입

| 타입 | 형태 | 특징 | 사용 예시 |
|------|------|------|-----------|
| **Point** | 점 | 모든 방향으로 빛 발산 | 전구, 촛불 |
| **Sun** | 무한 평행 | 위치 무관, 방향만 영향 | 태양, 달빛 |
| **Spot** | 원뿔 | 특정 방향에 집중 | 무대 조명, 가로등 |
| **Area** | 면 | 넓은 면에서 부드러운 빛 | 소프트박스, 모니터 |

**추가:** Shift+A > Light에서 선택

---

## 조명 Properties

**공통 설정:**
- **Color:** 조명 색상 (따뜻한/차가운 분위기 결정)
- **Power (Watts):** 밝기 강도
- **Shadow:** 그림자 활성화/비활성화

**타입별 고유 설정:**
- Point: **Radius** (클수록 부드러운 그림자)
- Sun: **Angle** (빛의 퍼짐 각도)
- Spot: **Spot Size** (원뿔 각도), **Blend** (가장자리 부드러움)
- Area: **Shape** (Rectangle/Disk 등), **Size** (면적)

---

## 3-Point Lighting

영화, 사진, 3D에서 가장 기본이 되는 조명 구성법:

| 조명 | 역할 | 권장 타입 | 밝기 비율 |
|------|------|-----------|-----------|
| **Key Light** | 메인 조명, 전체 밝기 결정 | Area Light | 100% |
| **Fill Light** | 그림자를 채워주는 보조 | Area Light | 30~50% |
| **Back Light** | 뒤에서 윤곽선(rim) 생성 | Spot Light | 50~70% |

**배치:** Key=앞 45도, Fill=반대편, Back=뒤쪽 위

---

## HDRI 환경 조명

**HDRI (High Dynamic Range Imaging):**
- 360도 파노라마 이미지에 실제 환경의 빛 정보를 담은 것
- 하나의 이미지만으로 **사실적 환경 조명 + 반사** 동시 구현

**설정 방법:**
1. World Properties (지구 아이콘)
2. Surface > Background > Color 옆 노란 점 클릭
3. **Environment Texture** 선택
4. Open > HDR/EXR 파일 로드
5. Strength로 밝기 조절

---

## 무료 HDRI 리소스

**Poly Haven (polyhaven.com/hdris):**
- Indoor, Outdoor, Studio 등 다양한 카테고리
- 해상도: 1K ~ 4K 선택 가능
- 라이선스: CC0 (무료, 상업적 사용 가능)

**Blockade Labs Skybox (skybox.blockadelabs.com):**
- 텍스트 프롬프트 입력 → AI가 360도 HDRI 생성
- 원하는 환경을 텍스트로 직접 만들 수 있음
- 프롬프트 예시:
  - "modern photography studio with soft white lighting"
  - "futuristic neon-lit city at night"

---

## Blender 5.0 색상 관리: AgX

**View Transform 비교:**

| Transform | 특징 |
|-----------|------|
| **AgX** (기본) | 자연스러운 하이라이트 롤오프, 채도 보존 |
| Filmic | 넓은 다이나믹 레인지, 약간 desaturated |
| Standard | 색 보정 없음 (비추천) |

**AgX 장점:**
- Blender 5.0 기본값으로 채택
- 강한 조명에서도 색상이 과도하게 빠지지 않음
- 컬러풀한 로봇/제품 렌더에 특히 적합

---

## 실습 1: 3-Point Lighting 세팅

**Key Light:**
- Area Light, Power 200W, Size 2m
- 로봇 왼쪽 앞 45도 위에 배치
- Color: 약간 따뜻한 흰색 (#FFF5E6)

**Fill Light:**
- Area Light, Power 60~80W, Size 3m
- Key Light 반대편에 배치
- Color: 약간 차가운 흰색 (#E6F0FF)

**Back Light:**
- Spot Light, Power 100W, Spot Size 60도
- 로봇 뒤쪽 위에 배치

---

## 실습 2: HDRI 적용

**Poly Haven HDRI:**
1. polyhaven.com/hdris에서 Studio HDRI 다운로드 (2K)
2. World Properties > Environment Texture > Open
3. Strength 0.5~2.0으로 밝기 조절

**Blockade Labs AI HDRI:**
1. skybox.blockadelabs.com에서 프롬프트 입력
2. 생성된 360 이미지 다운로드
3. 동일한 방법으로 Blender에 적용

**팁:** 3-Point Lighting + HDRI를 함께 사용하면 더욱 사실적!

---

## 실습 3: Claude MCP 조명 자동 연출

**따뜻한 스튜디오:**
```
"Create a warm sunset studio lighting setup
for my robot model with area lights"
```

**드라마틱 Noir:**
```
"Set up dramatic single-light noir style
with hard shadows and black background"
```

**밝은 제품 사진:**
```
"Create bright product photography lighting
with soft shadows and white background"
```

---

## 3가지 조명 환경 렌더 비교

각 환경에서 F12로 렌더 후 비교:

| 환경 | 분위기 | 조명 구성 |
|------|--------|-----------|
| **밝은 스튜디오** | 깨끗하고 전문적 | 3-Point + 밝은 HDRI |
| **무드 있는 환경** | 드라마틱하고 감성적 | 단일/컬러 조명 + 어두운 배경 |
| **AI HDRI** | 창의적이고 독특 | Blockade Labs 환경 + 보조 조명 |

**렌더 설정:** 1920x1080, AgX View Transform

---

## 과제 안내

- **제출처:** 본인 학생 페이지
- **내용:**
  - 3가지 조명 환경에서 자신의 로봇 렌더 이미지 3장
  - 각 이미지에 조명 설정 한줄 설명
- **평가:**
  - 조명 설정 적절성 35%
  - 분위기 표현 35%
  - AI 도구 활용 30%

---

## 다음 주: Animation 기초

**Week 10: Animation 기초**

- Keyframe과 Timeline 개념
- 로봇에 간단한 움직임 부여
- Graph Editor로 자연스러운 이징 조절
- 3~5초 애니메이션 제작

조명이 끝났으니 이제 로봇을 움직여 봅시다!
