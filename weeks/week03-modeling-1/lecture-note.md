# Week 03: 기초 모델링 1 - Edit Mode + Modifier

## 학습 목표

- [ ] Edit Mode의 핵심 도구를 이해한다
- [ ] Modifier가 무엇인지 쉽게 설명할 수 있다
- [ ] Mirror, Subdivision Surface, Solidify, Array, Boolean을 사용할 수 있다
- [ ] Bevel Tool과 Bevel Modifier의 차이를 구분할 수 있다
- [ ] Weighted Normal, Join/Separate, Apply 타이밍을 작업 흐름 안에서 이해한다
- [ ] Edit Mode와 Modifier를 조합해 로봇 기본 형태를 만들 수 있다

## 🔗 이전 주차 복습

- Week 02에서 배운 **G / R / S**와 축 제한을 계속 사용한다
- 작업 전 **Ctrl + A > All Transforms**를 적용하는 습관이 중요하다
- **Numpad 1 / 3 / 7**로 정면, 측면, 상면을 자주 오가며 형태를 확인한다
- 파츠가 많아지면 **P (Separate)**, **Ctrl + J (Join)**로 정리할 수 있다

## 이론 (30분)

### 이번 주 흐름

- **Edit Mode:** 점, 선, 면을 직접 움직이며 기본형을 만든다
- **Modifier:** 원본을 바로 깎지 않고 효과를 얹어 더 빠르게 다듬는다
- **Join / Separate:** 파츠를 나누거나 묶어 작업을 정리한다
- **Apply 타이밍:** `Ctrl + A`는 중간에도 자주, `Modifier Apply`는 마지막에만
- 이번 주는 **손으로 형태를 만들고, Modifier로 정리하는 흐름**으로 이해하면 된다

> 💡 Edit Mode는 손으로 점토를 만지는 단계이고, Modifier는 거울 효과나 두께 효과 같은 필터를 얹는 단계라고 생각하면 쉽다.

### 꼭 기억할 Edit Mode 도구 4개

| 도구 | 쉽게 말하면 | 어디에 쓰는지 |
|------|-------------|----------------|
| **Extrude (E)** | 점토를 잡아당기기 | 팔, 다리, 안테나, 돌출 |
| **Loop Cut (Ctrl + R)** | 케이크에 칼집 넣기 | 분할선, 관절 위치 만들기 |
| **Inset (I)** | 면 안쪽에 작은 면 하나 더 만들기 | 눈, 패널, 버튼 영역 |
| **Bevel (Ctrl + B)** | 날카로운 모서리를 살짝 깎기 | 부드러운 모서리, 기계 디테일 |

### Modifier란?

- Modifier는 **필터처럼 얹는 기능**이라고 생각하면 쉽다
- 원본 메쉬를 바로 망가뜨리지 않고, 화면에 보이는 결과를 바꿔준다
- 숫자를 바꾸거나 끄거나 지우면서 실험하기 좋다
- 위치는 `Properties > Modifier Properties` (렌치 아이콘)

> 💡 **Non-destructive**는 되돌릴 수 있다는 뜻이다. Apply 하기 전까지는 원본을 살려둔 채 실험할 수 있다.

### 자주 쓰는 Modifier 한눈에 보기

| Modifier | 한 줄 비유 | 주로 하는 일 |
|----------|------------|---------------|
| **Mirror** | 거울처럼 반대편이 자동으로 생긴다 | 좌우 대칭 모델링 |
| **Subdivision Surface** | 스케치를 더 촘촘하게 다시 그린다 | 곡면을 부드럽게 만들기 |
| **Solidify** | 종이에 두께를 준다 | 외장 패널, 얇은 판 만들기 |
| **Array** | 도장을 여러 번 찍는다 | 반복 구조 만들기 |
| **Boolean** | 블록을 붙이거나 뺀다 | 구멍, 홈, 소켓 만들기 |

### 필수로 알아둘 추가 Modifier

| Modifier | 언제 쓰는지 | 같이 기억할 점 |
|----------|-------------|----------------|
| **Bevel Modifier** | 모서리를 비파괴로 둥글게 만들 때 | 하드서피스에서 자주 쓴다 |
| **Weighted Normal** | 음영이 이상할 때 정리할 때 | Bevel Modifier와 같이 쓰는 경우가 많다 |

### 선택으로 써볼 Modifier

| Modifier | 언제 쓰는지 | 같이 기억할 점 |
|----------|-------------|----------------|
| **Simple Deform** | 전체를 휘게, 비틀게, 가늘게 만들 때 | Bend, Twist, Taper를 빠르게 시험할 수 있다 |
| **Decimate** | 너무 무거운 메쉬를 가볍게 만들 때 | AI 생성 메쉬나 복잡한 모델에서 유용하다 |

