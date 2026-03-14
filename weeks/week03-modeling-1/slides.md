---
marp: true
theme: rpd
paginate: true
---

# Week 03: 기초 모델링 1

## Edit Mode

2026 Spring | 인하대학교 | 송지희

---

## Object Mode vs Edit Mode

- **Object Mode:** 오브젝트 단위 조작 (이동, 회전, 스케일)
- **Edit Mode:** 메시 내부의 점, 선, 면을 직접 편집
- **Tab 키**로 두 모드를 전환

Object Mode에서 형태를 잡고, Edit Mode에서 디테일을 만든다

---

## Primitive 종류

Shift + A > Mesh로 추가

| 도형 | 설명 | 활용 |
|------|------|------|
| Cube | 정육면체 | 모델링의 기본 출발점 |
| UV Sphere | 경위도 구체 | 머리, 눈 등 구형 |
| Ico Sphere | 삼각형 구체 | 유기적 형태 |
| Cylinder | 원기둥 | 팔, 다리, 기둥 |
| Cone | 원뿔 | 뿔, 모자 |
| Torus | 도넛 | 바퀴, 링 |

F9: 생성 직후 옵션 조절 (Segments, Rings 등)

---

## 선택 모드 (Vertex / Edge / Face)

- **1 (Vertex):** 점 선택. 가장 세밀한 조작
- **2 (Edge):** 선 선택. 두 점을 잇는 변
- **3 (Face):** 면 선택. 가장 자주 사용

**선택 방법:**
- Left Click: 단일 선택
- Shift + Click: 복수 선택
- A: 전체 선택 / Alt + A: 전체 해제
- L: 연결된 요소 전체 선택

---

## Extrude (E) 사용법

1. Face 모드(3)에서 돌출할 면 선택
2. E 키로 돌출
3. 마우스로 방향과 거리 조절
4. Left Click으로 확정

**Region Extrude (E):** 면들을 하나의 영역으로 돌출
**Individual Faces:** 각 면이 개별적으로 돌출

---

## Extrude 활용 예시

**로봇 팔 만들기:**
1. Cube의 측면 Face 선택
2. E 키로 돌출하여 팔 생성
3. S 키로 크기 조절하며 형태 다듬기

**안테나 만들기:**
1. 머리 상단 Face 선택
2. S 키로 면 축소 후 E 키로 길게 돌출

---

## Loop Cut (Ctrl + R)

1. Ctrl + R로 활성화
2. 마우스 위치에 따라 노란색 미리보기 표시
3. **스크롤 업/다운:** Loop Cut 개수 조절
4. Left Click으로 위치 확정
5. Right Click으로 중앙에 고정

**활용:**
- 관절 부분에 Edge Loop 추가
- 디테일 영역에 분할선 삽입

---

## Inset (I)

1. Face 모드(3)에서 면 선택
2. I 키로 안쪽에 새 면 생성
3. 마우스로 크기 조절 후 Left Click 확정

**활용:**
- 로봇 얼굴에 눈 영역 생성
- 가슴 패널이나 버튼 영역 만들기
- Inset 후 Extrude로 움푹한 형태 제작

---

## Bevel (Ctrl + B)

1. Edge 모드(2)에서 Edge 선택
2. Ctrl + B로 Bevel 적용
3. 마우스로 Bevel 크기 조절
4. **스크롤 업/다운:** Segment 수 조절 (부드러움 정도)
5. Left Click으로 확정

**활용:**
- 날카로운 모서리를 부드럽게 처리
- 기계적 형태에 곡면감 부여

---

## 실습: 로봇 머리 만들기

1. Cube에서 시작
2. Loop Cut(Ctrl + R)으로 가로/세로 분할
3. 얼굴 부분에 Inset(I)으로 눈 영역 생성
4. 눈 영역을 Extrude(E)로 움푹하게
5. 상단 Face에서 Extrude로 안테나 돌출
6. Bevel(Ctrl + B)로 모서리 부드럽게 처리

---

## 과제 안내

- **제출처:** Discord #week03-assignment 채널
- **내용:**
  - Front 뷰 스크린샷 (Numpad 1)
  - Side 뷰 스크린샷 (Numpad 3)
  - Perspective 뷰 스크린샷 (자유 각도)
  - 한줄 코멘트
- **평가:** 도구 활용 40% / 완성도 30% / 창의성 30%

---

## 다음 주 예고

**Week 04: 기초 모델링 2 - Modifier**

- Mirror Modifier로 좌우 대칭 모델링
- Subdivision Surface로 부드러운 곡면
- Boolean으로 형태 결합/분리
- Solidify로 두께 부여
