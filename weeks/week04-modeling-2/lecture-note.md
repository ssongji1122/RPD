# Week 04: 기초 모델링 2 - 하드서피스 디테일 & 정리

## 학습 목표

- [ ] `Ctrl + B`와 `Bevel Modifier`의 차이를 설명할 수 있다
- [ ] `Weighted Normal`이 어떤 문제를 해결하는지 이해한다
- [ ] `Apply Transform`과 `Modifier Apply`의 시점을 구분할 수 있다
- [ ] 로봇 모델의 얼굴, 관절, 패널 디테일을 더 깔끔하게 정리할 수 있다

## 🔗 이전 주차 복습

- Week 03에서 **기본형 + Mirror + Subdivision + Bevel/Weighted Normal + Join/Separate + Apply 타이밍**까지 한 번 경험했다
- 이번 주는 큰 덩어리를 새로 만드는 시간보다, **이미 만든 형태를 더 좋아 보이게 정리하는 시간**이다
- 계속해서 **G / R / S**, 축 제한, `Ctrl + A`를 사용한다

## 이론 (30분)

### 이번 주 흐름

- 지난주에는 로봇의 **큰 덩어리**를 만들었다
- 이번 주에는 얼굴, 관절, 패널 같은 **디테일**을 더한다
- 그리고 마지막에 **음영 정리**와 **Apply 타이밍**을 구분한다

> 💡 실제 로봇 모델링 영상도 대부분 `기본형 → 디테일 추가 → 음영 정리 → 마지막에만 확정` 흐름으로 진행된다.

### 디테일에서 자주 쓰는 도구

| 도구 | 언제 쓰는지 | 기억할 점 |
|------|-------------|-----------|
| **Inset (I)** | 버튼, 눈, 패널 영역을 안쪽으로 한 번 더 잡을 때 | 디테일 시작점을 만들기 좋다 |
| **Boolean** | 구멍, 소켓, 홈을 빠르게 만들 때 | 커터가 실제로 겹쳐 있어야 한다 |
| **Bevel (`Ctrl + B`)** | 특정 모서리만 직접 깎을 때 | 손으로 직접 다듬는 느낌 |
| **Bevel Modifier** | 전체 외장 모서리 느낌을 비파괴로 정리할 때 | 나중에도 값을 조절할 수 있다 |
| **Weighted Normal** | 형태는 괜찮은데 음영이 울퉁불퉁해 보일 때 | Bevel Modifier와 함께 볼 때 차이가 잘 보인다 |

### 헷갈리기 쉬운 Apply 두 가지

| 항목 | 의미 | 언제 쓰는지 |
|------|------|-------------|
| **Apply Transform (`Ctrl + A`)** | 위치/회전/스케일 수치를 정리 | Modifier 전, 작업 중간중간 확인 |
| **Apply Modifier** | 현재 Modifier 결과를 실제 메쉬로 확정 | 정말 마지막 정리 단계 |

> ⚠️ `Ctrl + A`는 자주 써도 되지만, `Modifier Apply`는 너무 일찍 하면 수정 여지가 줄어든다.

## 실습 (90분)

### Step 1: Transform 정리 + 파츠 관리 (20분)

1. Week 03에서 만든 로봇 파일을 연다
2. `N` 패널에서 Scale이 `(1, 1, 1)`인지 확인한다
3. 이상하면 `Ctrl + A > All Transforms`를 적용한다
4. 따로 관리할 파츠는 `P > Selection`으로 분리한다
5. 하나로 묶어도 되는 파츠는 `Ctrl + J`로 합친다

> 💡 관절, 안테나, 헤드셋처럼 따로 움직일 수 있는 파츠는 미리 분리해두면 이후 작업이 편하다.

### Step 2: 얼굴 / 패널 / 관절 디테일 만들기 (20분)

1. 얼굴이나 가슴 패널처럼 눈에 잘 보이는 부위를 하나 고른다
2. `Inset (I)`으로 안쪽 영역을 만든다
3. 필요하면 `Extrude`로 살짝 들어가거나 나오게 만든다
4. 구멍이나 소켓이 필요하면 `Boolean Difference`를 사용한다
5. 디테일을 넣은 뒤 정면, 측면, 투시 뷰에서 다시 확인한다

### Step 3: Bevel 두 가지 비교하기 (20분)

#### `Ctrl + B`

