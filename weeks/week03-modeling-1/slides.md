---
marp: true
theme: rpd
paginate: true
---

# Week 03: 기초 모델링 1

## Edit Mode + Modifier

2026 Spring | 인하대학교 | 송지희

---

## 이번 주 핵심

- **Edit Mode:** 점, 선, 면을 직접 만져서 기본형 만들기
- **Modifier:** 원본은 살리고 결과만 바꾸며 빠르게 다듬기
- **파츠 정리와 Apply 타이밍**도 같이 익히기
- 이번 주는 **손으로 만들고 Modifier로 정리하는 흐름**을 익혀요

---

## Edit Mode 도구 4개

| 도구 | 비유 | 활용 |
|------|------|------|
| Extrude (E) | 점토를 잡아당기기 | 팔, 다리, 안테나 |
| Loop Cut (Ctrl + R) | 케이크에 칼집 넣기 | 분할선, 관절 |
| Inset (I) | 면 안쪽에 작은 면 하나 더 | 눈, 패널, 버튼 |
| Bevel (Ctrl + B) | 모서리를 살짝 깎기 | 기계 디테일, 부드러운 모서리 |

---

## Modifier란?

- 필터처럼 얹는 기능
- 원본 메쉬를 바로 망가뜨리지 않음
- 숫자를 바꾸거나 끄고 켜며 실험 가능
- 렌치 아이콘 탭에서 추가

**Non-destructive = Apply 전까지 되돌릴 수 있음**

---

## 핵심 Modifier 5개

| Modifier | 한 줄 설명 |
|----------|-------------|
| Mirror | 한쪽만 만들면 반대쪽이 자동 생성 |
| Subdivision Surface | 각진 형태를 부드럽게 |
| Solidify | 납작한 면에 두께 추가 |
| Array | 반복 구조를 빠르게 생성 |
| Boolean | 합치기, 빼기, 교차 |

---

## Mirror Modifier

- 로봇, 캐릭터처럼 좌우 대칭인 형태에 필수
- 한쪽만 수정해도 반대쪽이 같이 바뀜
- **Clipping 꼭 켜기**

```plain text
S + X + 0 + Enter
```

중심선이 벌어졌을 때 X축 0으로 다시 정렬

---

## Subdivision Surface

- 메쉬를 더 잘게 나눠서 표면을 부드럽게 보여줌
- **Ctrl + 1 / 2 / 3**으로 레벨 빠르게 변경
- **Shift + E**로 Edge Crease를 주면 필요한 모서리는 날카롭게 유지 가능

---

## Solidify / Array / Boolean

**Solidify**
- 외장 패널, 갑옷, 얇은 판에 두께

**Array**
- 손가락 마디, 척추, 계단, 반복 패턴

**Boolean**
- 구멍, 소켓, 홈, 파츠 결합

---

## 필수로 알아둘 추가 Modifier

| Modifier | 어디에 좋은가 |
|----------|----------------|
| Bevel Modifier | 모서리를 비파괴로 둥글게 |
| Weighted Normal | 하드서피스 음영 정리 |

---

## 파츠 정리와 Apply 타이밍

| 항목 | 한 줄 설명 |
|------|-------------|
| Join / Separate | 파츠를 묶거나 나눠서 관리 |
| Ctrl + A | Transform 정리 |
| Modifier Apply | 마지막 확정 단계에서만 |

---

## 선택으로 써볼 Modifier

| Modifier | 어디에 좋은가 |
|----------|----------------|
| Simple Deform | 휘기, 비틀기, 가늘게 만들기 |
| Decimate | 너무 무거운 메쉬 가볍게 만들기 |

---

## 영상에서 자주 보이는 작업 순서

1. **G / R / S**로 큰 덩어리 배치
2. **Ctrl + A**로 Transform 정리
3. Edit Mode로 기본형 제작
4. Mirror / Subdivision으로 실루엣 정리
5. Boolean / Inset으로 디테일 추가
6. Bevel Modifier / Weighted Normal로 표면 정리
7. Modifier Apply는 마지막에만

---

## 헷갈리기 쉬운 차이

| 항목 | 한 줄 설명 |
|------|-------------|
| Ctrl + B | 특정 모서리를 직접 깎기 |
| Bevel Modifier | 전체 모서리를 비파괴로 정리 |
| Ctrl + A | Modifier 전 Transform 정리 |
| Modifier Apply | 최종 확정 단계에서만 사용 |

---

## 추천 조합

- **Mirror + Subdivision**: 대칭 + 부드러운 몸체
- **Solidify + Array**: 패널 + 반복 구조
- **Boolean + Subdivision**: 홈이나 구멍이 있는 둥근 형태
- **Bevel Modifier + Weighted Normal**: 깔끔한 하드서피스 음영

---

## 종합 실습

1. Cube로 기본 몸체 잡기
2. Extrude, Loop Cut, Inset, Bevel로 기본형 만들기
3. Mirror로 좌우 대칭 맞추기
4. Subdivision Surface로 큰 덩어리 부드럽게
5. Solidify, Array, Boolean으로 디테일 추가
6. Bevel Modifier 또는 Weighted Normal은 꼭 보기
7. Join / Separate와 Apply 타이밍 확인
8. 선택 심화 Modifier는 여유 있으면 실험

---

## 흔한 실수

- 중심선이 벌어짐 → **Clipping 확인**
- 너무 둥글어짐 → **Shift + E** 또는 Loop Cut 추가
- 두께, 간격이 이상함 → **Ctrl + A**
- Apply를 너무 일찍 함 → **Modifier Apply는 마지막에**
- Boolean이 이상함 → 커터가 실제로 겹치는지 확인
- 음영이 지저분함 → **Weighted Normal** 확인
- 파츠 관리가 헷갈림 → **P / Ctrl + J** 확인

---

## 과제

- 스크린샷 3장
  - 과정 화면
  - Modifier Stack 화면
  - 최종 형태 화면
- Edit Mode 도구 3가지 이상
- Modifier 2가지 이상
- 필수 추가 Modifier 1개 확인
- 선택 심화 Modifier: Simple Deform / Decimate
- 한줄 코멘트