### 영상에서 자주 보이는 실전 흐름

1. `G / R / S`로 큰 덩어리 위치를 먼저 맞춘다
2. `Ctrl + A > All Transforms`로 Scale과 Rotation을 정리한다
3. Edit Mode에서 `Extrude`, `Loop Cut`, `Inset`, `Bevel`로 기본형을 만든다
4. `Mirror`, `Subdivision Surface`로 실루엣을 빠르게 정리한다
5. `Boolean`이나 `Inset`으로 얼굴, 패널, 소켓 디테일을 추가한다
6. `Bevel Modifier`와 `Weighted Normal`로 표면 느낌과 음영을 정리한다
7. `Modifier Apply`는 정말 마지막에만 한다

### 헷갈리기 쉬운 차이

| 항목 | 언제 쓰는지 | 기억할 점 |
|------|-------------|-----------|
| **Edit Mode Bevel (`Ctrl + B`)** | 특정 모서리만 직접 다듬고 싶을 때 | 지금 선택한 부분만 바로 수정된다 |
| **Bevel Modifier** | 전체 모서리 느낌을 비파괴로 조절할 때 | 나중에도 값을 바꿀 수 있다 |
| **Apply Transform (`Ctrl + A`)** | Modifier 전, 비율과 회전을 정리할 때 | 작업 중간에도 자주 확인하는 편이 안전하다 |
| **Apply Modifier** | 형태를 최종 확정할 때 | 초반에 해버리면 수정 여지가 줄어든다 |

### Modifier Stack

- Modifier는 **위에서 아래로** 순서대로 계산된다
- 순서가 바뀌면 결과도 달라진다
- 처음에는 아래 순서를 기준으로 보면 덜 헷갈린다

```plain text
Mirror
↓
Boolean
↓
Subdivision Surface
```

> ⚠️ 같은 Modifier를 써도 순서가 달라지면 전혀 다른 결과가 나온다.

## 실습 (90분)

### Step 1: Edit Mode로 기본형 만들기 (20분)

1. Cube에서 시작
2. **Extrude (E)**로 머리, 팔, 다리 위치를 만든다
3. **Loop Cut (Ctrl + R)**로 관절과 분할선을 추가한다
4. **Inset (I)**으로 눈, 패널, 버튼 영역을 만든다
5. **Bevel (Ctrl + B)**로 너무 날카로운 모서리를 정리한다

> 💡 기본형은 Edit Mode로 먼저 만든다. Modifier는 그다음 속도를 올려주는 도구다.

### Step 2: Mirror Modifier - 대칭을 가장 빨리 만드는 방법 (15분)

- 로봇처럼 좌우가 비슷한 형태를 만들 때 가장 먼저 떠올리면 좋다
- 한쪽만 만들면 반대쪽이 자동으로 따라와서 작업 시간이 크게 줄어든다

**실습 순서**

1. Cube를 준비한다
2. Edit Mode에서 가운데를 기준으로 한쪽 절반을 지운다
3. `Add Modifier > Mirror`를 추가한다
4. X축 기준 대칭인지 확인한다
5. **Clipping**을 켠다
6. 한쪽만 `Extrude`로 수정하면서 반대쪽이 같이 바뀌는지 확인한다

```plain text
S + X + 0 + Enter
```

- 중심선이 틀어졌을 때 중심 Vertex를 X축 0 위치로 정렬할 때 자주 쓴다

> ⚠️ **Clipping은 꼭 켜두기.** 꺼져 있으면 중심선이 벌어질 수 있다.

### Step 3: Subdivision Surface + Solidify (20분)

#### Subdivision Surface

- 메쉬를 더 잘게 나눠서 표면을 부드럽게 보여준다
- 박스로 시작해도 둥근 몸체 느낌을 만들 수 있다
- 너무 많이 올리면 무거워지니 작업 중에는 낮게 둔다

**기본 설정**

- Viewport Level: `1` 또는 `2`
- Render Level: `2` 또는 `3`

```plain text
Ctrl + 1
Ctrl + 2
Ctrl + 3
```

- `Shade Smooth`를 함께 쓰면 더 자연스럽게 보인다
- 날카롭게 유지할 Edge는 `Shift + E`로 **Edge Crease**를 준다

#### Solidify

- 납작한 면에 **두께**를 준다
- 로봇 외장, 갑옷, 날개, 얇은 패널을 만들 때 자주 쓴다

| 파라미터 | 의미 | 처음 써볼 값 |
|----------|------|---------------|
| Thickness | 두께 | `0.01 ~ 0.1` |
| Offset | 안쪽 / 중앙 / 바깥쪽 방향 | `-1 / 0 / 1` 비교 |
| Even Thickness | 두께를 균일하게 유지 | 켜두는 편이 좋다 |