- 특정 모서리를 직접 골라서 깎는다
- 얼굴 테두리, 손가락 끝, 패널 라인처럼 **부분 수정**에 좋다

#### Bevel Modifier

- 오브젝트 전체의 모서리 느낌을 한 번에 조절한다
- 외장 파츠 전체를 정리할 때 좋다

**실습 포인트**

1. 작은 파츠 하나는 `Ctrl + B`로 직접 다듬는다
2. 다른 파츠 하나는 `Bevel Modifier`를 넣어 비교한다
3. Width와 Segments를 바꾸며 차이를 확인한다

### Step 4: Weighted Normal로 음영 정리하기 (15분)

1. `Shade Smooth`를 먼저 적용한다
2. `Bevel Modifier` 아래에 `Weighted Normal`을 추가한다
3. 전후를 비교하며 표면이 얼마나 깔끔해졌는지 본다
4. 특히 평평한 면이 많은 가슴판, 팔 외장, 다리 파츠에서 확인한다

> 💡 `Weighted Normal`은 모양을 바꾸는 도구라기보다 **빛이 닿는 느낌을 정리하는 도구**라고 이해하면 쉽다.

### Step 5: 최종 점검과 Apply 시점 이해하기 (15분)

1. Modifier Stack 순서를 다시 확인한다
2. 수정할 가능성이 남아 있으면 Apply하지 않는다
3. 정말 확정할 파츠만 별도 저장 후 Apply를 시험해본다
4. 스크린샷은 `수정 가능한 상태`와 `최종 확인 화면`을 모두 남긴다

## ⚠️ 흔한 실수와 해결법

| 실수 | 원인 | 해결법 |
|------|------|--------|
| Bevel이 너무 두꺼워 보임 | Width가 과함 | 값을 아주 작게 시작하고 천천히 올린다 |
| Weighted Normal 차이가 잘 안 보임 | 비교 기준이 없음 | Bevel Modifier 전후, Shade Smooth 전후를 같이 본다 |
| Boolean이 지저분함 | 커터가 애매하게 겹침 | 커터를 더 명확히 겹치고 Scale도 정리한다 |
| Apply 후 수정이 어려워짐 | Modifier를 너무 일찍 확정함 | **Modifier Apply는 마지막에만** |
| 파츠 관리가 헷갈림 | 합쳐야 할 것과 분리할 것이 섞여 있음 | 움직일 파츠는 분리, 고정 파츠는 정리해서 묶는다 |

## 과제

- **제출:** Discord `#week04-assignment` 채널
- **내용:** Week 03 기본형에 디테일과 음영 정리를 더한 로봇/캐릭터 형태 제작
- **형식:** 스크린샷 3장 + 사용한 도구/Modifier 목록 + 한줄 코멘트
  - 1장: 디테일 작업 과정
  - 2장: Modifier Stack 또는 Transform 확인 화면
  - 3장: 최종 결과 화면
- **기한:** 다음 수업 전까지

## 핵심 정리

| 개념 | 핵심 내용 |
|------|-----------|
| `Ctrl + B` | 특정 모서리를 직접 깎는 수동 Bevel |
| Bevel Modifier | 전체 외장 모서리를 비파괴로 정리 |
| Weighted Normal | 하드서피스 음영을 깔끔하게 정리 |
| Apply Transform | Modifier 전 Scale/Rotation을 정리 |
| Modifier Apply | 최종 확정 단계에서만 사용 |
| Join / Separate | 파츠를 묶거나 분리해 관리 |

## 📋 프로젝트 진행 체크리스트

- [ ] 얼굴, 패널, 관절 중 한 곳 이상 디테일을 추가했다
- [ ] `Ctrl + B` 또는 `Bevel Modifier`를 사용했다
- [ ] `Weighted Normal`을 확인했다
- [ ] `Ctrl + A`로 Transform을 점검했다
- [ ] 파츠를 분리하거나 합쳐서 정리했다
- [ ] 결과 스크린샷 3장을 저장했다

## 참고 자료

- [Blender 단축키 모음](../../resources/blender-shortcuts.md)
- [Blender Manual - Bevel Tool](https://docs.blender.org/manual/en/latest/modeling/meshes/tools/bevel.html)
- [Blender Manual - Bevel Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html)
- [Blender Manual - Weighted Normal Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weighted_normal.html)
- [Blender Manual - Boolean Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html)
