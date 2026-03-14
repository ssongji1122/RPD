# Week 03: 기초 모델링 1 - Edit Mode

## 학습 목표

- [ ] Edit Mode의 3가지 선택 모드를 이해한다
- [ ] Extrude, Loop Cut, Inset, Bevel 도구를 사용할 수 있다
- [ ] 기본 도형에서 로봇 형태를 만들 수 있다

## 🔗 이전 주차 복습

- Week 02에서 배운 **Transform (G, R, S)**과 **축 제한**을 Edit Mode에서도 동일하게 사용한다
- **Apply Transform (Ctrl + A)**을 Edit Mode 진입 전에 반드시 적용했는지 확인
- **뷰 전환 (Numpad 1, 3, 7)**으로 정면/측면/상면을 오가며 작업하는 습관 유지
- MCP를 활용하여 기본 도형 배치를 자동화할 수 있음 (복습 겸 활용)

## 이론 (30분)

### Object Mode vs Edit Mode

- **Object Mode:** 오브젝트 단위로 이동, 회전, 스케일 등을 수행하는 모드
- **Edit Mode:** 오브젝트 내부의 점, 선, 면을 직접 편집하는 모드
- **Tab 키**로 두 모드를 전환
- Edit Mode에서는 메시의 형태를 자유롭게 변경할 수 있음

### Primitive 종류

Shift + A > Mesh 메뉴에서 기본 도형을 추가할 수 있음

- **Cube:** 정육면체. 가장 기본적인 모델링 출발점
- **UV Sphere:** 경위도 방식의 구체. 균일한 사각형 면으로 구성
- **Ico Sphere:** 삼각형 면으로 구성된 구체. 유기적 형태에 적합
- **Cylinder:** 원기둥. 팔, 다리, 기둥 등에 활용
- **Cone:** 원뿔. 뿔, 모자 등에 활용
- **Torus:** 도넛 형태. 바퀴, 링 등에 활용
- **Plane:** 평면. 바닥, 벽 등에 활용
- **Circle:** 원. Edge만으로 구성된 형태

도형 추가 직후 F9 키를 누르면 Segments, Rings 등 생성 옵션을 조절할 수 있음

### 선택 모드

Edit Mode에서 상단 Header 또는 단축키로 전환

- **1 (Vertex):** 점 선택 모드. 개별 꼭짓점을 선택하고 이동
- **2 (Edge):** 선 선택 모드. 두 점을 잇는 변을 선택
- **3 (Face):** 면 선택 모드. 면 전체를 선택하여 조작

#### 선택 방법

- Left Click: 단일 선택
- Shift + Left Click: 복수 선택 (추가/제거)
- A: 전체 선택
- Alt + A: 전체 선택 해제
- L: 연결된 요소 전체 선택 (마우스 커서 위치 기준)
- Ctrl + Numpad +: 선택 영역 확장
- Shift로 Vertex/Edge/Face 복수 선택 모드를 동시에 활성화 가능

## 실습 (90분)

### Edit Mode 진입과 선택 연습 (15분)

1. 기본 Cube 선택 후 Tab 키로 Edit Mode 진입
2. 1, 2, 3 키로 선택 모드 전환하며 차이 확인
3. Vertex 모드에서 점 하나를 선택하고 G 키로 이동
4. Edge 모드에서 변 하나를 선택하고 이동
5. Face 모드에서 면 하나를 선택하고 이동
6. Shift + Click으로 여러 요소를 동시에 선택하는 연습

> 💡 **프로 팁:** **Wireframe 모드 (Z > Wireframe)**에서 선택하면 뒷면의 Vertex/Edge/Face도 함께 선택할 수 있다. Solid 모드에서는 보이는 면만 선택되므로, 대칭적인 편집이 필요할 때는 Wireframe 모드를 활용하자.

### Extrude (E) (20분)

#### 기본 사용법

1. Face 모드(3)로 전환
2. 돌출할 면을 선택
3. E 키를 누르면 선택한 면이 돌출됨
4. 마우스로 돌출 방향과 거리를 조절한 후 Left Click으로 확정

#### Region Extrude vs Individual Faces

- **Region Extrude (E):** 선택한 면들을 하나의 영역으로 돌출
- **Individual Faces (Mesh > Extrude > Extrude Individual Faces):** 각 면이 개별적으로 돌출

#### 활용

- 로봇 머리 위에 안테나 돌출
- 로봇 얼굴에서 눈 부분 돌출

> 💡 **프로 팁:** Extrude 후 ESC나 Right Click으로 취소하면 겉보기에는 취소된 것 같지만, 실제로는 **중복 Vertex가 생성**되어 있다. 이 경우 즉시 **Ctrl + Z**로 되돌리거나, M 키 > Merge by Distance로 중복 Vertex를 제거해야 한다.

### Loop Cut (Ctrl + R) (15분)

#### 기본 사용법

1. Ctrl + R을 누르면 마우스 위치에 따라 노란색 Edge Loop 미리보기가 표시됨
2. Left Click으로 Loop Cut 위치를 확정
3. 마우스를 움직여 위치를 세밀하게 조정한 후 Left Click으로 완료
4. 또는 Right Click으로 중앙 위치에 고정

#### 마우스 스크롤로 개수 조절

- Ctrl + R 후 스크롤 업: Loop Cut 개수 증가
- Ctrl + R 후 스크롤 다운: Loop Cut 개수 감소

#### 활용

- 로봇 몸체에 분할선을 추가하여 팔, 다리 돌출을 위한 면 생성
- 디테일을 추가할 영역에 추가적인 Edge Loop 삽입

