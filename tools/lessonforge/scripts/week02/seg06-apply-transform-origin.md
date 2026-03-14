# Week 02 · Seg 06 — Apply Transform & Origin 설정

**목표 영상 길이:** 7분
**레퍼런스:** 기존 week02 lecture-note Step 3·4 / Blender Guru 도넛 시리즈 모디파이어 전 주의사항
**촬영 도구:** blender-mcp
**RPD 연결:** "이걸 안 하고 모델링하면 나중에 반드시 문제가 생깁니다"

> **핵심 메시지 (Blender Guru 원칙):** "왜 필요한지"를 시각적으로 먼저 보여주고, 그다음에 해결 방법을 알려준다

---

## 화면 큐 (Screen Cues)

| 타임 | 화면 | 나레이션 큐 |
|------|------|------------|
| 0:00 | 오프닝 슬라이드 | 인트로 |
| 0:30 | 큐브 S로 스케일 변경 → Properties에서 Scale 값 확인 | 문제 상황 보여주기 |
| 1:30 | Subdivision Modifier 추가 → 왜곡 현상 시연 | "이게 문제" |
| 2:30 | Ctrl + A > Apply All Transforms | 해결법 |
| 3:00 | Scale이 (1,1,1)로 리셋된 것 확인 | 결과 확인 |
| 3:30 | Origin 개념 시각화 (주황 점) | Origin이란? |
| 4:00 | Right-click > Set Origin > Origin to Geometry | Origin 설정 |
| 5:00 | Origin to 3D Cursor 시연 | 응용 |
| 5:30 | Pivot Point 메뉴 소개 | Pivot Point |
| 6:00 | 정리 슬라이드 | 요약 |
| 6:30 | 아웃트로 + Week 02 전체 마무리 | 마무리 |

---

## TTS 나레이션 스크립트

### [인트로 — 0:00]
이번 영상은 **Apply Transform**과 **Origin** 에 대한 내용입니다.
지금 당장은 왜 필요한지 와닿지 않을 수 있어요.
하지만 이걸 모르고 모델링을 진행하면 나중에 반드시 문제가 생깁니다.
실제로 어떤 문제가 생기는지 먼저 보여드릴게요.

### [문제 상황 보여주기 — 0:30]
큐브를 하나 선택하고, S키로 크기를 2배 정도 키워봅니다.
그 다음 오른쪽 Properties Panel에서 Object Properties 탭을 봅니다.
Transform 섹션에서 Scale 값이 보이죠? (2, 2, 2)로 되어 있어요.

이게 무슨 의미냐면, Blender 내부적으로는 이 오브젝트의 "진짜 크기"가 아직 (1,1,1)이고
그냥 화면에 2배로 크게 그리고 있는 거예요.
겉으로 보기엔 똑같아 보이지만, 내부 데이터는 달라요.

### [문제 발생 시연 — 1:30]
이 상태에서 오른쪽 Properties에서 모디파이어 탭, 즉 렌치 모양 아이콘을 클릭합니다.
Add Modifier에서 Subdivision Surface를 추가해볼게요.

어떻게 됩니까? 형태가 이상하게 비틀리거나 예상과 다르게 나타나죠?
Scale이 적용되지 않은 상태에서 모디파이어를 썼기 때문이에요.

이런 문제가 리깅, 물리 시뮬레이션, GLB 내보내기 할 때도 다 생깁니다.

### [해결법 — 2:30]
해결 방법은 아주 간단합니다.
스케일을 바꾼 뒤에는 **Ctrl + A** 를 눌러서 **Apply All Transforms** 를 선택하세요.
이러면 Blender가 "이 크기가 진짜 크기야"라고 데이터를 업데이트합니다.

실행하고 나면 Scale 값이 (1, 1, 1)로 돌아온 걸 확인할 수 있어요.
오브젝트 크기는 그대로인데 내부 수치가 정리된 거예요.

습관처럼 외워두세요: **모델링 시작 전에는 항상 Ctrl + A → Apply All Transforms!**

### [Origin이란? — 3:30]
이번엔 **Origin** 에 대해 알아봅니다.
뷰포트에서 오브젝트를 보면 주황색 작은 점이 하나 보이죠?
이게 Origin이에요. 오브젝트의 기준점입니다.

이동, 회전, 스케일의 중심이 바로 이 점을 기준으로 이루어집니다.
그래서 Origin이 엉뚱한 곳에 있으면, 회전할 때 오브젝트가 이상하게 돌아가요.

### [Origin 설정 — 4:00]
오브젝트를 선택하고 **우클릭** 하면 컨텍스트 메뉴가 뜹니다.
여기서 **Set Origin** 을 선택하세요.

세 가지 옵션이 있어요:
- **Origin to Geometry**: Origin을 메시의 기하학적 중심으로 이동. 가장 많이 씁니다.
- **Origin to 3D Cursor**: 3D Cursor 위치로 Origin을 이동. 정밀한 배치에 유용해요.
- **Origin to Center of Mass**: 물리적인 질량 중심으로 이동. 시뮬레이션에서 씁니다.

일반적으로 **Origin to Geometry**가 가장 많이 쓰입니다.
오브젝트 편집이 끝난 후 Origin이 중심에서 벗어나 있다면 이걸 써서 정리하세요.

### [Pivot Point — 5:30]
마지막으로 **Pivot Point** 를 소개합니다.
뷰포트 상단 헤더 가운데쯤에 조그만 아이콘이 있어요. 점 세 개 같은 모양이에요.
이게 Pivot Point 설정입니다.

여러 오브젝트를 동시에 회전하거나 스케일 할 때 기준점을 어디로 잡을지 결정해요.
- **Individual Origins**: 각각의 오브젝트 Origin을 기준으로 변환
- **3D Cursor**: 3D Cursor 위치를 기준으로
- **Median Point**: 선택된 오브젝트들의 평균 중간점
기본값인 **Median Point**로 두면 대부분의 경우 잘 작동합니다.

### [정리 — 6:00]
오늘의 핵심 두 가지:
첫 번째, **Ctrl + A → Apply All Transforms**: 모디파이어나 내보내기 전에 반드시!
두 번째, **Right-click → Set Origin to Geometry**: Origin을 항상 오브젝트 중심에 맞추기.

이 두 가지를 습관으로 만들어두면 나중에 발생할 많은 문제를 예방할 수 있습니다.

### [아웃트로 — 6:30]
이번 Week 02 수업이 모두 끝났습니다.
오늘 배운 내용을 정리하면:
Blender 설치 → 프리퍼런스 설정 → UI 구조 이해 → 뷰포트 조작 → Transform 기초 → Apply Transform & Origin.

다음 수업인 Week 03에서는 본격적으로 Edit Mode에 들어가서 로봇 머리를 모델링합니다.
오늘 배운 뷰포트 조작과 Transform이 자연스러워질 때까지 연습해두세요.

---

## 촬영 체크리스트

- [ ] Scale 문제 시연이 명확하게 보일 것 (Subdivision 왜곡)
- [ ] Ctrl+A 메뉴 팝업 화면 확대
- [ ] Scale (2,2,2) → Apply → (1,1,1) 비교를 Properties 패널로 클로즈업

## 편집 메모

- "왜 필요한지"를 문제 시연으로 먼저 보여주는 Blender Guru 스타일 적용
- 차녹 스타일: 핵심만 빠르게, 군더더기 없이
- Week 02 마지막 영상이므로 전체 요약을 포함
- 다음 Week 03 예고 씬 (편집 모드 짧은 티저) 있으면 좋음
