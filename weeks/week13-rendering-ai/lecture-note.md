# Week 13: AI 영상/사운드 + 렌더링 + MCP

## 🔗 이전 주차 복습

> **Week 09의 조명 설정 + Week 10의 애니메이션 기법이 합쳐지는 최종 렌더링 단계입니다.**
>
> - **Week 09 조명:** 3-Point Lighting, HDRI 환경맵, Emission Material 등으로 장면에 분위기를 만들었습니다.
> - **Week 10 애니메이션:** Keyframe, Graph Editor, 타이밍 조절로 로봇에 생명을 불어넣었습니다.
> - **이번 주:** 그 모든 것을 카메라로 담아 최종 이미지/영상으로 출력하고, AI 도구로 프로모션 컨텐츠까지 제작합니다.
>
> 렌더링은 "디지털 사진 촬영"과 같습니다. 아무리 모델링과 애니메이션이 훌륭해도 카메라와 렌더 설정이 나쁘면 결과물의 품질이 떨어집니다.

## 학습 목표

- [ ] Camera 설정과 렌더링 기초를 이해한다
- [ ] Eevee와 Cycles 렌더러의 차이를 이해한다
- [ ] AI 영상 및 사운드 생성 도구를 활용할 수 있다
- [ ] Claude MCP로 카메라/렌더 설정을 자동화할 수 있다

## 이론 (40분)

> 이번 주차는 렌더링, AI 미디어 생성, MCP 자동화까지 다루는 내용이 가장 많은 주차입니다.
> 이론 시간을 40분으로 확장하여 진행합니다.

### Camera 설정

#### Camera 추가 및 기본 조작

- **Camera 추가:** Shift+A > Camera
- **Camera 뷰 전환:** Numpad 0 (Camera 시점으로 전환)
- **Camera to View:** Ctrl+Alt+Numpad 0 (현재 뷰포트 시점을 그대로 Camera 뷰로 설정)
- **Camera 선택:** Scene에서 Camera 오브젝트 클릭, 또는 Outliner에서 선택
- **Camera 이동/회전:** G (이동), R (회전) - 일반 오브젝트와 동일하게 조작

#### Focal Length (초점 거리)

- Camera Properties > Lens > Focal Length에서 설정
- 단위: mm (밀리미터)
- **렌즈별 특성:**

| Focal Length | 명칭 | 특징 | 용도 |
|-------------|------|------|------|
| 24mm 이하 | 광각 | 넓은 시야, 왜곡 있음 | 공간 전체 촬영, 건축 |
| 35mm | 표준 광각 | 자연스러운 화각 | 일반 촬영, 제품 전체 |
| 50mm | 표준 | 사람 눈과 가장 유사 | 인물, 제품 촬영 |
| 85mm | 중망원 | 배경 압축, 왜곡 적음 | 클로즈업, 디테일 |
| 135mm 이상 | 망원 | 강한 배경 압축 | 세부 디테일 |

- **로봇 제품 촬영 추천:** 50mm (전체) 또는 85mm (디테일 클로즈업)

#### Depth of Field (피사계 심도)

- Camera Properties > Depth of Field 체크박스 활성화
- **Focus Object:** 초점을 맞출 대상 오브젝트 선택 (Empty를 사용하면 편리)
- **Focus Distance:** 초점 거리를 수치로 직접 입력
- **F-Stop:** 조리개 값. 값이 작을수록 배경이 더 많이 흐려짐

| F-Stop | 효과 | 용도 |
|--------|------|------|
| 1.4~2.8 | 배경 강하게 흐림 | 제품 강조, 감성적 연출 |
| 4.0~5.6 | 적당한 배경 흐림 | 일반 제품 촬영 |
| 8.0~16 | 대부분 선명 | 전체 장면 촬영 |

- **팁:** 로봇 제품 강조 시 F-Stop 2.8, Focus Object를 로봇으로 설정

#### 카메라 애니메이션

