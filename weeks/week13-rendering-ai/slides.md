---
marp: true
theme: rpd
paginate: true
---

# Week 13: AI 영상/사운드 + 렌더링 + MCP

## 로봇프러덕트 디자인

2026 Spring | 인하대학교 | 송지희

---

## Camera 기초

- **Camera 추가:** Shift+A > Camera
- **Camera 뷰:** Numpad 0
- **Camera to View:** Ctrl+Alt+Numpad 0 (현재 뷰 -> 카메라 뷰)

**Focal Length (초점 거리):**

| 값 | 특징 | 용도 |
|------|------|------|
| 35mm | 표준 광각, 자연스러운 화각 | 제품 전체 촬영 |
| 50mm | 사람 눈과 유사 | 일반 제품 촬영 |
| 85mm | 배경 압축, 왜곡 적음 | 클로즈업, 디테일 |

---

## Depth of Field 설정

- Camera Properties > **Depth of Field** 체크
- **Focus Object:** 초점 대상 오브젝트 선택
- **F-Stop:** 조리개 값 (작을수록 배경 흐림이 강함)

| F-Stop | 효과 | 용도 |
|--------|------|------|
| 1.4~2.8 | 배경 강하게 흐림 | 제품 강조 |
| 4.0~5.6 | 적당한 배경 흐림 | 일반 촬영 |
| 8.0~16 | 대부분 선명 | 전체 장면 |

**로봇 제품 추천:** F-Stop 2.8, Focus Object = 로봇

---

## Eevee vs Cycles 비교

| 항목 | Eevee | Cycles |
|------|-------|--------|
| 렌더 방식 | 래스터화 (실시간) | 레이트레이싱 |
| 속도 | 매우 빠름 | 느림 (수 분~시간) |
| 품질 | 게임 수준 | 포토리얼 |
| 반사/굴절 | Screen Space (제한적) | 물리 기반 (정확) |
| 그림자 | Shadow Map | 레이트레이싱 (부드러움) |
| GI | 제한적 | 정확한 간접광 |
| **추천 용도** | **실습, 애니메이션** | **최종 렌더, 포트폴리오** |

---

## Eevee 주요 설정

**Render Properties > Eevee:**

- **Sampling:** Render 64~128 / Viewport 16~32
- **Ambient Occlusion:** 틈새 그림자 추가
- **Screen Space Reflections:** 반사 효과
  - Refraction 체크: 투명 재질 굴절
- **Bloom:** 밝은 부분 빛 번짐 효과
  - Threshold: 블룸 시작 밝기
  - Intensity: 블룸 강도
  - Emission Material과 함께 사용 시 효과적

**Eevee = 빠른 테스트와 실습에 최적**

---

## Cycles 주요 설정

**Render Properties > Cycles:**

- **Device:** GPU Compute 선택
  - CUDA (NVIDIA) / HIP (AMD) / Metal (Apple Silicon)
- **Sampling:** Render 128~512 (256 권장)
  - Adaptive Sampling: 노이즈 적은 영역 자동 최적화
- **Denoising:** 체크 필수
  - Denoiser: **OpenImageDenoise** 권장
  - 128 Samples + Denoising >= 512 Samples 품질

**핵심:** GPU + Denoising으로 속도와 품질 모두 확보

---

## Blender 5.0 색상 관리 (AgX)

**Render Properties > Color Management:**

| Transform | 설명 | 용도 |
|-----------|------|------|
| **AgX** | Blender 5.0 기본, 권장 | 대부분의 작업 |
| Filmic | 이전 버전 기본 | 레거시 호환 |
| Standard | 선형 색상 표시 | 데이터 시각화 |
| ACES | 영화 산업 표준 | VFX 워크플로우 |

**AgX 장점:**
- 하이라이트가 자연스럽게 롤오프
- 색상 번짐 감소 (Filmic 대비)
- 금속 반사가 자연스럽게 표현됨

**Look:** None / High Contrast / Medium Contrast

---

## 렌더 출력 설정

**Resolution:**
- 1920 x 1080 (Full HD) - 기본 권장
- 3840 x 2160 (4K) - 포트폴리오용
- Resolution %: 50%로 빠른 테스트 가능

**Frame Rate:**
- 24fps (영화) / 30fps (일반) / 60fps (게임)

**Output Format:**
- PNG: 무손실, Alpha 지원
- JPEG: 용량 작음
- MP4 (FFmpeg): 애니메이션

**렌더 실행:**
- F12: 이미지 렌더 / Ctrl+F12: 애니메이션 렌더

---

## AI 영상: Kling AI 워크플로우

