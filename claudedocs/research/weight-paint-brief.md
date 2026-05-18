# 리서치 브리프: 웨이트 페인트 (Weight Paint)
> 생성일: 2026-05-18 | Blender 5.0 기준

---

## 1. 공식 정의

- **영문**: "Weight painting is a method to maintain large amounts of weight information in a very intuitive way. It is primarily used for rigging meshes, where the vertex groups are used to define the relative bone influences on the mesh." (Blender Manual)
- **한글 풀이**: 웨이트 페인트는 메쉬의 각 버텍스(꼭짓점)가 아머튜어 본(Bone)에 얼마나 영향을 받는지를 그림 그리듯이 직접 칠해서 지정하는 작업이에요. 값이 1(빨간색)에 가까울수록 해당 본의 움직임을 100% 따라가고, 0(파란색)에 가까울수록 전혀 따라가지 않아요.
- **공식 문서**: [Blender Manual — Weight Paint](https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/index.html)

---

## 2. 핵심 파라미터

| 파라미터 | 기본값 | 설명 | 학생에게 중요한 이유 |
|---------|-------|------|-------------------|
| Weight | 1.0 | 브러시가 칠하는 웨이트 값 (0.0~1.0) | 이 값을 낮추지 않으면 항상 최대 영향(빨간색)으로만 칠해져요 |
| Radius | 50px | 브러시 크기 | 세밀한 부분(손가락, 입 주변)과 큰 면적(몸통)에서 수시로 바꿔야 해요 |
| Strength | 0.5 | 한 번 칠할 때 얼마나 깊이 적용할지 (브러시 불투명도와 같아요) | 낮으면 여러 번 덧칠해서 점진적으로 조절 가능해요 |
| Falloff | Smooth | 브러시 가장자리가 얼마나 부드럽게 감소할지 | 딱딱한 경계선이 생기는 원인이에요 |
| Auto Normalize | Off | 칠할 때마다 모든 본의 웨이트 합이 자동으로 1.0이 되게 유지 | 켜두면 한 본에 웨이트를 더하면 다른 본에서 자동으로 빠져요 |
| Front Faces Only | Off | 보이는 면만 칠하고 뒤쪽 면은 칠하지 않음 | 끄면 메쉬를 관통해서 반대쪽까지 칠해지는 문제가 생겨요 |
| X Mirror | Off | X축 기준 대칭 편집 | 양쪽 대칭 캐릭터는 켜두면 작업 시간이 절반으로 줄어요 |

---

## 3. 단축키

| 키 | 동작 | 컨텍스트 | 비고 |
|----|------|---------|------|
| Ctrl + Tab | 웨이트 페인트 모드 진입/전환 | 오브젝트 모드에서 | 메쉬가 선택된 상태여야 해요 |
| Tab | 에디트 모드로 전환 | 웨이트 페인트 모드에서 | 버텍스 직접 편집 시 사용 |
| Ctrl + Shift + LMB | 본 선택 (버텍스 그룹 전환) | 웨이트 페인트 모드에서 | Blender 4.0 이후 변경됨. 이전 버전은 Ctrl + LMB |
| F | 브러시 크기 조절 | 페인팅 중 | 마우스 드래그로 조절 |
| Shift + F | 브러시 강도(Strength) 조절 | 페인팅 중 | |
| G | 그라디언트 도구 활성화 | 웨이트 페인트 모드에서 | 선형/방사형 그라디언트로 칠해요 |
| Ctrl + LMB | Subtract 모드로 칠하기 | 페인팅 중 | 현재 브러시 모드와 무관하게 웨이트를 빼는 방향으로 칠해요 |
| Shift + LMB | Blur/Smooth 효과 | 페인팅 중 | 경계를 부드럽게 섞어줘요 |

---

## 4. 연관 개념 그래프

### 선수 지식 (이걸 모르면 이해 불가)

- **버텍스 그룹 (Vertex Group)**: 웨이트 페인트가 실제로 수정하는 대상이에요. 각 버텍스 그룹은 특정 본의 이름과 연결되어 있어요. 그룹이 없으면 아무것도 칠 수 없어요.
- **아머튜어 (Armature)**: 본(Bone)의 집합체예요. 웨이트 페인트는 메쉬와 아머튜어를 연결하는 다리 역할을 해요.
- **본 (Bone)**: 아머튜어를 구성하는 개별 관절이에요. 본 이름 = 버텍스 그룹 이름이어야 연결이 돼요.
- **오브젝트 모드 / 에디트 모드**: 오브젝트 모드에서 페어런팅(Parenting)으로 메쉬와 아머튜어를 연결한 뒤에야 웨이트 페인트가 의미를 가져요.

### 연결 개념 (함께 쓰이는 것)