- Camera를 선택한 상태에서 특정 프레임에서 I 키 > Location / Rotation 선택
- 다른 프레임으로 이동 후 Camera 위치/각도를 변경하고 다시 Keyframe 삽입
- Timeline에서 Keyframe 간격을 조절하여 카메라 이동 속도 제어
- **카메라 트래킹:** Track To Constraint를 사용하면 카메라가 항상 대상을 바라봄
  - Camera 선택 > Properties > Object Constraint > Add Constraint > Track To
  - Target에 로봇 오브젝트 설정

### 렌더 엔진 비교

Blender 5.0에서 제공하는 두 가지 주요 렌더 엔진을 비교합니다.

#### Eevee vs Cycles 비교 표

| 항목 | Eevee | Cycles |
|------|-------|--------|
| 렌더 방식 | 래스터화 (Rasterization) | 레이트레이싱 (Ray Tracing) |
| 렌더 속도 | 매우 빠름 (실시간) | 느림 (수 분~수 시간) |
| 품질 | 게임 수준, 충분히 좋음 | 사실적, 포토리얼 |
| 반사/굴절 | Screen Space 기반 (제한적) | 물리 기반 (정확) |
| 그림자 | Shadow Map 기반 | 레이트레이싱 기반 (부드러움) |
| 투명도 | Alpha Blend/Hashed | 물리 기반 투명도 |
| GI (글로벌 일루미네이션) | 제한적 | 정확한 간접광 |
| GPU 활용 | 빠름 | GPU 렌더링으로 가속 가능 |
| 추천 용도 | 실습, 프리뷰, 애니메이션 | 최종 렌더, 포트폴리오 |

#### Eevee 주요 설정

- **Render Properties > Render Engine > Eevee**
- **Sampling:**
  - Render Samples: 64~128 (높을수록 노이즈 감소, 속도 저하)
  - Viewport Samples: 16~32 (작업 중 프리뷰용)
- **Ambient Occlusion:**
  - Render Properties > Ambient Occlusion 체크
  - 오브젝트 사이 틈새에 자연스러운 그림자 추가
  - Distance 값으로 AO 범위 조절
- **Screen Space Reflections:**
  - Render Properties > Screen Space Reflections 체크
  - 반사 표면에 주변 환경이 비치는 효과
  - Refraction 체크: 투명 재질의 굴절 효과
- **Bloom:**
  - Render Properties > Bloom 체크
  - 밝은 부분에서 빛이 번지는 효과
  - Emission Material과 함께 사용하면 효과적
  - Threshold: 블룸이 시작되는 밝기 기준
  - Intensity: 블룸 강도

> **💡 프로 팁: Eevee 활용 전략**
> - Eevee는 **실시간 미리보기와 빠른 테스트 렌더**에 최적입니다. 조명/카메라 구도를 잡을 때는 Eevee로 빠르게 확인하고, 최종 고품질 렌더만 Cycles로 전환하세요.
> - Bloom + Emission Material 조합은 로봇의 LED 눈이나 발광 파츠를 표현할 때 매우 효과적입니다.

#### Cycles 주요 설정

- **Render Properties > Render Engine > Cycles**
- **Device:** GPU Compute 선택 (Edit > Preferences > System에서 GPU 설정)
  - CUDA (NVIDIA), HIP (AMD), Metal (Apple Silicon)
  - GPU가 없으면 CPU로 렌더 (매우 느림)
- **Sampling:**
  - Render Samples: 128~512 (일반적으로 256 권장)
  - Viewport Samples: 32~64
  - Adaptive Sampling: 노이즈가 적은 영역의 샘플을 자동으로 줄여 속도 향상
- **Denoising:**
  - Render Properties > Denoising 체크
  - Denoiser: OpenImageDenoise (OID) 권장
  - 낮은 샘플 수에서도 깨끗한 결과를 얻을 수 있음
  - 128 Samples + Denoising이 512 Samples보다 빠르면서 비슷한 품질
- **Light Paths:**
  - Max Bounces: 빛의 최대 반사 횟수 (기본 12, 실내 장면은 높이기)
  - Transparent Max Bounces: 투명 재질 반사 횟수