**klingai.com - 이미지 -> 비디오 변환**

**워크플로우:**
1. Blender에서 렌더 이미지 저장 (PNG/JPG)
2. Kling AI > Image to Video > 이미지 업로드
3. 영문 프롬프트 입력
4. Generate > 다운로드

**프롬프트 예시:**
- "A cute robot slowly turning its head and waving"
- "Camera orbiting around a sleek robot product"
- "The robot's eyes lighting up with a gentle glow"

**팁:** 단순한 움직임일수록 자연스러운 결과

---

## AI 영상: Veo (Google)

**Google Gemini의 비디오 생성 기능**

**특징:**
- 텍스트만으로 새로운 영상 생성 (이미지 불필요)
- Gemini 앱에서 직접 사용 가능

**프롬프트 예시:**
- "A small white robot with blue LED eyes sitting on a desk, 4K cinematic"
- "Product showcase of a futuristic robot, rotating on turntable"

**Kling vs Veo:**
| | Kling AI | Veo |
|--|----------|-----|
| 입력 | 렌더 이미지 기반 | 텍스트만 |
| 장점 | 내 로봇 디자인 활용 | 새로운 영상 생성 |
| 수업 추천 | **주로 사용** | 보조적 활용 |

---

## AI 음악: Suno AI

**suno.com - 텍스트 -> 음악 생성**

**사용법:**
1. Create 클릭 > Song Description 입력
2. Create > 2곡 자동 생성 > 선택 후 다운로드 (MP3)

**프롬프트 구성:**
- **장르:** electronic, ambient, cinematic, lo-fi
- **분위기:** cheerful, calm, energetic, futuristic
- **용도:** product showcase, background music
- **길이:** 30 seconds, 1 minute

**예시:**
- "cheerful electronic music for a robot product showcase, upbeat, 30 seconds"
- "calm ambient music, futuristic, soft synth pads, 1 minute"

---

## AI 음악: ElevenLabs Music

**elevenlabs.io - 음악 + Sound Effects 생성**

**Sound Effects가 강점:**
- "robot servo motor whirring sound"
- "futuristic UI notification chime"
- "mechanical arm clicking sound effect"

**Suno vs ElevenLabs:**

| | Suno AI | ElevenLabs |
|--|---------|------------|
| 강점 | 음악(곡) 생성 | Sound Effects |
| 보컬 | 가능 | 제한적 |
| 길이 | 2분+ | 짧은 효과음 |

**추천 조합:** Suno BGM + ElevenLabs 효과음

---

## Compositor 기초

**렌더 후 이미지 후처리 (Post-Processing)**

**주요 노드:**
- **Glare:** 빛 번짐 효과 (Fog Glow / Streaks)
  - 로봇 Emission 파츠(눈, LED)에 효과적
- **Color Balance:** Lift/Gamma/Gain 색보정
  - 영화적 톤 매핑
- **Denoise:** Cycles 노이즈 후처리 제거
- **Lens Distortion:** 색수차(Chromatic Aberration) 효과

**Blender 5.0 업데이트:**
- Video Sequencer에서 Compositor Modifier 직접 사용 가능

---

## MCP 카메라/렌더 자동화

**Claude에게 자연어로 카메라/렌더 설정 요청:**

**카메라 설정:**
- "Set camera at 45 degree angle, focal length 50mm"
- "Enable depth of field with f-stop 2.8"

**렌더 설정:**
- "Set render engine to Eevee with bloom enabled"
- "Switch to Cycles with GPU rendering, 256 samples"

**여러 앵글 한 번에 설정:**
```
Create 3 cameras:
1. Front hero shot, 50mm, f-stop 2.8
2. Head close-up, 85mm, f-stop 1.8
3. Low angle dramatic, 35mm, f-stop 5.6
```

**MCP = 반복 설정 자동화로 시간 절약**

---

## 핵심 정리 + 다음 주 예고

**오늘 배운 것:**
- **Eevee:** 빠른 실습용, Bloom/AO/SSR로 품질 향상
- **Cycles:** 고품질 최종본, GPU + Denoising 필수
- **AgX:** Blender 5.0 기본 색상 관리
- **Kling AI:** 렌더 이미지 -> AI 비디오
- **Suno/ElevenLabs:** AI BGM + 효과음 생성
- **MCP:** 카메라/렌더 설정 자동화

**과제:** Eevee/Cycles 렌더 비교 + AI 영상 + AI BGM 생성

**다음 주 (Week 14): 최종 프로젝트 제작 시작!**
모든 기술을 종합하여 로봇 프러덕트 완성 + 프로모션 영상 제작
