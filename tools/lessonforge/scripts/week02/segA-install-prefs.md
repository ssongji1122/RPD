# Week 02 · Seg A — 설치 & 환경설정

**목표 영상 길이:** 7분
**레퍼런스:** 차녹 0:00~0:42 / Blender Guru Part 1 도입부 + preferences
**촬영 도구:** screen_record (브라우저 + Blender Preferences)
**RPD 연결:** "지금 설치하는 이 프로그램으로 여러분의 캐릭터 로봇을 만들 거예요"

> **핵심 메시지:** 설치와 설정을 한 번에 처리. 이유를 먼저 설명하고 방법을 알려준다 (Blender Guru 원칙).

---

## 화면 큐 (Screen Cues)

| 타임 | 화면 | 나레이션 큐 |
|------|------|------------|
| 0:00 | 타이틀 슬라이드 | 인트로 |
| 0:20 | 브라우저 → blender.org/download | 다운로드 |
| 1:00 | Mac .dmg / Windows .msi 설치 화면 | 설치 (빠르게) |
| 2:00 | Blender 첫 실행 → Splash Screen → General 클릭 | 첫 실행 |
| 2:30 | Edit > Preferences 열기 | Preferences 진입 |
| 3:00 | System 탭 → GPU Compute | GPU 설정 (이유 먼저) |
| 4:30 | Input 탭 → Emulate Numpad 체크 | 노트북 필수 |
| 5:30 | Interface 탭 → Resolution Scale | 고해상도 대응 |
| 6:00 | Save Preferences 클릭 강조 | 저장 |
| 6:30 | 아웃트로 슬라이드 | 마무리 |

---

## TTS 나레이션 스크립트

### [인트로 — 0:00]
이번 영상에서는 Blender 5.0을 설치하고, 바로 기본 환경설정까지 잡겠습니다.
설치는 딱 한 번, 설정도 딱 한 번. 같이 해봅시다.

### [다운로드 — 0:20]
브라우저에서 **blender.org** 로 이동합니다. 상단 Download 메뉴를 클릭하세요.
Blender는 완전 무료 오픈소스입니다.

지금 보이는 버전이 **Blender 5.0** 이에요. 항상 페이지 가장 위에 있는 최신 버전을 받으면 됩니다.

여러분의 운영체제에 맞는 버튼을 클릭하세요.
맥이라면 macOS, 윈도우라면 Windows.
Apple Silicon, 즉 M1·M2·M3 맥이라면 **macOS Apple Silicon** 버전을 꼭 받으세요.

### [설치 — 1:00]
다운로드가 끝나면 설치합니다.

**Mac**: .dmg 파일을 열고, Blender 아이콘을 Applications 폴더로 드래그. 끝이에요.
**Windows**: .msi 파일 실행 → Next → Next → Install → Finish. 기본값 그대로 진행하면 됩니다.

### [첫 실행 — 2:00]
Blender를 실행해볼게요.
처음 열면 **Splash Screen** 이 나타납니다. 여기서 **General** 을 클릭하면
기본 씬이 열립니다. 큐브, 카메라, 조명이 있는 이 화면이 Blender의 기본 상태예요.

복잡해 보이지만 걱정하지 마세요. 이 화면은 다음 영상에서 하나씩 설명할게요.

### [Preferences 열기 — 2:30]
설치가 됐으면 바로 환경설정을 잡겠습니다.
상단 메뉴에서 **Edit → Preferences** 를 클릭합니다.

### [GPU 설정 — 3:00]
먼저 **System** 탭으로 이동합니다.
여기서 가장 중요한 설정이 **GPU Compute** 예요.

왜 중요하냐면, 렌더링을 GPU로 하면 CPU 대비 10배에서 50배까지 빠릅니다.
나중에 로봇 렌더링할 때 이 차이가 크게 납니다.

- **NVIDIA GPU** 사용자: CUDA 또는 OptiX 항목에서 GPU 체크
- **Apple Silicon(M1·M2·M3)** 사용자: Metal 항목에서 GPU 체크
- **내장 그래픽만** 있는 경우: 해당 항목이 없을 수 있어요. 그래도 괜찮습니다

### [Emulate Numpad — 4:30]
**Input** 탭을 클릭합니다.
**Emulate Numpad** 를 체크하세요.

Blender는 뷰포트 조작에 키보드 오른쪽 숫자패드를 많이 씁니다.
그런데 노트북에는 Numpad가 없죠.
이 옵션을 체크하면 키보드 상단 숫자 키 1·3·7 이 Numpad처럼 작동합니다.
노트북이 아닌 분도 체크해두면 편합니다.

### [Resolution Scale — 5:30]
**Interface** 탭으로 이동합니다.
고해상도 모니터, 즉 Retina나 4K를 쓰신다면 **Resolution Scale** 을 1.2~1.5로 올려보세요.
아이콘과 텍스트가 더 크게 보입니다.
일반 1080p 모니터라면 기본값 1.0으로 두면 됩니다.

### [저장 — 6:00]
마지막으로 왼쪽 하단 **Save Preferences** 를 꼭 클릭하세요.
이걸 안 누르면 다음에 블렌더를 다시 열었을 때 설정이 다 초기화됩니다.
꼭 저장해주세요.

### [아웃트로 — 6:30]
설치 완료, 환경설정 완료.
- GPU 활성화
- Emulate Numpad 체크
- Save Preferences 저장

다음 영상에서는 Blender 화면 구조와 뷰포트 조작을 배웁니다.
어디에 무엇이 있는지 파악하면 나머지 수업이 훨씬 쉬워져요.

---

## 촬영 체크리스트

- [ ] 브라우저 북마크바 숨김 (깔끔한 화면)
- [ ] Mac / Windows 설치 화면 모두 캡처
- [ ] Blender virgin 상태 (기존 config 삭제 후 첫 실행)
- [ ] GPU 설정 항목 강조 (화살표 또는 빨간 원)
- [ ] Save Preferences 버튼 클릭 순간 강조

## 편집 메모

- 다운로드 대기 구간은 x2 배속 처리
- Mac / Windows 설치는 화면 분할 또는 순차 편집
- GPU 설정: "왜?"를 먼저 설명하는 Blender Guru 스타일 유지