> **💡 프로 팁: Cycles 렌더 시간 최적화**
> - **128 Samples + Denoising(OpenImageDenoise)** 조합이 512 Samples보다 빠르면서 비슷한 품질을 제공합니다. 항상 Denoiser를 켜세요.
> - GPU Compute가 CPU보다 5~10배 빠릅니다. `Edit > Preferences > System`에서 GPU가 활성화되었는지 반드시 확인하세요.

### Blender 5.0 색상 관리

#### View Transform

- Render Properties > Color Management > View Transform에서 설정
- 렌더 결과의 색감과 톤을 결정하는 중요한 설정

| Transform | 설명 | 용도 |
|-----------|------|------|
| AgX | Blender 5.0 기본값, 권장 | 대부분의 작업 |
| Filmic | 이전 버전 기본값 | 레거시 프로젝트 호환 |
| Standard | 선형 색상 그대로 표시 | 데이터 시각화 |
| ACES | 영화 산업 표준 | VFX, 영화 워크플로우 |

#### AgX 장점

- **하이라이트 롤오프:** 밝은 부분이 자연스럽게 어두워지며 색상이 유지됨
- **색상 번짐 감소:** Filmic에서 발생하던 하이라이트 색상 왜곡이 줄어듦
- **넓은 다이나믹 레인지:** 어두운 부분과 밝은 부분 모두 디테일 유지
- **로봇 금속 재질:** 금속 반사 하이라이트가 자연스럽게 표현됨

#### Look 설정

- View Transform 하위에 Look 옵션
- **None:** 기본 (추가 보정 없음)
- **High Contrast:** 대비 강조 (극적인 조명에 적합)
- **Medium Contrast:** 중간 대비 (일반적인 제품 촬영)
- **Low Contrast:** 낮은 대비 (부드러운 분위기)

### 렌더 출력 설정

#### Resolution (해상도)

- Output Properties > Format > Resolution
- **1920 x 1080 (Full HD):** 기본 권장, 대부분의 용도에 적합
- **3840 x 2160 (4K):** 고해상도 포트폴리오용 (렌더 시간 4배)
- **1080 x 1080:** 인스타그램 정사각형 포맷
- **Resolution %:** 50%로 설정하면 절반 해상도로 빠른 테스트 가능

#### Frame Rate (프레임 레이트)

- Output Properties > Format > Frame Rate
- **24 fps:** 영화 표준, 시네마틱 느낌
- **30 fps:** 일반 영상, 웹 콘텐츠
- **60 fps:** 부드러운 움직임, 게임 트레일러

#### Output Format

- **이미지 렌더:**
  - PNG: 무손실, 투명도(Alpha) 지원, 파일 크기 큼
  - JPEG: 손실 압축, 파일 크기 작음, 투명도 미지원
  - EXR: HDR 이미지, 후처리(Compositing)에 적합
- **애니메이션 렌더:**
  - MP4 (FFmpeg): 일반 동영상, 공유에 적합
  - AVI: 무손실, 파일 크기 매우 큼
  - 이미지 시퀀스 (PNG): 가장 안전 (렌더 중단 시에도 기존 프레임 보존)

#### 렌더 실행

- **이미지 렌더:** F12 (현재 프레임 1장 렌더)
- **애니메이션 렌더:** Ctrl+F12 (모든 프레임 렌더)
- **렌더 결과 저장:** Image > Save As (F3)
- **렌더 취소:** Esc 키

### AI 영상 생성

#### Kling AI (klingai.com)

- **기능:** 이미지를 기반으로 비디오를 생성하는 AI 도구
- **무료 크레딧:** 회원가입 시 무료 크레딧 제공 (일일 갱신)
- **사용법:**
  1. Blender에서 렌더링한 이미지를 PNG/JPG로 저장
  2. klingai.com 접속 > AI Videos > Image to Video
  3. 렌더 이미지 업로드
  4. 프롬프트 입력 (영문):
     - "A cute robot slowly turning its head and waving"
     - "Camera orbiting around a sleek robot product on a white background"
     - "A robot's eyes lighting up with a gentle glow animation"
  5. Duration 선택 (5초 또는 10초)
  6. Generate 클릭 > 생성 완료 후 다운로드
