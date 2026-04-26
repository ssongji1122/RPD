# Week 09 과제: 3가지 조명 환경 렌더

## 학습 목표

- [ ] 3-Point Lighting 시스템을 직접 구성할 수 있다
- [ ] HDRI 환경 조명을 설정하고 분위기를 조절할 수 있다
- [ ] AI 도구(Blockade Labs, MCP)를 활용하여 조명을 연출할 수 있다
- [ ] 서로 다른 조명 환경에서 렌더하여 분위기 차이를 표현할 수 있다

## 과제 내용

자신의 로봇 또는 캐릭터 모델을 **3가지 서로 다른 조명 환경**에서 렌더링하여 제출한다. 각 조명 환경은 확연히 다른 분위기를 표현해야 한다.

### 3가지 조명 환경

#### 환경 1: 밝은 스튜디오 (Bright Studio)

- 3-Point Lighting 또는 다중 Area Light 구성
- 밝고 깨끗한 제품 사진 느낌
- 배경: 밝은 색상 또는 Studio HDRI
- 참고: 제품 카탈로그, 쇼핑몰 사진 스타일

#### 환경 2: 무드 있는 환경 (Moody Atmosphere)

- 단일 조명 또는 컬러 조명 활용
- 드라마틱한 명암 대비 또는 감성적 분위기
- 배경: 어두운 색상 또는 분위기 있는 HDRI
- 참고: 영화 포스터, 컨셉 아트 스타일

#### 환경 3: AI HDRI 환경 (AI-Generated Environment)

- Blockade Labs Skybox로 생성한 AI HDRI 적용
- 또는 Claude MCP를 활용하여 조명 자동 구성
- 창의적인 환경 설정 권장
- AI 도구를 활용한 프롬프트도 함께 기록

### 렌더 설정 가이드

- **해상도:** 1920x1080 이상
- **View Transform:** AgX (Render Properties > Color Management)
- **렌더 엔진:** Eevee 또는 Cycles (선택 자유)
- **카메라 앵글:** 로봇의 형태와 조명이 잘 보이는 각도

### 조명 설정 한줄 설명 예시

- "Key: Area 200W warm + Fill: Area 60W cool + Back: Spot 100W + Studio HDRI"
- "Single Spot Light 500W, 45도 각도, 하드 섀도우, 검은 배경"
- "AI HDRI: futuristic robot lab + Area Light 50W 보조"

## 제출 방법

- **제출처:** 본인 학생 페이지
- **형식:**
  - 렌더 이미지 3장 (환경 1, 2, 3 각 1장)
  - 각 이미지에 대한 조명 설정 한줄 설명 (3줄)
  - AI HDRI 사용 시 프롬프트 포함
- **기한:** 다음 수업 전까지

## 평가 기준

| 항목 | 비율 | 세부 기준 |
|------|------|-----------|
| 조명 설정 적절성 | 35% | 각 환경에 맞는 조명을 올바르게 구성했는가, 조명 타입과 설정값이 적절한가 |
| 분위기 표현 | 35% | 3가지 환경이 확연히 다른 분위기를 표현하는가, 조명으로 의도한 감정을 전달하는가 |
| AI 도구 활용 | 30% | Blockade Labs Skybox 또는 Claude MCP를 효과적으로 활용했는가, 프롬프트가 구체적인가 |

## 참고 자료

- [Poly Haven HDRI Library](https://polyhaven.com/hdris) - 무료 CC0 HDRI
- [Blockade Labs Skybox](https://skybox.blockadelabs.com) - AI 360 HDRI 생성
- [Blender Manual: Lighting](https://docs.blender.org/manual/en/latest/render/lights/index.html)
- [3-Point Lighting Tutorial](https://www.youtube.com/results?search_query=3+point+lighting+blender) - 3점 조명 영상 튜토리얼
