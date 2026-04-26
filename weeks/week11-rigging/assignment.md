# Week 11 과제: 기초 리깅 적용

## 학습 목표

- [ ] Armature를 생성하고 Bone 구조를 설계할 수 있다
- [ ] 로봇/캐릭터 모델에 리깅을 적용할 수 있다
- [ ] Weight Painting을 확인하고 조정할 수 있다
- [ ] Pose Mode에서 2가지 이상의 포즈를 잡을 수 있다

## 과제 내용

자신의 로봇 또는 캐릭터 모델에 기초 리깅을 적용하고, 2가지 이상의 서로 다른 포즈를 잡아 제출한다.

### 제작 과정

1. **Armature 설계:** 자신의 모델에 맞는 Bone 구조 계획
   - 로봇: 관절마다 개별 Bone 배치 (기계 리깅)
   - 캐릭터: 인체 구조에 맞는 Bone 배치 (캐릭터 리깅)
2. **Armature 생성:** Shift+A > Armature로 Bone 생성 후 E(Extrude)로 연장
3. **메쉬 연결:** 메쉬 선택 > Armature 선택 > Ctrl+P > Armature Deform
   - 로봇: With Empty Groups 후 수동 Vertex Group Assign
   - 캐릭터: With Automatic Weights
4. **Weight Painting 확인:** Weight Paint 모드에서 각 Bone의 영향 범위 확인 및 조정
5. **포즈 잡기:** Pose Mode에서 최소 2가지 서로 다른 포즈 완성
6. **스크린샷 촬영:** 각 포즈의 렌더 이미지 + Armature 와이어프레임 스크린샷

### 포즈 아이디어 (참고)

- 인사하는 포즈 (한쪽 팔 들기)
- 걷는 포즈 (팔다리 교차)
- 앉아있는 포즈
- 물건을 집는 포즈
- 전투/액션 포즈
- 춤추는 포즈

### 팁

- Viewport Display > In Front를 체크하면 Armature가 메쉬 위에 항상 보임
- Bone 이름을 의미 있게 지정하면 나중에 작업이 편리함 (예: Arm.L, Arm.R)
- 포즈를 잡을 때 Alt+R로 초기화하면서 여러 번 시도해 보기
- Armature 와이어프레임 보이기: Viewport Overlays에서 확인

## 제출 방법

- **제출처:** 본인 학생 페이지
- **형식:**
  - 포즈 이미지 2장 (서로 다른 포즈, Viewport 또는 렌더)
  - Armature 와이어프레임이 보이는 스크린샷 1장 (Bone 구조 확인용)
  - 한줄 코멘트 (리깅 과정에서 어려웠던 점 또는 느낀 점)
- **기한:** 다음 수업 전까지

## 평가 기준

| 항목 | 비율 | 세부 기준 |
|------|------|-----------|
| Bone 구조 적절성 | 35% | 모델에 맞는 Bone 배치인가, Parent-Child 관계가 올바른가, Bone 이름이 적절한가 |
| Weight Painting 품질 | 35% | 각 Bone의 영향 범위가 적절한가, 파츠가 올바르게 움직이는가, 메쉬 깨짐이 없는가 |
| 포즈 다양성 | 30% | 2가지 이상의 서로 다른 포즈인가, 자연스러운 포즈인가, 로봇/캐릭터의 특성을 살렸는가 |

## 참고 자료

- [Blender Manual: Armatures](https://docs.blender.org/manual/en/latest/animation/armatures/index.html)
- [Blender Manual: Weight Painting](https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/index.html)
- [Blender Manual: Posing](https://docs.blender.org/manual/en/latest/animation/armatures/posing/index.html)