- **팁:**
  - 프롬프트에 카메라 움직임 지정 가능: "camera slowly zooming in", "orbit shot"
  - 단순한 움직임일수록 결과가 자연스러움
  - 복잡한 로봇 구조보다는 전체 실루엣이 명확한 이미지가 좋은 결과를 냄

#### Veo (Google Gemini)

- **기능:** 텍스트 기반 비디오 생성 (Google AI)
- **접속:** Gemini 앱 또는 웹에서 Veo 기능 사용
- **사용법:**
  1. Gemini에게 영상 생성 프롬프트 입력
  2. 프롬프트 예시:
     - "A small white robot with blue LED eyes sitting on a desk, 4K cinematic lighting"
     - "Product showcase video of a futuristic robot, rotating on a turntable, studio lighting"
  3. 생성된 영상 다운로드
- **Kling AI와의 차이:**
  - Kling: 기존 이미지 기반 (렌더 이미지 활용 가능)
  - Veo: 텍스트만으로 새로운 영상 생성 (이미지 불필요)
  - 수업에서는 Kling AI를 주로 사용 (자신의 로봇 렌더 이미지를 활용하므로)

### AI 사운드/음악 생성

#### Suno AI (suno.com)

- **기능:** 텍스트 프롬프트로 음악을 생성하는 AI 도구
- **무료 크레딧:** 일일 무료 크레딧 제공 (약 5곡/일)
- **사용법:**
  1. suno.com 접속 > Create 클릭
  2. Song Description에 프롬프트 입력:
     - "cheerful electronic music for a robot product showcase, upbeat, 30 seconds"
     - "calm ambient music, futuristic, soft synth pads, technology feel, 1 minute"
     - "energetic pop rock, product launch, exciting, modern, 30 seconds"
  3. Create 클릭 > 2곡이 생성됨 (선택 가능)
  4. 마음에 드는 곡 다운로드 (MP3)
- **프롬프트 팁:**
  - 장르 지정: electronic, ambient, pop, cinematic, lo-fi 등
  - 분위기 지정: cheerful, calm, energetic, mysterious, futuristic
  - 용도 지정: product showcase, commercial, background music
  - 길이 지정: 30 seconds, 1 minute 등
- **주의:** Suno AI로 생성한 음악의 상업적 사용은 라이선스 확인 필요

#### ElevenLabs Music (elevenlabs.io)

- **기능:** AI 음악 생성 및 Sound Effects 생성
- **특징:**
  - 음악 생성: 텍스트 프롬프트로 배경음악 생성
  - Sound Effects: "robot servo motor sound", "futuristic UI beep" 등 효과음 생성
- **사용법:**
  1. elevenlabs.io 접속 > Sound Effects 또는 Music 기능 선택
  2. 프롬프트 입력:
     - 음악: "upbeat electronic background music for tech product video"
     - 효과음: "robot arm moving mechanical sound"
     - 효과음: "futuristic button click sound effect"
  3. Generate > 다운로드
- **Suno vs ElevenLabs:**
  - Suno: 음악(곡) 생성에 특화, 보컬 포함 가능
  - ElevenLabs: Sound Effects 생성에 강점, 짧은 효과음에 적합
  - 프로모션 영상에는 Suno BGM + ElevenLabs 효과음 조합 추천

### Compositor 기초

#### Compositor란?

- 렌더링 후 이미지/영상에 후처리(Post-Processing) 효과를 적용하는 도구
- Photoshop 필터와 비슷한 개념이지만 노드 기반으로 동작
- 노드를 연결하여 다양한 효과를 조합

#### Compositor 사용법

1. 상단 Workspace에서 Compositing 탭 선택
2. "Use Nodes" 체크 (활성화)
3. 기본 구성: Render Layers -> Composite
4. 중간에 효과 노드를 추가하여 후처리

#### 주요 Compositor 노드

- **Glare (빛 번짐):**
  - Add > Filter > Glare
  - Fog Glow: 전체적으로 부드러운 빛 번짐
  - Streaks: 별 모양 빛 갈래
  - 로봇의 Emission 파츠(눈, LED)에 효과적
- **Color Balance:**
  - Add > Color > Color Balance
  - Lift (어두운 톤), Gamma (중간 톤), Gain (밝은 톤) 조절
  - 영화적 색보정에 활용