- **Automatic Weights (자동 웨이트)**: Ctrl + P → "With Automatic Weights"로 블렌더가 뼈대 위치를 기반으로 초기 웨이트를 자동 계산해줘요. 이걸 시작점으로 삼고 웨이트 페인트로 수정하는 게 일반 워크플로우예요.
- **포즈 모드 (Pose Mode)**: 웨이트 페인트 결과를 확인할 때 아머튜어를 포즈 모드로 움직여서 테스트해요. 웨이트 페인트 도중에 포즈 모드와 번갈아 쓰는 경우가 많아요.
- **Normalize All**: 모든 버텍스 그룹의 합이 1이 되도록 일괄 정규화해줘요. 자동 웨이트 적용 후 정리할 때 사용해요.
- **Mirror Modifier**: X Mirror 옵션과 함께 쓰면 좌우 대칭 캐릭터 작업이 편해지는데, Mirror Modifier가 적용된 상태면 동작이 달라질 수 있어요.

### 심화 (알면 이해가 깊어지는 것)

- **웨이트 정규화 원리**: 블렌더는 애니메이션 계산 시 모든 본의 웨이트 합이 1.0이 되도록 내부적으로 항상 정규화해요. 그래서 합이 1이 아니어도 실제 결과에 차이가 없는 경우가 많아요. 하지만 Auto Normalize를 켜두면 직관적인 합산 제어가 가능해요.
- **Heat Map 알고리즘**: Automatic Weights가 쓰는 알고리즘이에요. 본과 메쉬 표면의 거리를 기반으로 열전도 방식처럼 웨이트를 퍼뜨려요. 메쉬에 구멍이 있거나 구조가 복잡하면 실패해요.
- **Vertex Weight 전달 (Data Transfer)**: 이미 웨이트가 적용된 메쉬에서 다른 메쉬로 웨이트를 복사하는 방법이에요. 비슷한 캐릭터 변형에 유용해요.

---

## 5. 학생 혼란 포인트

| # | 질문 (실제) | 출처 | 핵심 원인 | 검증된 답변 |
|---|-----------|------|----------|-----------|
| 1 | "웨이트 빼려고 칠하는데 오히려 다른 색이 더 진해져요" | Blender Artists, cgcookie | Auto Normalize가 켜져 있으면 한 본의 웨이트를 빼는 만큼 다른 본에 자동으로 더해져요 | Auto Normalize는 합을 1로 유지하기 때문에 다른 그룹이 올라가는 게 정상이에요. Subtract로 칠할 때는 다른 그룹도 같이 확인해야 해요 |
| 2 | "반대쪽 팔까지 같이 칠해져요" | DCinside 블렌더 갤, arca.live | Front Faces Only 옵션이 꺼져 있어서 메쉬를 관통해 반대면도 칠해짐 | 브러시 옵션에서 Front Faces Only를 켜면 보이는 면만 칠해져요 |
| 3 | "Ctrl + 클릭으로 뼈대가 선택이 안 돼요" | Blender Artists (4.1 관련 스레드) | Blender 4.0에서 단축키가 변경됨 | 4.0 이후는 Ctrl + Shift + LMB로 바뀌었어요. 버전을 확인해야 해요 |
| 4 | "Normalize All을 눌렀더니 잠근 그룹도 바뀌었어요" | Blender developer tracker (T29431) | Normalize All이 Lock 상태를 무시하는 버그/설계 문제가 존재함 | Normalize All 전에 잠그지 않고, Lock을 건 상태에서는 Deform 필터로 전환 후 진행하는 게 안전해요 |
| 5 | "자동 웨이트 적용 시 오류가 나요 (Heat Weighting Failed)" | 국내 커뮤니티 다수, blender.pe.kr | 메쉬에 구멍, 비다양체(Non-manifold) 면, 겹친 버텍스가 있으면 Heat Map 알고리즘이 실패해요 | 에디트 모드에서 Mesh > Clean Up > Merge by Distance 실행 후 다시 시도해요 |
| 6 | "웨이트 페인트 없이 숫자로 바로 지정하고 싶어요" | DCinside 블렌더 갤 | 에디트 모드에서 버텍스 선택 후 수치 입력 방법을 모름 | 에디트 모드 → 버텍스 선택 → Properties > Vertex Groups > Assign 버튼 옆에 Weight 수치 직접 입력 가능해요 |

---