> 💡 **프로 팁:** Loop Cut 후 위치 조정 시 **Right Click**을 누르면 정확히 **중앙에 고정**된다. 균등한 분할이 필요할 때 유용하다. 또한 **Proportional Editing (O키)**을 활성화하면 주변 Vertex가 함께 부드럽게 변형되어, 유기적인 곡면을 만들기 좋다.

### Inset (I) (10분)

#### 기본 사용법

1. Face 모드(3)에서 면을 선택
2. I 키를 누르면 선택한 면 안쪽에 새로운 면이 생성됨
3. 마우스로 크기를 조절한 후 Left Click으로 확정

#### 활용

- 로봇 얼굴에서 눈 영역을 Inset으로 만든 후, 안쪽 면을 Extrude로 움푹하게 처리
- 가슴 부분에 패널이나 버튼 영역 생성

### Bevel (Ctrl + B) (10분)

#### 기본 사용법

1. Edge 모드(2)에서 Edge를 선택
2. Ctrl + B를 누르면 선택한 Edge가 둥글게 분할됨
3. 마우스로 Bevel 크기를 조절
4. 마우스 스크롤로 Segment(분할) 수를 조절하여 부드러움 정도를 결정
5. Left Click으로 확정

#### 활용

- 로봇의 날카로운 모서리를 부드럽게 처리
- 기계적인 느낌에서 약간의 곡면감을 부여

### 로봇 기본 형태 만들기 (20분)

#### 제작 순서

1. **몸통:** Cube에서 시작. S + Z로 세로로 약간 늘림
2. **머리:** 몸통 상단 Face를 선택하고 Extrude로 돌출
3. **팔:** 몸통 좌우 Face를 선택하고 Extrude로 돌출
4. **다리:** 몸통 하단 Face를 선택하고 Extrude로 돌출
5. **디테일:** Loop Cut으로 관절 부분에 Edge Loop 추가
6. **마무리:** Bevel로 모서리를 부드럽게 처리

#### 팁

- 좌우 대칭을 유지하려면 한쪽만 작업 후 Mirror Modifier를 활용 (다음 주 학습)
- Apply Transform(Ctrl + A)을 수시로 적용하여 Transform 값 정리
- Numpad 1, 3으로 정면/측면 뷰를 오가며 형태 확인

## ⚠️ 흔한 실수와 해결법

| 실수 | 원인 | 해결법 |
|------|------|--------|
| Edit Mode에서 일부 Vertex가 선택되지 않음 | H 키로 숨겨놓은 요소가 있음 | **Alt + H**로 모든 숨겨진 요소를 Unhide |
| Extrude 취소 후 메시가 이상해짐 | ESC/Right Click으로 취소해도 중복 Vertex가 생성됨 | **Ctrl + Z**로 완전히 되돌리거나, **M > Merge by Distance**로 중복 Vertex 정리 |
| Face의 색이 어둡거나 음영이 이상함 | Face Normal 방향이 뒤집어져 있음 | Edit Mode에서 전체 선택(A) 후 **Shift + N** (Recalculate Outside)으로 Normal 방향 통일 |
| 선택 모드가 갑자기 바뀜 | 실수로 1, 2, 3 키를 누름 | Header 상단의 선택 모드 아이콘을 확인. Vertex/Edge/Face 중 원하는 모드 클릭 |
| 도형 추가 후 옵션 패널이 사라짐 | 다른 조작을 먼저 수행함 | 도형 추가 **직후** 바로 **F9**를 눌러야 옵션 조절 가능. 다른 작업 전에 설정 완료하기 |

## 과제

- **제출:** Discord #week03-assignment 채널
- **내용:** 로봇/캐릭터 기본 형태 스크린샷 3장 + 한줄 코멘트
  - Front 뷰 (Numpad 1)
  - Side 뷰 (Numpad 3)
  - Perspective 뷰 (자유 각도)
- **기한:** 다음 수업 전까지

## 핵심 정리

| 개념 | 핵심 내용 |
|------|-----------|
| Object Mode vs Edit Mode | Object Mode는 오브젝트 단위 조작, Edit Mode (Tab)는 점/선/면 직접 편집 |
| 선택 모드 | 1 (Vertex), 2 (Edge), 3 (Face). Shift로 복수 모드 동시 활성화 가능 |
| Extrude (E) | 선택한 면을 돌출. 로봇 팔, 다리, 안테나 등 형태 확장에 핵심 |
| Loop Cut (Ctrl + R) | Edge Loop 추가로 면을 분할. 스크롤로 개수 조절, Right Click으로 중앙 고정 |
| Inset (I) | 면 안쪽에 새 면 생성. 눈, 버튼, 패널 영역 만들기에 활용 |
| Bevel (Ctrl + B) | Edge를 둥글게 분할. 스크롤로 Segment 수 조절, 부드러운 모서리 처리 |
| Merge by Distance (M) | 중복 Vertex 정리. Extrude 실수 후 필수 점검 |

> Edit Mode의 4대 도구(Extrude, Loop Cut, Inset, Bevel)만 잘 활용해도 대부분의 기본 형태를 만들 수 있다.

## 📋 프로젝트 진행 체크리스트

이번 주차까지 아래 항목이 완료되어야 합니다:

- [ ] 로봇 기본 형태 완성 (머리 + 몸통 + 팔 + 다리)
- [ ] 정면 뷰 (Numpad 1) 실루엣 확인 - 캐릭터 특징이 드러나는지 점검
- [ ] 측면 뷰 (Numpad 3) 실루엣 확인 - 두께감과 비율이 적절한지 점검
- [ ] 불필요한 중복 Vertex 정리 완료
- [ ] Apply Transform (Ctrl + A) 적용 완료

## 참고 자료

- [Blender 단축키 모음](../../resources/blender-shortcuts.md)