- **Denoise:**
  - Add > Filter > Denoise
  - Cycles 렌더의 노이즈를 후처리로 제거
  - Render Layers의 Denoising Data 출력 연결
- **Lens Distortion:**
  - Add > Distortion > Lens Distortion
  - 실제 카메라 렌즈의 왜곡을 시뮬레이션
  - Dispersion 값을 올리면 색수차(Chromatic Aberration) 효과

> **💡 프로 팁: Compositor 후보정 활용**
> - Compositor에서 **Glare(Fog Glow)** 노드를 추가하면 로봇의 Emission 파츠에 자연스러운 빛 번짐 효과를 줄 수 있습니다.
> - **Color Balance** 노드로 영화적 색감 보정(시네마틱 톤)을 쉽게 적용할 수 있습니다. Lift를 약간 푸르게, Gain을 약간 따뜻하게 설정하면 시네마틱 룩이 됩니다.

#### Blender 5.0 Compositor 업데이트

- Compositor Modifier가 Video Sequencer에서도 사용 가능
- Sequencer에서 영상 편집 중 직접 Compositor 효과를 적용할 수 있음
- 별도의 Compositor Workspace를 오가지 않아도 됨

#### Blender 5.0 렌더링 성능 향상

> **🆕 Blender 5.0 주요 개선사항:**
> - **Material 컴파일 속도 최대 4배 향상:** NVIDIA GPU + Vulkan 백엔드 조합에서 Material 컴파일이 크게 빨라졌습니다. 복잡한 Shader가 많은 씬에서 체감 효과가 큽니다.
> - **Compositor Asset Shelf:** 자주 사용하는 Compositor 노드 조합을 Asset으로 저장하고 재사용할 수 있습니다. Glare + Color Balance 같은 자주 쓰는 후보정 세트를 한 번 만들어두면 다른 프로젝트에서도 드래그 앤 드롭으로 적용 가능합니다.
> - **Eevee 품질 향상:** Blender 5.0의 Eevee는 이전 버전 대비 반사/그림자 품질이 크게 개선되어, 간단한 프로젝트에서는 Cycles 없이도 충분한 품질을 얻을 수 있습니다.

### MCP 활용: 카메라/렌더 자동화

#### MCP (Model Context Protocol) 복습

- Claude Desktop에서 Blender를 제어하는 MCP 서버를 통해 자동화 가능
- 반복적인 카메라 배치, 렌더 설정 등을 자연어 명령으로 처리

#### 카메라 설정 자동화 프롬프트

Claude에게 다음과 같은 프롬프트를 사용할 수 있습니다:

- **카메라 위치/각도 설정:**
  - "Set camera to a 45 degree angle looking at the origin with focal length 50mm"
  - "Move the camera to position (5, -5, 3) and point it at the robot"
  - "Create three cameras: front view, side view, and top-down view"

- **Depth of Field 설정:**
  - "Enable depth of field with f-stop 2.8 focusing on the robot"
  - "Set focus distance to 3 meters with f-stop 4.0"

- **렌더 설정:**
  - "Set render engine to Eevee with 128 samples and enable bloom"
  - "Switch to Cycles with GPU rendering, 256 samples, and enable denoising"
  - "Set render resolution to 1920x1080 at 100%"

- **렌더 실행:**
  - "Render the current scene at 1920x1080"
  - "Set output path to //renders/ and render the animation"

#### 여러 앵글 자동 렌더 예시

Claude에게 한 번에 요청:

```
Create 3 cameras for my robot product:
1. Front hero shot at 45 degrees, focal length 50mm, f-stop 2.8
2. Close-up of the head area, focal length 85mm, f-stop 1.8
3. Low angle dramatic shot, focal length 35mm, f-stop 5.6
Set render engine to Eevee with bloom enabled and render each camera view.
```

이런 식으로 여러 카메라 앵글을 한 번에 설정하고 렌더까지 자동화할 수 있습니다.

## 실습 (80분)

### Camera 배치 및 설정 (10분)

