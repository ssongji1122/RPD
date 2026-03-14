---
marp: true
theme: rpd
paginate: true
---

# Week 04: 기초 모델링 2

## 하드서피스 디테일 & 정리

## 로봇프러덕트 디자인

2026 Spring | 인하대학교 | 송지희

---

## 이번 주 포인트

- Week 03에서 배운 흐름을 **실전에 반복 적용**하는 주차
- 얼굴, 관절, 패널 같은 **디테일** 추가
- **Bevel / Weighted Normal / Apply 타이밍**은 복습하며 더 익히기
- 파츠 분리와 합치기까지 같이 점검

---

## 디테일에서 자주 쓰는 것

| 도구 | 역할 |
|------|------|
| Inset | 버튼, 눈, 패널 영역 만들기 |
| Boolean | 구멍, 소켓, 홈 만들기 |
| Ctrl + B | 특정 모서리 직접 깎기 |
| Bevel Modifier | 전체 외장 모서리 정리 |
| Weighted Normal | 하드서피스 음영 정리 |

---

## Apply 두 가지 차이

| 항목 | 언제 쓰는가 |
|------|-------------|
| **Ctrl + A** | Modifier 전 Transform 정리 |
| **Modifier Apply** | 정말 마지막 확정 단계 |

**Ctrl + A는 자주 확인해도 되지만, Modifier Apply는 초반에 하지 않기**

---

## Step 1: Transform 정리 + 파츠 관리

- `N` 패널에서 Scale 확인
- 필요하면 **Ctrl + A > All Transforms**
- 따로 관리할 파츠는 **P > Selection**
- 묶어도 되는 파츠는 **Ctrl + J**

---

## Step 2: 얼굴 / 패널 디테일

- **Inset**으로 안쪽 영역 만들기
- 필요하면 **Extrude**로 들어가거나 나오게
- 구멍, 소켓은 **Boolean Difference**
- 정면, 측면, 투시에서 같이 보기

---

## Step 3: Bevel 두 가지 비교

**Ctrl + B**
- 특정 모서리만 직접 다듬기

**Bevel Modifier**
- 전체 외장 느낌을 비파괴로 조절

**비교 포인트**
- 부분 수정 vs 전체 정리
- 지금 바로 수정 vs 나중에도 값 변경 가능

---

## Step 4: Weighted Normal

- **Shade Smooth** 먼저 적용
- **Bevel Modifier 아래**에 넣어 비교
- 평평한 외장 면에서 차이가 잘 보임
- 모양보다 **빛 반응**을 정리하는 도구

---

## 흔한 실수

- Bevel이 너무 큼 → 값 아주 작게 시작
- Boolean이 이상함 → 커터가 실제로 겹치는지 확인
- Apply를 너무 일찍 함 → 마지막에만
- 음영이 지저분함 → **Weighted Normal** 확인
- 파츠 관리가 헷갈림 → 움직일 파츠는 분리

---

## 과제

- 얼굴, 관절, 패널 중 **디테일 1곳 이상**
- `Ctrl + B` 또는 `Bevel Modifier`
- `Weighted Normal` 확인
- 스크린샷 3장
- 한줄 코멘트

---

## 다음 주 예고

**Week 05: AI 3D 생성 + Sculpting + MCP 활용**

- AI 도구(Meshy, Tripo)로 3D 모델 생성
- Blender Sculpt Mode 기초 브러시
- Blender MCP로 씬 자동 생성
- AI 모델을 Blender에서 수정하는 워크플로우