### Step 4: Array + Boolean (20분)

#### Array

- 같은 오브젝트를 규칙적으로 반복한다
- 손가락 마디, 척추, 볼트 패턴, 계단 구조에 좋다

**기본 실습**

1. Cube에 Array를 추가한다
2. Count를 `5`로 바꾼다
3. Relative Offset의 X값을 `1.5`로 바꾼다
4. Y나 Z로도 바꿔서 가로, 세로, 계단형 반복을 비교한다

#### Boolean

- 두 오브젝트를 **합치거나**, **빼거나**, **겹치는 부분만 남길 때** 쓴다
- 구멍, 소켓, 패널 홈을 만들 때 특히 자주 쓴다

| 연산 | 의미 | 자주 쓰는 상황 |
|------|------|----------------|
| Union | 합치기 | 파츠를 하나의 덩어리처럼 만들기 |
| Difference | 빼기 | 구멍, 소켓, 홈 만들기 |
| Intersect | 겹친 부분만 남기기 | 특정 교차 형태 추출 |

**기본 실습**

1. 바디가 될 오브젝트를 준비한다
2. 커터 역할로 쓸 Cylinder 또는 Cube를 겹치게 놓는다
3. 바디 오브젝트에 Boolean을 추가한다
4. Operation을 **Difference**로 바꾼다
5. Object에서 커터 오브젝트를 지정한다

### Step 5: 필수 추가 Modifier + 선택 심화 (15분)

#### 필수로 알아둘 것

#### Bevel Modifier

- Edit Mode의 `Ctrl + B`를 전체 모서리에 비파괴로 적용하는 느낌이다
- 전체적으로 살짝 둥근 하드서피스 느낌을 볼 때 편하다
- 특정 엣지 몇 개는 `Ctrl + B`, 전체 외장은 `Bevel Modifier`처럼 나눠 생각하면 덜 헷갈린다

#### Weighted Normal

- 형태는 괜찮은데 음영이 지저분해 보일 때 정리한다
- 특히 Bevel Modifier와 같이 쓰면 로봇 외장이 더 깔끔하게 보인다
- 쉽게 말하면 **모양을 바꾸기보다 빛이 닿는 느낌을 정리하는 도구**다

#### 선택으로 써볼 것

#### Simple Deform

- 전체를 휘게(Bend), 비틀게(Twist), 가늘게(Taper) 만들 수 있다
- 안테나, 꼬리, 손잡이, 아치형 구조에 빠르게 변화를 줄 때 좋다

#### Decimate

- 너무 무거운 메쉬를 가볍게 줄인다
- 지금 주차 필수는 아니지만, 나중에 AI 3D 생성 메쉬를 다룰 때 특히 자주 쓰게 된다

#### Join / Separate

- 로봇 모델은 작업하다 보면 머리, 팔, 안테나, 손 파츠처럼 덩어리가 많아진다
- 따로 관리할 파츠는 `P > Selection`으로 분리하고, 함께 갈 파츠는 `Ctrl + J`로 합친다
- 이후 리깅이나 애니메이션까지 생각하면 파츠 정리를 일찍 해두는 편이 편하다

#### Apply 타이밍

- `Ctrl + A > All Transforms`는 Modifier 전, 작업 중간중간 자주 확인한다
- `Modifier Apply`는 수정 가능성을 거의 다 쓴 뒤 마지막에만 한다
- 쉽게 말하면 `Ctrl + A`는 **정리**, `Apply Modifier`는 **확정**이다

### Step 6: 종합 실습 - 로봇 기본 형태 완성하기 (20분)

**1. Edit Mode로 기본형 만들기**

- `Extrude`, `Loop Cut`, `Inset`, `Bevel`로 몸통과 머리, 팔, 다리 위치를 잡는다

**2. Mirror로 좌우 대칭 맞추기**

- 절반만 남기고 Mirror를 건다
- Clipping을 켜고 한쪽만 수정한다

**3. Subdivision Surface로 큰 덩어리 다듬기**

- 몸통과 머리의 큰 곡면을 부드럽게 만든다
- 필요한 Edge는 `Shift + E`로 너무 둥글어지지 않게 잡는다

**4. Solidify, Array, Boolean으로 디테일 추가**

- 얇은 패널에는 Solidify
- 반복 파츠에는 Array
- 눈 구멍이나 환기구에는 Boolean

**5. 필수 추가 Modifier는 꼭 확인하기**

- Bevel Modifier 또는 Weighted Normal은 꼭 한 번 확인한다

**6. Join / Separate와 Apply 타이밍 같이 보기**

- 파츠를 나눌지 묶을지 한 번 정리해본다
- `Ctrl + A`와 `Modifier Apply`를 다르게 이해한다