1. 자신의 로봇/캐릭터 모델이 있는 씬 열기
2. Shift+A > Camera 추가
3. Camera를 선택하고 위치/각도를 조정:
   - 위치: 로봇 정면에서 약간 위, 대각선 방향
   - 예시 좌표: Location (4, -4, 3), Rotation (60, 0, 45)
4. Numpad 0으로 Camera 뷰 확인
5. Camera Properties에서 설정:
   - Focal Length: 50mm
   - Depth of Field: 체크
   - Focus Object: 로봇 오브젝트 선택
   - F-Stop: 2.8
6. Camera 뷰에서 로봇이 적절한 구도로 보이는지 확인
7. 필요하면 Ctrl+Alt+Numpad 0으로 현재 뷰를 Camera 뷰로 설정

### Eevee 렌더 테스트 (10분)

1. Render Properties > Render Engine > **Eevee** 선택
2. Sampling 설정:
   - Render Samples: 128
3. 추가 설정 활성화:
   - Ambient Occlusion: 체크
   - Screen Space Reflections: 체크
   - Bloom: 체크 (Emission Material이 있는 경우 효과적)
4. Color Management 확인:
   - View Transform: AgX (기본값)
   - Look: Medium Contrast
5. Output Properties에서 해상도 확인:
   - Resolution: 1920 x 1080
   - Resolution %: 100%
6. **F12**를 눌러 렌더 실행
7. 렌더 결과 확인 후 **Image > Save As**로 저장
   - 파일명 예시: `robot_eevee_render.png`

### Cycles 렌더 비교 (10분)

1. Render Properties > Render Engine > **Cycles** 변경
2. Device 설정:
   - GPU Compute 선택 (Edit > Preferences > System에서 GPU 확인)
   - Apple Silicon의 경우 Metal 선택
3. Sampling 설정:
   - Render Samples: 128
   - Denoising: 체크, Denoiser: OpenImageDenoise
4. **F12**를 눌러 렌더 실행
5. Eevee 렌더와 비교:
   - 그림자의 부드러움 차이
   - 반사/굴절의 정확도 차이
   - 전체적인 톤과 분위기 차이
6. 렌더 결과 저장
   - 파일명 예시: `robot_cycles_render.png`
7. 두 이미지를 나란히 비교하여 차이점 확인

### MCP로 카메라/렌더 자동화 (10분)

1. Claude Desktop 열기 (MCP 서버가 연결된 상태)
2. 다음 프롬프트를 Claude에게 입력:

```
내 Blender 씬에 3가지 카메라 앵글을 설정해줘:
1. 정면 45도 각도, focal length 50mm, f-stop 2.8
2. 머리 부분 클로즈업, focal length 85mm, f-stop 1.8
3. 낮은 각도 드라마틱 샷, focal length 35mm, f-stop 5.6
렌더 엔진은 Eevee, Bloom 켜줘.
```

3. Claude가 자동으로 카메라를 생성하고 설정하는 것을 확인
4. 각 카메라 뷰에서 Numpad 0으로 확인
5. 마음에 드는 앵글을 선택하여 렌더

### AI 영상 생성 - Kling AI (15분)

1. 가장 마음에 드는 렌더 이미지 1장 선택 (PNG 또는 JPG)
2. 웹 브라우저에서 **klingai.com** 접속
3. 로그인 (Google 계정으로 간편 로그인 가능)
4. AI Videos > **Image to Video** 선택
5. 렌더 이미지 업로드
6. 프롬프트 작성 (영문):
   - 예시 1: "A cute robot slowly turning its head left and right, studio lighting"
   - 예시 2: "Camera slowly orbiting around the robot product, soft shadows"
   - 예시 3: "The robot's eyes gently glowing and pulsing with blue light"
7. 설정:
   - Duration: 5초 (처음에는 짧게 테스트)
   - Mode: Standard (무료 크레딧으로 이용 가능)
8. **Generate** 클릭
9. 생성 완료까지 대기 (약 2~5분)
10. 결과 확인 후 다운로드
11. 마음에 들지 않으면 프롬프트를 수정하여 재생성

### AI BGM 생성 - Suno AI (15분)

