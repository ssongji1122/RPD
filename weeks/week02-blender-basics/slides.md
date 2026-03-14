---
marp: true
theme: rpd
paginate: true
---

# Week 02: Blender 인터페이스 및 기초

## + MCP 설정

2026 Spring | 인하대학교 | 송지희

---

## Blender 5.0 UI 구조

- **3D Viewport:** 메인 작업 영역, 오브젝트 조작 및 결과 확인
- **Outliner:** 씬 계층 구조 관리, 가시성 및 선택 제어
- **Properties Panel:** 오브젝트/재질/렌더 세부 설정
- **Timeline:** 애니메이션 키프레임 관리

---

## Blender 5.0 변경사항

- **Pill 형태 탭:** 기존 직사각형 탭에서 둥근 pill 형태로 변경
- **Workspace 통합:** Compositing/Rendering이 General Workspace로 통합
- **아이콘 개선:** 전반적인 아이콘 및 레이아웃 현대화
- 기능은 동일하되 접근성이 향상됨

---

## 뷰 조작: 기본

| 조작 | 단축키 |
|------|--------|
| 회전 | Middle Mouse Button |
| 이동 | Shift + Middle Mouse |
| 줌 | Scroll Wheel |

- 노트북 사용자: Edit > Preferences > Input > Emulate 3 Button Mouse 활성화

---

## 뷰 전환: Numpad

| 뷰 | 단축키 |
|------|--------|
| 정면 (Front) | Numpad 1 |
| 측면 (Right) | Numpad 3 |
| 상면 (Top) | Numpad 7 |
| 원근/직교 전환 | Numpad 5 |
| 카메라 뷰 | Numpad 0 |

- Numpad가 없는 경우: Preferences > Input > Emulate Numpad 활성화

---

## Shading 모드 (Z 키)

Z 키를 누르면 Pie Menu가 나타남

- **Wireframe:** 와이어프레임만 표시, 구조 확인용
- **Solid:** 기본 음영, 일반 작업 시 사용
- **Material Preview:** 재질 + HDRI 환경 미리보기
- **Rendered:** 실시간 렌더링 결과 확인

---

## Transform: G / R / S

- **G (Grab):** 오브젝트 이동
- **R (Rotate):** 오브젝트 회전
- **S (Scale):** 오브젝트 크기 변경

공통 조작:
- 마우스 이동으로 방향/크기 결정
- Left Click으로 확정, Right Click 또는 Esc로 취소

---

## 축 제한과 숫자 입력

**축 제한:**
- G + X / G + Y / G + Z: 해당 축으로만 이동
- R + X / R + Y / R + Z: 해당 축을 기준으로만 회전
- S + X / S + Y / S + Z: 해당 축으로만 스케일

**숫자 입력:**
- G + X + 2 + Enter: X축으로 2미터 이동
- R + Z + 45 + Enter: Z축 기준 45도 회전
- S + 0.5 + Enter: 크기를 절반으로 축소

---

## Apply Transform이 중요한 이유

**적용 전 문제:**
- Scale이 (2, 1, 1)처럼 남아 있으면 모델링 비율 왜곡
- 리깅 시 뼈대가 올바르게 동작하지 않음
- FBX/glTF 내보내기 시 크기/회전 오류 발생

**적용 방법:**
- Ctrl + A > Apply All Transforms
- Location (0,0,0), Rotation (0,0,0), Scale (1,1,1)로 초기화
- 모델링/리깅/내보내기 전에 반드시 실행

---

## Origin 설정

**Origin이란?**
- 오브젝트의 기준점 (주황색 점)
- 이동, 회전, 스케일의 중심

**설정 방법 (Right-click > Set Origin):**
- Origin to Geometry: 메시 중심으로 이동
- Origin to 3D Cursor: 3D Cursor 위치로 이동
- Origin to Center of Mass: 질량 중심으로 이동

---

## Pivot Point

Header 바에서 변경 가능

- **Individual Origins:** 각 오브젝트 자체 Origin 기준
- **3D Cursor:** 3D Cursor 위치 기준
- **Median Point:** 선택된 오브젝트들의 중간점 기준
- **Active Element:** 마지막 선택 오브젝트 기준

활용: 여러 오브젝트를 한 점을 중심으로 회전시킬 때 유용

---

## 실습: Blender MCP 설치

**Blender MCP란?**
- Blender와 AI(Claude)를 연결하는 프로토콜
- 자연어 명령으로 Blender를 제어 가능

**설치 순서:**
1. Blender MCP Add-on 설치 및 활성화
2. Claude Desktop/Code에서 MCP 서버 연결
3. Blender 측에서 MCP 서버 시작

---

## MCP 연결 테스트

**기본 테스트:**
- "Create a sphere at origin"

**응용 테스트:**
- "Create a red cube, a blue sphere, and a green cylinder arranged in a row"

**확인 사항:**
- Blender에서 오브젝트가 자동으로 생성되는지 확인
- 오류 발생 시 콘솔 로그 확인

---

## 과제 안내

- **제출처:** Discord #week02-assignment 채널
- **내용:**
  - 스크린샷 1: 기본 도형 5개 이상을 배치한 씬
  - 스크린샷 2: Blender MCP 연결 테스트 성공 화면
  - 한줄 코멘트
- **평가:** 도구 활용 40% / 완성도 30% / 창의성 30%

---

## 다음 주 예고

**Week 03: 기초 모델링 1 - Edit Mode**

- Object Mode vs Edit Mode
- Extrude, Loop Cut, Inset, Bevel 도구
- 기본 도형에서 로봇 형태 만들기
