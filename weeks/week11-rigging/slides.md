---
marp: true
theme: rpd
paginate: true
---

# Week 11: Rigging 기초

## 로봇프러덕트 디자인

2026 Spring | 인하대학교 | 송지희

---

## 리깅(Rigging)이란?

- 3D 모델 안에 **뼈대(Armature)**를 넣어 메쉬를 움직이게 하는 시스템
- 현실 세계의 **관절과 뼈**를 디지털로 구현
- 리깅 없이는 모델을 자연스럽게 움직일 수 없음

**3D 파이프라인에서의 위치:**

모델링 > 텍스처 > **리깅** > 애니메이션

---

## 캐릭터 리깅 vs 기계 리깅

| 항목 | 캐릭터 리깅 | 기계/로봇 리깅 |
|------|-----------|--------------|
| 변형 방식 | 부드러운 변형 (Smooth) | 독립적 회전 (Rigid) |
| Weight Painting | 필수 (그라데이션) | 간단 (0 또는 1) |
| 연결 방식 | Automatic Weights | Bone Parenting |
| 대상 | 사람, 동물 | 로봇, 기계, 차량 |

**이 수업: 로봇 리깅 중심 + 캐릭터 리깅 개념 이해**

---

## Armature & Bone 구조

**Armature:** Bone의 집합체 (뼈대 시스템)
- 생성: Shift+A > Armature > Single Bone

**Bone 구성 요소:**
- **Head (Root):** 시작점 (둥근 끝)
- **Tail (Tip):** 끝점 (뾰족한 끝)
- **Body:** Head와 Tail을 잇는 본체
- **Roll:** 축 회전 각도

Viewport Display > **In Front** 체크: Armature가 항상 보이도록

---

## Bone 추가 방법 (Edit Mode)

**Armature 선택 > Tab (Edit Mode 진입)**

| 동작 | 단축키 | 설명 |
|------|--------|------|
| Bone 연장 | E (Extrude) | 현재 Bone 끝에서 연결된 새 Bone |
| 독립 Bone 추가 | Shift+A | 연결되지 않은 새 Bone |
| Bone 분할 | Subdivide | 하나의 Bone을 여러 개로 나누기 |
| Bone 삭제 | X / Delete | 선택한 Bone 제거 |
| 이름 변경 | Properties > Bone | 좌우 대칭: .L / .R 접미사 |

---

## Parent-Child 관계

**Connected (연결):**
- Child의 Head가 Parent의 Tail에 물리적으로 연결
- Parent 움직임을 Child가 자동으로 따라감
- 예: 상완 > 하완 > 손

**Free (자유):**
- 위치가 분리되지만 계층 관계 유지
- 예: 어깨와 팔 (독립 회전 필요)

**설정:** Child 선택 > Shift+클릭으로 Parent 선택 > Ctrl+P

---

## IK vs FK 비교

**IK (Inverse Kinematics):**
- 끝에서 당기면 연결된 뼈가 **자동으로 따라옴**
- 손 위치를 지정하면 팔꿈치, 어깨 자동 조정
- 직관적이고 빠른 포징

**FK (Forward Kinematics):**
- 부모 뼈부터 **하나씩 회전**
- 어깨 > 팔꿈치 > 손목 순서대로 조정
- 정밀한 각도 제어 가능

| 추천 사용 | IK | FK |
|----------|----|----|
| 팔, 다리 | O | |
| 꼬리, 안테나 | | O |
| 체인, 촉수 | | O |

---

## Weight Painting 개념

- 각 Bone이 메쉬에 미치는 **영향 범위**를 색상으로 시각화
- 모드 진입: 메쉬 선택 > Ctrl+Tab > Weight Paint

**색상 의미:**
- **빨간색 (1.0):** 완전히 영향 (100%)
- **노란색 (0.5):** 절반 영향 (50%)
- **파란색 (0.0):** 영향 없음 (0%)

**로봇:** 각 파츠에 해당 Bone = 1.0, 나머지 = 0.0
**캐릭터:** 관절 주변에 그라데이션 (부드러운 변형)

---

## Weight Painting 실습

**브러시 종류:**
- **Add:** Weight 값 증가 (영향 추가)
- **Subtract:** Weight 값 감소 (영향 제거)
- **Draw:** 직접 Weight 값 지정

**팁:**
- Weight: 1.0, Strength: 1.0으로 한 번에 칠하기
- Armature를 Pose Mode로 전환하여 Bone 회전하면서 확인
- 로봇은 파츠별로 단순하게, 캐릭터는 관절을 세밀하게

---

## Pose Mode

- **리깅 완료 후** 포즈를 잡는 모드
- Armature 선택 > Ctrl+Tab > Pose Mode

**포즈 조작:**
- R: Bone 회전
- G: Bone 이동 (IK가 설정된 경우)
- Alt+R: 회전 초기화
- Alt+G: 위치 초기화
- A > Alt+R > Alt+G: 전체 포즈 초기화

**Keyframe:** I > Location & Rotation으로 포즈 저장

---

## 실습: 로봇 팔 리깅

**Armature 구조:**

Shoulder > UpperArm > Forearm > Hand

**작업 순서:**
1. Shift+A > Armature > Single Bone
2. Edit Mode에서 E로 Bone 4개 생성
3. 각 Bone 이름 지정 (Shoulder, UpperArm, Forearm, Hand)
4. 파츠별 Cylinder 메쉬 생성
5. 메쉬 선택 > Shift+클릭 Armature > Ctrl+P > With Empty Groups
6. Vertex Groups에서 해당 Bone 그룹에 Assign (Weight 1.0)

---

## 실습: 로봇 다리 리깅

**Armature 구조:**

Hip > UpperLeg > LowerLeg > Foot

**작업 순서:**
1. 기존 Armature의 Edit Mode에서 Shift+A로 새 Bone 추가
2. E로 다리 Bone 체인 생성 (4개)
3. 이름 지정: Hip, UpperLeg, LowerLeg, Foot
4. 파츠별 Cylinder 메쉬 생성
5. 각 메쉬를 해당 Bone에 연결 (같은 방법)
6. Pose Mode에서 다리 Bone 회전하여 움직임 확인

---

## 핵심 단축키 정리

| 단축키 | 기능 |
|--------|------|
| Shift+A > Armature | Armature 생성 |
| E | Bone Extrude (Edit Mode) |
| Ctrl+P | Parent 설정 / 메쉬-Armature 연결 |
| Ctrl+Tab | 모드 전환 |
| R | Bone 회전 (Pose Mode) |
| I | Keyframe 삽입 (Pose Mode) |
| Alt+R | 회전 초기화 |
| Alt+G | 위치 초기화 |

---

## 다음 주 예고: Mixamo로 AI 자동 리깅

**Week 12: AI 활용 리깅 (Mixamo)**

- Adobe Mixamo: 무료 자동 리깅 + 2000+ 애니메이션
- 복잡한 리깅을 AI가 자동으로 처리
- NLA Editor로 여러 애니메이션 조합

**준비:** Adobe 계정 가입 (무료) - https://mixamo.com

**과제:** 자신의 로봇/캐릭터에 기초 리깅 적용 + 포즈 2가지 이상