1. 웹 브라우저에서 **suno.com** 접속
2. 로그인 (Google 계정)
3. **Create** 클릭
4. Song Description에 프롬프트 입력:
   - 예시 1: "cheerful electronic music for a robot product showcase, upbeat, modern synth, 30 seconds"
   - 예시 2: "calm ambient background music, futuristic technology feel, soft pads, 1 minute"
   - 예시 3: "energetic cinematic trailer music, epic drums, synthesizer, product launch, 30 seconds"
5. **Create** 클릭 > 2개의 곡이 생성됨
6. 각 곡을 재생하여 청취
7. 마음에 드는 곡 선택 후 다운로드 (MP3)
8. (선택) ElevenLabs에서 효과음도 생성해보기:
   - "robot servo motor whirring sound"
   - "futuristic UI notification chime"

### 영상 조합 (10분)

생성한 AI 영상과 BGM을 간단히 합칩니다.

#### 방법 1: Blender Video Sequencer (기본)

1. 새로운 Blender 파일 열기 또는 상단 Workspace에서 **Video Editing** 선택
2. Sequencer에서 **Add > Movie** > AI 생성 영상 파일 로드
3. **Add > Sound** > AI 생성 BGM 파일 로드
4. 영상과 음악의 길이를 맞추기 (Strip 끝을 드래그하여 조절)
5. Ctrl+F12로 최종 영상 렌더

#### 방법 2: 외부 편집기 (간편)

- **CapCut (무료):** 드래그 앤 드롭으로 영상+음악 조합, 자막 추가
- **DaVinci Resolve (무료):** 전문적인 영상 편집 가능
- 외부 편집기가 더 익숙하다면 사용해도 무방

#### 최종 결과물 확인

- AI 영상 위에 BGM이 자연스럽게 깔리는지 확인
- 음악 볼륨이 적절한지 확인
- 최종 영상 파일로 Export

## ⚠️ 흔한 실수와 해결법

### 실수 1: Eevee에서 투명/반사가 안 보임

- **증상:** 유리 재질이 불투명하게 보이거나, 금속 반사에 주변 환경이 비치지 않음
- **원인:** Eevee의 Screen Space Reflection/Refraction이 비활성화 상태
- **해결:**
  - `Render Properties > Screen Space Reflections` 체크
  - 하위의 `Refraction` 체크박스도 활성화
  - 투명 재질의 Material Properties > Settings > Screen Space Refraction 체크
  - Blend Mode를 Alpha Blend 또는 Alpha Hashed로 변경

### 실수 2: 렌더 시간이 너무 길음

- **증상:** Cycles 렌더가 한 장에 수십 분 이상 걸림
- **원인:** Sample 수가 너무 높거나, Denoiser를 사용하지 않거나, CPU로 렌더 중
- **해결:**
  - Render Samples를 128~256으로 줄이고 **Denoising(OpenImageDenoise)** 활성화
  - `Edit > Preferences > System`에서 GPU Compute 활성화 확인
  - 테스트 렌더 시 Resolution %를 50%로 낮추기
  - 불필요한 오브젝트는 Outliner에서 렌더 제외 (카메라 아이콘 끄기)

### 실수 3: 영상 렌더 시 프레임이 빠짐

- **증상:** 렌더링된 영상에서 특정 프레임이 누락되거나 검은 화면이 나옴
- **원인:** Output 설정에서 Frame Range가 잘못되었거나, 파일 경로에 문제가 있음
- **해결:**
  - `Output Properties > Frame Range`에서 Start/End 프레임이 올바른지 확인
  - Output Path가 존재하는 폴더인지 확인 (폴더가 없으면 렌더 실패)
  - 애니메이션 렌더 시 **이미지 시퀀스(PNG)**로 출력하는 것을 권장 (렌더 중단 시에도 기존 프레임 보존)
  - 이미지 시퀀스를 나중에 Video Sequencer에서 합치면 안전

### 실수 4: 메모리 부족으로 렌더 실패

