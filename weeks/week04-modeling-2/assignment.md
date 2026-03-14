# Week 04 과제: 로봇 디테일 & 음영 정리

## 학습 목표

- [ ] 기본형 위에 디테일을 더해 완성도를 높일 수 있다
- [ ] `Ctrl + B`와 `Bevel Modifier` 중 알맞은 방식을 골라 사용할 수 있다
- [ ] `Weighted Normal`과 `Apply` 시점을 이해하고 설명할 수 있다

## 과제 내용

Week 03에서 만든 로봇 또는 캐릭터 기본형을 바탕으로, 얼굴/관절/패널 디테일을 추가하고 표면 음영을 정리한다.

### 요구사항

1. **디테일 1곳 이상 추가**
   - Inset, Extrude, Boolean 중 하나 이상 활용
2. **Bevel 계열 1회 이상 사용**
   - `Ctrl + B` 또는 `Bevel Modifier`
3. **Weighted Normal 확인**
   - 실제로 적용해보거나, 적용 전후 차이를 비교
4. **Transform 정리 확인**
   - `Ctrl + A > All Transforms` 점검
5. **Modifier Stack 또는 Transform 확인 화면 포함**

### 제작 과정 예시

1. Week 03 기본형 파일 열기
2. 얼굴, 가슴판, 관절 중 하나를 골라 디테일 추가
3. `Ctrl + B` 또는 `Bevel Modifier`로 모서리 정리
4. `Weighted Normal`로 음영 정리
5. 최종 화면을 여러 각도에서 점검

### 참고 팁

- 작은 부분은 `Ctrl + B`, 전체 외장은 `Bevel Modifier`가 편한 경우가 많다
- `Ctrl + A`, `Modifier Apply`, `Join/Separate`는 3주차 개념을 실제 작업에 다시 적용한다고 생각하면 된다
- 파츠를 따로 움직이거나 관리할 계획이 있으면 `P`로 분리해두는 것이 좋다

## 제출 방법

- **제출처:** Discord `#week04-assignment` 채널
- **형식:**
  - 스크린샷 3장
    - 1장: 디테일 작업 과정
    - 2장: Modifier Stack 또는 Transform 확인 화면
    - 3장: 최종 결과물
  - 사용한 도구/Modifier 목록
  - 한줄 코멘트
- **기한:** 다음 수업 전까지

## 평가 기준

| 항목 | 비율 | 세부 기준 |
|------|------|-----------|
| 디테일 완성도 | 40% | 얼굴, 패널, 관절 등 디테일이 분명하게 보이는가 |
| 도구 이해 | 35% | Bevel, Weighted Normal, Apply 시점을 적절히 이해했는가 |
| 화면 정리 | 25% | 음영과 파츠 구성이 깔끔하게 정리되었는가 |

## 참고 자료

- [Blender 단축키 모음](../../resources/blender-shortcuts.md)
- [Blender Manual - Bevel Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html)
- [Blender Manual - Weighted Normal Modifier](https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weighted_normal.html)
