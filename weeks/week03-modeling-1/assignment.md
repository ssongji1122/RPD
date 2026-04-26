# Week 03 과제: Edit Mode + Modifier 로봇 기본 형태

## 과제 개요

Edit Mode의 핵심 도구와 Modifier를 함께 사용해 로봇 또는 캐릭터의 기본 형태를 만듭니다.

## 제출 방법

- **제출처:** 본인 학생 페이지
- **형식:** 스크린샷 3장 + 사용한 Modifier 목록 + 한줄 코멘트
- **기한:** 다음 수업 전까지

## 과제 내용

### 스크린샷 3장

1. **과정 화면:** Edit Mode로 기본형을 잡는 장면
2. **Modifier Stack 화면:** 사용한 Modifier가 보이는 상태
3. **최종 형태 화면:** 자유 각도에서 전체가 보이게 촬영

### 필수 요구사항

- Cube 또는 다른 Primitive에서 시작할 것
- **Edit Mode 도구 3가지 이상** 사용할 것
  - Extrude, Loop Cut, Inset, Bevel 중 선택
- **Modifier 2가지 이상** 사용할 것
  - 기본 5개를 우선 사용: Mirror, Subdivision Surface, Solidify, Array, Boolean
- **필수 추가 Modifier 1가지 이상** 확인하거나 사용해볼 것
  - Bevel Modifier 또는 Weighted Normal
- **작업 흐름 1가지 이상 확인할 것**
  - Join/Separate 또는 Apply 타이밍
- 머리, 몸통, 팔, 다리 또는 그에 준하는 구조가 드러날 것

### 추가 Modifier 기준

- **필수로 알아둘 추가 Modifier**
  - Bevel Modifier
  - Weighted Normal
- **선택 심화 Modifier**
  - Simple Deform
  - Decimate
- 선택 심화 Modifier는 시간이 남을 때 시도하면 충분하다

### 한줄 코멘트

- 어떤 Modifier를 썼는지, 작업하면서 가장 어려웠던 부분이 무엇이었는지 한 줄로 적기

## 평가 기준

| 항목 | 비율 | 설명 |
|------|------|------|
| 도구 활용 | 35% | Edit Mode 도구와 Modifier를 적절히 조합했는가 |
| 형태 완성도 | 35% | 기본 구조와 실루엣이 명확한가 |
| 작업 흐름 이해 | 20% | 대칭, 곡면, 두께, 반복 같은 문제를 적절한 Modifier로 해결했는가 |
| 창의성 | 10% | 자신만의 형태나 디테일을 시도했는가 |

## 팁

- 무리하게 복잡하게 만들기보다 **기본형 + Modifier 흐름**이 보이게 만드는 것이 더 중요하다
- Mirror는 좌우 대칭을 빠르게 잡을 때 가장 먼저 떠올리면 좋다
- Subdivision Surface는 Viewport Level을 너무 높이지 않는 편이 작업이 편하다
- Scale 값이 이상하면 Modifier 결과도 이상해질 수 있으니 **Ctrl + A**를 먼저 확인한다
- **Ctrl + A**와 **Modifier Apply**는 다른 개념이다. Transform 정리는 중간에도 하지만, Modifier Apply는 마지막에만 하는 편이 안전하다
- 파츠가 많아지기 시작하면 **P(Separate)**, **Ctrl + J(Join)**로 정리하는 습관을 같이 들이면 좋다
- 하드서피스 느낌이 필요하면 **Bevel Modifier + Weighted Normal** 조합을 먼저 떠올리면 좋다
- Simple Deform과 Decimate는 선택 심화로 보고, 시간이 남을 때 시도해도 충분하다

## 참고 자료

- [Blender 단축키 모음](../../resources/blender-shortcuts.md)
- [Week 03 강의노트](./lecture-note.md)
