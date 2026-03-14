# Week 04 과제: Modifier 활용 로봇 형태

## 학습 목표

- [ ] Modifier의 Non-destructive 워크플로우를 실제 모델링에 적용할 수 있다
- [ ] 2개 이상의 Modifier를 조합하여 로봇/캐릭터 형태를 만들 수 있다
- [ ] Modifier Stack 순서의 영향을 이해하고 적절히 구성할 수 있다

## 과제 내용

Modifier를 활용하여 자신의 로봇/캐릭터 형태를 제작한다.

### 요구사항

1. **최소 2개 이상의 Modifier 사용** (아래에서 선택)
   - Subdivision Surface
   - Mirror
   - Solidify
   - Array
   - Boolean
2. **대칭 구조 활용:** Mirror Modifier를 사용한 대칭 모델링 권장
3. **Modifier Stack이 표시된 상태**의 스크린샷 포함

### 제작 과정

1. **기본 형태 잡기:** Cube 또는 기본 도형에서 시작
2. **Mirror Modifier 추가:** 대칭 모델링 설정
3. **Edit Mode에서 모델링:** Extrude, Loop Cut 등으로 형태 완성
4. **추가 Modifier 적용:** Subdivision Surface, Boolean 등으로 디테일 추가
5. **결과 확인:** Shade Smooth 적용, 다양한 각도에서 확인

### 참고 팁

- Mirror + Subdivision Surface 조합이 가장 기본적이고 효과적
- Boolean은 구멍이나 홈을 만들 때 유용하지만, 토폴로지가 복잡해질 수 있음
- Modifier는 Apply하지 않은 상태로 제출 (Non-destructive 상태 유지)

## 제출 방법

- **제출처:** Discord #week04-assignment 채널
- **형식:**
  - 스크린샷 2장
    - 1장: Modifier Stack이 보이는 상태의 작업 화면
    - 2장: 완성된 결과물 (Rendered 또는 Solid 뷰)
  - 사용한 Modifier 목록 및 간단한 설명
  - 한줄 코멘트 (작업 과정에서 느낀 점)
- **기한:** 다음 수업 전까지

## 평가 기준

| 항목 | 비율 | 세부 기준 |
|------|------|-----------|
| Modifier 활용 | 40% | 적절한 Modifier 선택, Stack 순서의 합리성 |
| 완성도 | 30% | 형태의 완성도, 깔끔한 실루엣, 비례감 |
| 창의성 | 30% | 독창적인 디자인, 컨셉과의 연결성 |

## 참고 자료

- [Blender 단축키 모음](../../resources/blender-shortcuts.md)
- [Blender Manual - Modifiers](https://docs.blender.org/manual/en/latest/modeling/modifiers/index.html)