- **증상:** Cycles 렌더 시 "Out of memory" 오류 또는 Blender 크래시
- **원인:** GPU 메모리(VRAM)가 부족하여 텍스처와 씬 데이터를 처리하지 못함
- **해결:**
  - 텍스처 해상도 줄이기: 4096x4096 텍스처를 2048x2048 또는 1024x1024로 축소
  - `Render Properties > Performance > Memory`에서 Tile Size 조정
  - Subdivision Modifier의 Render Level 낮추기
  - 최후 수단: GPU 대신 CPU로 렌더 (느리지만 시스템 메모리를 활용 가능)

### 실수 5: 렌더 결과 색감이 이상함

- **증상:** Viewport에서 보던 색감과 렌더 결과가 다르게 보임
- **원인:** Color Management 설정이 다르거나, View Transform이 적절하지 않음
- **해결:**
  - `Render Properties > Color Management > View Transform`을 **AgX**로 설정 (Blender 5.0 기본값)
  - Look 설정을 Medium Contrast로 변경하여 확인
  - Viewport Shading의 Color Management와 렌더 설정이 일치하는지 확인

## Notion 참고 자료

수업 Notion 페이지에서 다음 자료를 추가로 참고하세요:

- **Rendering:** 렌더 엔진별 세부 설정 가이드
- **Camera Setting:** 카메라 타입별 활용법
- **Render & Export:** 출력 포맷별 장단점
- **Eevee 문제해결:** Eevee 렌더 시 발생하는 일반적인 문제와 해결법

## 핵심 정리

| 개념 | 핵심 |
|------|------|
| Eevee | 빠른 실습용 렌더, Bloom/AO/SSR로 품질 향상 |
| Cycles | 고품질 최종본, GPU + Denoising으로 속도 최적화 |
| AgX | Blender 5.0 기본 색상 관리, 자연스러운 하이라이트 |
| Kling AI | 렌더 이미지 -> AI 비디오 변환 |
| Suno AI | 텍스트 프롬프트 -> BGM 음악 생성 |
| ElevenLabs | 효과음/짧은 음악 생성 |
| MCP | 카메라/렌더 설정 자연어 자동화 |

- **Eevee = 빠른 실습용**, Cycles = 고품질 최종본
- **AI 영상/음악은 프로모션 컨텐츠의 가능성을 확장**한다
- **MCP로 반복적인 렌더 설정을 자동화**하여 효율적으로 여러 앵글 렌더 가능
- 렌더링은 최종 결과물의 품질을 결정하는 중요한 단계

## 📋 프로젝트 진행 체크리스트

이번 주차 실습이 끝나면 아래 항목을 확인하세요:

- [ ] Camera를 배치하고 Focal Length, Depth of Field를 설정하였는가
- [ ] Eevee로 테스트 렌더를 완료하고 이미지를 저장하였는가
- [ ] Cycles로 최종 렌더를 완료하고 이미지를 저장하였는가
- [ ] Eevee vs Cycles 렌더 결과의 차이를 비교/이해하였는가
- [ ] AI 영상 생성 (Kling AI)을 시도하고 결과물을 다운로드하였는가
- [ ] AI BGM 생성 (Suno AI)을 시도하고 음악 파일을 다운로드하였는가
- [ ] 영상과 BGM을 조합하여 프로모션 영상 초안을 만들었는가
- [ ] (기말 프로젝트 대비) 최종 렌더 이미지가 1920x1080 이상인가

> **기말 프로젝트 진행률 체크:** 이 시점에서 기말 프로젝트의 약 **70%가 완료**되어 있어야 합니다.
> - 모델링/텍스처/리깅 완료
> - 애니메이션 1개 이상 완성
> - 렌더 이미지 3장 이상 확보
> - AI 영상/사운드 소재 확보
>
> 부족한 부분이 있다면 Week 14 피드백 시간 전까지 반드시 보충하세요.

## 다음 주 예고

**Week 14: 최종 프로젝트 제작**

- 최종 프로젝트 본격 제작 시작
- 지금까지 배운 모든 기술 (모델링, 텍스처, 리깅, 애니메이션, 렌더링, AI 도구)을 종합
- 각자의 로봇 프러덕트를 완성하고 프로모션 영상까지 제작
- 이번 주 렌더링과 AI 영상/음악 실습이 최종 프로젝트의 핵심 기반이 됩니다!
