# Week 10 과제: 3~5초 간단한 움직임 애니메이션

## 학습 목표

- [ ] Keyframe을 삽입하여 오브젝트에 움직임을 부여할 수 있다
- [ ] Graph Editor에서 이징을 조절하여 자연스러운 동작을 만들 수 있다
- [ ] 애니메이션 12원칙 중 핵심 원리를 실제 작업에 적용할 수 있다
- [ ] 완성된 애니메이션을 영상 또는 GIF로 출력할 수 있다

## 과제 내용

자신의 로봇 또는 캐릭터 모델에 **3~5초 분량의 간단한 움직임 애니메이션**을 만들어 제출한다.

### 동작 선택 (아래 중 하나 이상)

자유롭게 선택하되, 최소 하나 이상의 동작을 포함해야 한다:

- **손/팔 흔들기:** 인사하듯 팔을 좌우로 흔드는 동작
- **고개 돌리기:** 좌우 또는 상하로 머리를 움직이는 동작
- **점프:** 위로 뛰어오르고 착지하는 동작 (Squash & Stretch 적용)
- **몸체 회전:** 360도 또는 특정 각도로 회전하는 동작
- **다가오기/물러나기:** 카메라를 향해 다가오거나 물러나는 동작
- **자유 동작:** 위에 없는 창의적인 동작도 환영

### 필수 요소

1. **Keyframe:** 최소 4개 이상의 Keyframe 사용
2. **이징:** Graph Editor에서 Linear이 아닌 Bezier 또는 프리셋 이징 적용
3. **12원칙 적용:** Ease In/Out, Anticipation, Timing 중 하나 이상 의식적으로 적용
4. **길이:** 3~5초 (24fps 기준 72~120프레임)

### 출력 방법

#### MP4 영상 출력

1. Output Properties > Output 경로 설정
2. File Format: **FFmpeg Video**
3. Container: MPEG-4
4. Video Codec: H.264
5. 해상도: 1280x720 이상
6. **Ctrl+F12** (Render Animation)

#### GIF 변환 (선택)

1. MP4 파일을 GIF로 변환하고 싶은 경우:
   - [ezgif.com](https://ezgif.com/video-to-gif) 등 온라인 변환 도구 활용
   - 또는 FFmpeg 커맨드: `ffmpeg -i input.mp4 -vf "fps=12,scale=480:-1" output.gif`
2. GIF는 Discord에서 바로 재생되어 공유하기 편리

## 제출 방법

- **제출처:** Discord #week10-assignment 채널
- **형식:**
  - MP4 영상 파일 또는 GIF 파일 1개
  - 한줄 코멘트 (어떤 동작을 만들었는지, 어떤 이징을 적용했는지)
- **기한:** 다음 수업 전까지

## 평가 기준

| 항목 | 비율 | 세부 기준 |
|------|------|-----------|
| 자연스러운 움직임 | 40% | 움직임이 부자연스럽지 않은가, 이징이 적절히 적용되었는가, 기계적 느낌이 아닌 유기적 동작인가 |
| Keyframe/이징 활용 | 30% | Keyframe 수와 배치가 적절한가, Graph Editor에서 커브를 조절했는가, 12원칙을 의식적으로 적용했는가 |
| 창의성 | 30% | 동작 선택이 재미있는가, 단순한 이동을 넘어선 표현이 있는가, 로봇/캐릭터의 성격이 느껴지는가 |

## 팁

- **Origin Point 확인:** 회전 애니메이션을 만들 때는 반드시 회전 중심(Origin)이 올바른 위치인지 확인
- **Anticipation 추가:** 주 동작 전에 작은 예비 동작을 넣으면 훨씬 자연스러움
- **동작 겹침(Offset):** 여러 파트가 동시에 같은 타이밍으로 움직이면 부자연스러움. 시작 시점을 2~4프레임 어긋나게 배치
- **과감한 이징:** Ease In/Out을 강하게 적용할수록 생동감이 올라감. 너무 미세하면 효과가 느껴지지 않음
- **반복 재생:** Space로 계속 재생하면서 부자연스러운 부분을 찾아 수정

## 참고 자료

- [Blender Manual: Animation](https://docs.blender.org/manual/en/latest/animation/index.html)
- [Blender Manual: Graph Editor](https://docs.blender.org/manual/en/latest/editors/graph_editor/index.html)
- [12 Principles of Animation](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation) - Disney 애니메이션 12원칙
- [Blender Animation Tutorial (YouTube)](https://www.youtube.com/results?search_query=blender+animation+basics+beginner) - 애니메이션 기초 영상
- [ezgif.com](https://ezgif.com/video-to-gif) - 온라인 MP4→GIF 변환 도구
