---
marp: true
theme: rpd
paginate: true
---

# Week 10: Animation 기초

## 로봇프러덕트 디자인

2026 Spring | 인하대학교 | 송지희

---

## 애니메이션 원리: 12 Principles 중 핵심 4가지

**1. Squash & Stretch (압축과 늘림)**
- 힘에 의해 형태가 변형, 부피는 유지
- 예: 공이 바닥에 닿으면 납작해짐

**2. Anticipation (예비 동작)**
- 주 동작 전에 반대 방향으로 작은 동작
- 예: 점프 전 무릎 굽히기

**3. Ease In / Ease Out (가감속)**
- 시작과 끝에서 속도가 변함, 선형 움직임은 부자연스러움

**4. Timing (타이밍)**
- 프레임 수에 따라 무게감과 성격이 달라짐

---

## Timeline 기초

**Timeline:** Blender 하단의 시간 제어 패널

- **프레임 (Frame):** 시간의 최소 단위
- **Playhead:** 현재 프레임 위치 (파란 세로선)
- **Keyframe 마커:** 속성값이 기록된 프레임 (노란 다이아몬드)

**FPS 설정 (Output Properties > Frame Rate):**
- 24fps: 영화 표준 (이 수업에서 권장)
- 30fps: 게임/웹 표준

**프레임 범위:**
- 3초 = 72프레임 (24fps), 5초 = 120프레임

---

## Keyframe이란?

- 특정 프레임에 **오브젝트의 속성값을 기록**하는 것
- 두 Keyframe 사이의 값은 Blender가 **자동으로 보간**

**삽입:** 오브젝트 선택 > 원하는 프레임 이동 > **I** 키
- Location (위치)
- Rotation (회전)
- Scale (크기)
- LocRotScale (모두)

**삭제:** **Alt+I** 또는 Timeline에서 선택 후 X

**Auto Keying:** Timeline의 빨간 원 버튼 (자동 Keyframe)

---

## Keyframe 워크플로우

**기본 워크플로우:**
1. 프레임 1로 이동 → 초기 위치 설정 → **I** > Location
2. 프레임 24로 이동 → 최종 위치 설정 → **I** > Location
3. Space로 재생하여 확인
4. Graph Editor에서 이징 조절

**Keyframe이 삽입되면:**
- Properties 필드가 **노란색**으로 변함
- Timeline에 **노란 다이아몬드** 마커 표시
- 현재 값이 Keyframe 값과 다르면 **초록색**으로 변함

---

## Graph Editor

- Keyframe 사이의 **보간 커브**를 시각적으로 편집
- Editor Type > **Graph Editor**로 전환

| 보간 모드 | 특징 | 적합한 경우 |
|-----------|------|------------|
| **Bezier** | 부드러운 S커브 | 자연스러운 움직임 |
| **Linear** | 일정한 속도 직선 | 기계적 움직임 |
| **Constant** | 갑작스러운 전환 | On/Off 스위치 |

**이징 변경:** Keyframe 선택 > **T** 키

---

## 이징 프리셋

| 프리셋 | 효과 | 사용 예시 |
|--------|------|-----------|
| **Ease In** | 느리게 시작 → 빨라짐 | 물체 낙하 (중력 가속) |
| **Ease Out** | 빠르게 시작 → 느려짐 | 멈추는 동작 (감속) |
| **Back** | 목표를 넘었다 돌아옴 | 과장된 만화적 표현 |
| **Bounce** | 공 튀듯 반복 감속 | 착지, 물체 떨어짐 |
| **Elastic** | 고무줄 같은 늘어남 | 탄성 있는 재질 표현 |

**핸들 조절:** V 키로 핸들 타입 변경 (Auto, Vector, Free 등)

---

## 재생 관련 단축키

| 단축키 | 동작 |
|--------|------|
| **Space** | 재생 / 일시정지 |
| **Left / Right Arrow** | 1프레임 이동 |
| **Up / Down Arrow** | 10프레임 이동 |
| **Shift+Left** | 시작 프레임으로 이동 |
| **Shift+Right** | 끝 프레임으로 이동 |
| **I** | Keyframe 삽입 |
| **Alt+I** | Keyframe 삭제 |

---

## 실습 1: 공 바운스 애니메이션

**Squash & Stretch의 핵심을 체득하는 기본 실습**

1. UV Sphere + Plane (바닥) 준비
2. 24fps, 72프레임 (3초) 설정
3. Keyframe 삽입 (Z축 위치):
   - 프레임 1: Z=5 (높이)
   - 프레임 12: Z=0.5 (바닥) ← Squash 적용
   - 프레임 24: Z=3 (첫 바운스)
   - 프레임 36: Z=0.5 (바닥) ← Squash
   - 프레임 48: Z=1.5 (두 번째 바운스)
4. 바닥 닿을 때 Scale Z=0.6, XY=1.3 (납작하게)
5. Graph Editor에서 낙하=Ease In, 상승=Ease Out

---

## 실습 2: 로봇 머리 회전

**좌우 둘러보기 동작**

1. 머리 오브젝트 분리 (필요 시 P > Selection)
2. 120프레임 (5초) 설정
3. Rotation Z Keyframe:
   - 프레임 1: 정면 (0도)
   - 프레임 24: 왼쪽 (45도)
   - 프레임 48: 정면 (0도)
   - 프레임 72: 오른쪽 (-45도)
   - 프레임 96: 정면 (0도)
4. Bezier 이징 적용
5. 방향 전환 지점에 약간의 멈춤(hold) 추가

---

## 실습 3: 로봇 팔 올리기/내리기

**Origin Point 설정이 핵심!**

1. 팔의 Origin Point를 **어깨 관절**로 이동:
   - Edit Mode에서 어깨 vertex 선택
   - Shift+S > Cursor to Selected
   - Object Mode > Set Origin > Origin to 3D Cursor
2. Rotation X Keyframe:
   - 프레임 1: 팔 내림 (0도)
   - 프레임 12: Anticipation (10도, 살짝 뒤로)
   - 프레임 36: 팔 올림 (-90도)
   - 프레임 72: 팔 내림 (0도)
3. 올리기: Ease Out / 내리기: Ease In (중력)

---

## 실습 4: Graph Editor 이징 비교

**같은 동작, 다른 이징 → 전혀 다른 느낌**

- **Linear:** 기계적, 딱딱한 (로봇 정밀 동작에 적합)
- **Bezier:** 부드럽고 자연스러운 (대부분의 애니메이션)
- **Back:** 과장된 오버슈트 (만화적 표현)
- **Bounce:** 공 튀는 착지 (물리적 반동)

**팁:** 여러 동작을 같은 Timeline에 배치할 때
시작 시점을 **약간 어긋나게(offset)** 하면 더 자연스러움

---

## 과제 안내

- **제출처:** Discord #week10-assignment 채널
- **내용:**
  - 3~5초 분량의 간단한 움직임 애니메이션
  - 손 흔들기, 고개 돌리기, 점프 등 자유 선택
  - MP4 영상 또는 GIF 파일 + 한줄 코멘트
- **평가:**
  - 자연스러운 움직임 40%
  - Keyframe/이징 활용 30%
  - 창의성 30%

---

## 다음 주: Camera + 렌더링 기초

**Week 11: Camera + 렌더링 기초**

- 카메라 설정과 구도 (Camera Properties)
- 렌더 엔진 비교: Eevee vs Cycles
- 렌더 출력 설정 (해상도, 포맷)
- 애니메이션 렌더 및 영상 출력

이제 조명과 애니메이션을 합쳐서 완성된 영상을 만들어 봅시다!