**7. 선택 심화 Modifier는 여유 있으면 실험하기**

- Simple Deform, Decimate는 시간이 남으면 시도해본다

> 🔑 이번 주 핵심은 “전부 손으로 만들기”가 아니다. **직접 만들 부분은 Edit Mode로**, **대칭, 반복, 곡면, 두께는 Modifier로** 처리하는 감각을 익히는 것이 중요하다.

## ⚠️ 흔한 실수와 해결법

| 실수 | 원인 | 해결법 |
|------|------|--------|
| Extrude를 취소했는데 메시가 이상함 | 중복 Vertex가 남음 | **Ctrl + Z** 또는 **M > Merge by Distance** |
| Mirror 중심선이 벌어짐 | Clipping이 꺼져 있음 | **Clipping 활성화**, 필요하면 **S + X + 0** |
| Subdivision이 너무 둥글어짐 | 모든 Edge가 같이 부드러워짐 | **Shift + E**로 Crease 주기, Loop Cut 추가 |
| Boolean 결과가 비거나 이상함 | 겹침이 애매하거나 메쉬 상태가 좋지 않음 | 커터가 실제로 겹치는지 확인, **Non-Manifold** 검사 |
| 두께나 간격이 이상함 | Scale이 정리되지 않음 | **Ctrl + A > All Transforms** |
| Modifier를 너무 일찍 확정함 | Apply를 초반에 해버림 | **Modifier Apply는 마지막에만** |
| 음영이 지저분해 보임 | Normal 정리가 덜 됨 | **Weighted Normal** 또는 Shade 관련 옵션 확인 |

## 과제

- **제출:** Discord `#week03-assignment` 채널
- **내용:** Edit Mode와 Modifier를 함께 사용한 로봇 또는 캐릭터 기본 형태 제작
- **형식:** 스크린샷 3장 + 사용한 Modifier 목록 + 한줄 코멘트
  - 1장: Edit Mode로 기본형을 잡는 과정 화면
  - 2장: Modifier Stack이 보이는 화면
  - 3장: 최종 형태 화면
- **기한:** 다음 수업 전까지

## 핵심 정리

| 개념 | 핵심 내용 |
|------|-----------|
| Edit Mode | 점, 선, 면을 직접 편집하며 기본형을 만든다 |
| Modifier | 원본을 보존한 채 결과를 바꾸는 비파괴 방식 |
| Mirror | 대칭 모델링의 기본. Clipping 꼭 켜기 |
| Subdivision Surface | 표면을 부드럽게 만든다. Ctrl+1/2/3으로 레벨 변경 |
| Solidify | 납작한 면에 두께를 준다 |
| Array | 같은 오브젝트를 규칙적으로 반복한다 |
| Boolean | 합치기, 빼기, 교차로 디테일을 만든다 |
| Bevel Modifier | 모서리를 비파괴로 둥글게 만든다 |
| Weighted Normal | 하드서피스 음영을 정리한다 |
| Join / Separate | 파츠를 묶거나 분리해 관리한다 |
| Apply Timing | `Ctrl + A`는 정리, `Modifier Apply`는 마지막 확정 |
| Simple Deform | 전체를 휘게, 비틀게, 가늘게 만든다 |
| Decimate | 무거운 메쉬를 가볍게 줄인다 |

## 📋 프로젝트 진행 체크리스트

- [ ] Edit Mode로 기본 몸체 형태를 만들었다
- [ ] Mirror Modifier로 좌우 대칭을 맞췄다
- [ ] Subdivision Surface로 큰 덩어리를 다듬었다
- [ ] Solidify, Array, Boolean 중 1개 이상 추가로 사용했다
- [ ] Bevel Modifier 또는 Weighted Normal을 확인했다
- [ ] Join 또는 Separate로 파츠를 정리해봤다
- [ ] (선택) Simple Deform 또는 Decimate를 시도했다
- [ ] Modifier Stack 순서를 정리했다
- [ ] `Ctrl + A`로 Transform을 정리했다
- [ ] 결과 스크린샷 3장을 저장했다

## 참고 자료

- [Blender Manual - Modifiers Introduction](https://docs.blender.org/manual/en/latest/modeling/modifiers/introduction.html)
- [Blender Manual - Mirror Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/mirror.html)
- [Blender Manual - Subdivision Surface Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html)
- [Blender Manual - Solidify Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/solidify.html)
- [Blender Manual - Array Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/array.html)
- [Blender Manual - Boolean Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html)
- [Blender Manual - Bevel Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html)
- [Blender Manual - Weighted Normal Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weighted_normal.html)
- [Blender Manual - Simple Deform Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/simple_deform.html)
- [Blender Manual - Decimate Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/decimate.html)