## 6. 흔한 실수 & 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| 칠해도 변화가 없음 | 버텍스가 없거나 버텍스 그룹이 선택되지 않은 상태 | 올바른 버텍스 그룹이 Properties 패널에서 선택되어 있는지 확인 |
| 움직임이 이상하게 늘어남 | 한 버텍스에 여러 본이 과도하게 영향을 줌 | Weight > Normalize All로 정규화 후 개별 그룹을 확인 |
| 양쪽이 대칭으로 안 칠해짐 | X Mirror 옵션이 꺼짐, 또는 버텍스 그룹 이름에 ".L" / ".R" 접미사 없음 | 그룹 이름을 "Arm.L", "Arm.R" 형식으로 맞추고 X Mirror 활성화 |
| 특정 영역이 전혀 움직이지 않음 | 해당 버텍스에 어떤 본도 웨이트가 없음 (파란색 = 0) | 해당 본의 버텍스 그룹을 선택하고 웨이트를 낮은 값(0.1~0.3)이라도 칠해줘요 |
| Automatic Weights 적용 후 형태가 엉망 | 메쉬 밀도가 너무 낮거나, 본 위치가 메쉬 외부에 있음 | 메쉬를 Subdivide해서 버텍스 수를 늘리거나, 본 위치를 메쉬 내부로 이동 |
| 페인트 모드 진입 자체가 안 됨 | 선택된 오브젝트가 메쉬가 아님 (아머튜어, 카메라 등이 선택됨) | 메쉬 오브젝트만 선택한 상태에서 모드 변경 |

---

## 7. 추천 비유 후보

1. **리모컨 채널 배정** — 여러 TV(버텍스)에 리모컨(본)이 얼마나 영향을 미치는지 세기를 조절하는 것이에요. 한 TV가 여러 리모컨에 반응할 수 있고, 각각의 반응 강도를 칠로 정하는 거예요. "웨이트"의 수치 개념을 직관적으로 이해할 수 있어요.
2. **수면 마취제 농도 지도** — 수술 전 마취 주사를 부위별로 다르게 주는 것처럼, 본이 "움직여!" 하고 신호를 보낼 때 각 버텍스가 그 신호에 얼마나 깊이 반응하는지를 색으로 표현하는 거예요. 빨간 부분은 마취 100%, 파란 부분은 마취 0%라서 전혀 움직이지 않아요. 영향력의 "강도"와 "범위" 개념을 동시에 이해시킬 수 있어요.
3. **자석 인력 지도** — 본이 자석이고 버텍스가 쇳조각이에요. 빨간 구역은 강하게 달라붙고, 파란 구역은 자석이 지나가도 반응하지 않아요. 공간적 거리와 영향 강도를 자연스럽게 연결하는 비유예요. 단, 블렌더의 웨이트는 거리로만 결정되는 게 아니라 사람이 직접 칠한다는 점을 보완 설명해야 해요.

---

## 8. 크로스체크 로그

| 주장 | 소스 | 검증 | 결과 |
|------|------|------|------|
| 파란색=0, 빨간색=1 (cold-to-hot 색상 체계) | Blender Manual (2.81), 검색 결과 다수 | 여러 독립 출처 일치 | 확인 |
| Blender 4.0에서 뼈 선택 단축키가 Ctrl+LMB에서 Ctrl+Shift+LMB로 변경 | polyfable.com, Blender Artists 포럼 | 공식 이슈 트래커 및 커뮤니티 일치 | 확인 |
| Auto Normalize는 합이 1이 되도록 실시간으로 다른 그룹을 조정함 | Blender Manual (Options), cgcookie | 동작 방식 설명 일치 | 확인 |
| Normalize All은 Lock 상태를 무시하는 문제 있음 | developer.blender.org T29431 | 공식 이슈 트래커에 보고된 내용 | 확인 (버그/설계 의도 논쟁 있음) |
| Automatic Weights 실패 원인: Non-manifold 메쉬 | 커뮤니티 다수 | 국내외 여러 사례 일치 | 확인 |
| Front Faces Only 옵션으로 관통 칠 방지 가능 | 검색 결과 요약, 블렌더 갤러리 | 원리상 일치 | 확인 (Blender 공식 문서 직접 접근 불가로 2.81 기준 간접 확인) |

---

**참고 출처**

- [Blender Manual — Weight Paint Index](https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/index.html)
- [Blender Manual — Editing (5.1)](https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/editing.html)
- [Selecting Bones in Weight Paint Mode — Polyfable](https://polyfable.com/tutorials/selecting-bones-in-weight-paint-mode-blender-4-0)
- [Normalize All Bug — Blender Developer T29431](https://developer.blender.org/T29431)
- [Auto Normalize Bug — Blender Projects #78613](https://developer.blender.org/T78613)
- [웨이트 페인팅 — blender.pe.kr](https://blender.pe.kr/867)
- [DCinside 블렌더 갤러리 — 뼈대 선택 안됨](https://m.dcinside.com/board/blender/31202)
- [Artisticrender — How to Weight Paint in Blender](https://artisticrender.com/how-to-weight-paint-in-blender/)
