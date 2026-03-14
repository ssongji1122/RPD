# Week 04: 기초 모델링 2 - Modifier

## 학습 목표

- [ ] Modifier의 개념과 Non-destructive 워크플로우를 이해한다
- [ ] Subdivision Surface, Mirror, Solidify, Array Modifier를 사용할 수 있다
- [ ] Boolean 연산을 활용할 수 있다

## 🔗 이전 주차 복습

- Week 03에서 배운 **Extrude (E)**, **Loop Cut (Ctrl + R)**, **Bevel (Ctrl + B)**를 활용하여 기본 형태를 잡은 상태
- Edit Mode에서의 선택 모드 (Vertex/Edge/Face)와 각종 선택 방법 복습
- Extrude 취소 시 중복 Vertex 문제 → **M > Merge by Distance**로 정리하는 습관
- 이번 주에는 Modifier를 사용하므로, 작업 전 **Apply Transform (Ctrl + A)**이 되어 있는지 반드시 확인

## 이론 (30분)

### Modifier란?

- Non-destructive 워크플로우의 핵심
  - 원본 메쉬를 변경하지 않고 효과를 적용
  - 언제든 파라미터 조절/삭제 가능
  - Properties > Modifier Properties (렌치 아이콘)
- Modifier를 추가하면 원본 데이터는 그대로 유지하면서 결과물만 변경됨
- 최종 확정 전까지 자유롭게 실험 가능

### Modifier Stack

- Modifier는 위에서 아래로 순서대로 적용됨
- Stack 순서가 결과에 영향을 미침
  - 예: Mirror 다음 Subdivision vs Subdivision 다음 Mirror은 결과가 다름
- 드래그로 순서 변경 가능
- 일반적인 권장 순서: Mirror > Subdivision Surface > 기타 Modifier

> 💡 **프로 팁:** Modifier Stack의 순서는 결과에 큰 영향을 미친다. **Mirror를 항상 가장 위에**, Subdivision Surface는 그 아래에 배치하는 것이 일반적이다. 순서를 바꿔가며 결과를 비교해보면 차이를 체감할 수 있다.

## 실습 (90분)

### Subdivision Surface Modifier (20분)

1. 기본 Cube 선택 > Properties > Modifier Properties > Add Modifier > Subdivision Surface
2. Viewport/Render 레벨 설정
   - Viewport: 작업 중 미리보기 해상도 (1~2 권장)
   - Render: 최종 렌더링 해상도 (2~3 권장)
3. 단축키: Ctrl+1 (레벨 1), Ctrl+2 (레벨 2), Ctrl+3 (레벨 3)
4. Smooth Shading과 함께 사용
   - Right-click > Shade Smooth 적용
   - Subdivision + Smooth Shading으로 부드러운 곡면 생성
5. Crease로 날카로운 Edge 유지
   - Edit Mode에서 Edge 선택 > Shift+E로 Crease 값 설정
   - Crease 값이 높을수록 해당 Edge가 날카롭게 유지됨
   - Mean Crease 0.0 (부드러움) ~ 1.0 (날카로움)

> 💡 **프로 팁:** **Ctrl + 숫자키 (1, 2, 3)**로 Subdivision Surface 레벨을 빠르게 변경할 수 있다. 작업 중에는 레벨 1로 가볍게, 확인 시에만 레벨 2~3으로 올려보자. 또한 **Edge Crease (Shift + E)**는 Subdivision에서 날카로운 모서리를 유지하는 핵심 기법이다. 로봇의 기계적인 엣지를 표현할 때 필수적으로 사용된다.

### Mirror Modifier (20분)

1. 대칭 모델링의 핵심 도구
   - 한쪽만 모델링하면 반대쪽이 자동 생성
   - 작업 시간 절반으로 단축
2. 설정 방법
   - Add Modifier > Mirror
   - X/Y/Z 축 선택 (기본: X축)
   - Mirror Object: 대칭 기준이 되는 오브젝트 지정 가능
3. Clipping 옵션
   - 활성화하면 Vertex가 중심선을 넘지 않음
   - 대칭 모델링 시 반드시 켜두는 것을 권장

> 💡 **프로 팁:** Mirror Modifier 사용 시 **Clipping은 반드시 체크**하자. Clipping이 꺼져 있으면 중심선의 Vertex가 반대편으로 넘어가 좌우 대칭이 깨진다. 실수로 깨진 경우, 중심선 Vertex를 선택하고 S + X + 0 + Enter로 X축 위치를 0으로 정렬할 수 있다.
4. 실습: 로봇 모델링
   - Cube에서 시작, 한쪽 절반을 삭제 (Edit Mode > X축 기준 한쪽 선택 > Delete)
   - Mirror Modifier 추가
   - 한쪽만 Edit Mode에서 모델링 > 자동 대칭 확인

### Solidify Modifier (10분)

1. 면(Face)에 두께를 추가하는 Modifier
   - 얇은 Panel, 갑옷, 외장재 표현에 유용
2. 주요 파라미터
   - Thickness: 두께 값 설정
   - Offset: -1 (안쪽) ~ 0 (중앙) ~ 1 (바깥쪽)
   - Even Thickness: 균일한 두께 유지
3. 활용 예시
   - 로봇의 외장 패널
   - 갑옷이나 보호대
   - 얇은 구조물 (날개, 안테나 등)

### Array Modifier (10분)

1. 오브젝트를 규칙적으로 복제하는 Modifier
   - 반복되는 패턴을 효율적으로 생성
2. Offset 타입
   - Relative Offset: 오브젝트 크기 기준 상대적 거리
   - Constant Offset: 절대적 거리값 (미터 단위)
   - Object Offset: 다른 오브젝트의 Transform을 기준으로 배치
3. Count: 복제 개수 설정
4. 활용 예시
   - 로봇의 관절 마디
   - 손가락 관절
   - 척추/등뼈 구조
   - 반복되는 장식 패턴

### Boolean Modifier (15분)

1. 두 오브젝트 간의 논리 연산
   - Union (합치기): 두 오브젝트를 하나로 결합
   - Difference (빼기): 한 오브젝트에서 다른 오브젝트의 형태를 제거
   - Intersect (교차): 두 오브젝트가 겹치는 부분만 남김
2. 사용 방법
   - 대상 오브젝트 선택 > Add Modifier > Boolean
   - Operation 선택 (Union/Difference/Intersect)
   - Object에서 연산에 사용할 오브젝트 선택
3. 활용 예시
   - Difference: 로봇 바디에 구멍 뚫기, 소켓 만들기
   - Union: 여러 파츠를 하나로 합치기
   - Intersect: 특정 형태의 교차 부분만 추출
4. 주의사항
   - Boolean 연산 후 메쉬 정리가 필요할 수 있음
   - Ngon(5각형 이상의 면)이 생성될 수 있음
   - Apply 후 Edit Mode에서 토폴로지 정리 권장

### 종합 실습 (15분)

1. Mirror + Subdivision으로 대칭 로봇 바디 만들기
   - Cube에서 시작
   - Mirror Modifier 추가 (X축, Clipping 활성화)
   - Edit Mode에서 바디 형태 잡기
   - Subdivision Surface 추가 (레벨 2)
   - Crease로 날카로운 Edge 유지
2. Boolean으로 디테일 추가
   - Cylinder로 소켓/구멍 형태 만들기
   - Boolean Difference로 바디에 구멍 뚫기
3. Modifier Apply 시점과 순서
   - 모델링이 완전히 끝난 후 Apply 권장
   - Apply 순서: Mirror > Boolean > Subdivision Surface (위에서 아래)
   - Apply 전에 반드시 파일 저장 (되돌릴 수 없음)

### Blender 5.0 신규 Modifier 참고

Blender 5.0에서는 기존 Modifier 시스템에 더해 **Geometry Nodes** 기반의 새로운 Modifier가 추가되었다:

- **Scatter on Surface:** 메시 표면에 오브젝트를 자동으로 흩뿌리는 Modifier. 로봇 표면의 볼트, 리벳, 장식 패턴 등을 빠르게 배치할 수 있다.
- **Instance on Elements:** 메시의 특정 요소(Vertex, Edge, Face)에 오브젝트를 인스턴스로 배치. Array Modifier의 확장판으로, 불규칙한 패턴에도 대응 가능하다.

> 이 Modifier들은 Geometry Nodes를 기반으로 동작하며, Add Modifier 메뉴의 Generate 카테고리에서 찾을 수 있다. 이번 주차에서는 기본 Modifier 숙달이 우선이므로, 관심 있는 학생은 자율적으로 실험해보자.

## ⚠️ 흔한 실수와 해결법

| 실수 | 원인 | 해결법 |
|------|------|--------|
| Mirror에서 중심선이 깨짐 | Clipping 옵션을 체크하지 않음 | Mirror Modifier에서 **Clipping** 활성화. 이미 깨진 경우 중심 Vertex 선택 후 S + X + 0 |
| Subdivision Surface에서 원치 않는 둥글어짐 | 모든 Edge가 부드럽게 처리됨 | **Edge Crease (Shift + E)**로 날카로워야 할 Edge의 Crease 값을 1.0으로 설정 |
| Boolean 적용 시 오류/빈 결과 | 대상 오브젝트가 Manifold(폐쇄형)가 아님 | Boolean 대상 메시에 구멍이 없는지 확인. **Select > All by Trait > Non-Manifold**로 문제 영역 찾기 |
| Modifier Apply 후 형태가 다름 | Modifier 적용 순서가 잘못됨 | 반드시 **위에서 아래 순서**로 Apply. Mirror > Boolean > Subdivision 순서 유지 |
| Scale이 적용된 상태로 Modifier 추가 | Apply Transform을 하지 않음 | Modifier 추가 전 **Ctrl + A > All Transforms**를 적용하여 Scale (1,1,1) 상태 만들기 |

## 과제

- **제출:** Discord #week04-assignment 채널
- **내용:** Modifier를 활용한 로봇/캐릭터 형태 제작
- **형식:** 스크린샷 2장 + 사용한 Modifier 목록 설명 + 한줄 코멘트
- **기한:** 다음 수업 전까지

## 핵심 정리

| 개념 | 핵심 내용 |
|------|-----------|
| Modifier | Non-destructive 워크플로우의 핵심. 원본 메시를 유지하면서 효과 적용 |
| Modifier Stack | 위에서 아래로 순서대로 적용. 순서가 결과에 영향을 미침 |
| Subdivision Surface | 메시를 세분화하여 부드러운 곡면 생성. Ctrl+숫자로 레벨 변경 |
| Edge Crease (Shift+E) | Subdivision에서 날카로운 Edge를 유지하는 핵심 기법 |
| Mirror | 한쪽만 모델링하면 자동 대칭. Clipping 반드시 활성화 |
| Solidify | 면에 두께 추가. 패널, 외장재 표현에 활용 |
| Array | 규칙적 복제. 관절, 손가락, 반복 패턴에 활용 |
| Boolean | Union(합치기), Difference(빼기), Intersect(교차). 디테일 추가에 핵심 |
| Apply 순서 | Mirror > Boolean > Subdivision (위에서 아래). Apply 전 반드시 저장 |

> Modifier는 "실험의 자유"를 준다. Apply 전까지는 언제든 되돌릴 수 있으니, 과감하게 여러 조합을 시도해보자.

## 📋 프로젝트 진행 체크리스트

이번 주차까지 아래 항목이 완료되어야 합니다:

- [ ] Mirror Modifier로 좌우 대칭 완성
- [ ] Subdivision Surface로 부드러운 형태 확보 (Crease로 날카로운 부분 유지)
- [ ] Boolean으로 소켓, 구멍 등 디테일 추가
- [ ] Modifier Stack 순서 정리 완료
- [ ] 정면/측면/투시 뷰에서 형태 점검 스크린샷 촬영
- [ ] (선택) Solidify나 Array로 추가 디테일 실험

## 참고 자료

- [Blender 단축키 모음](../../resources/blender-shortcuts.md)
- [Blender Manual - Modifiers](https://docs.blender.org/manual/en/latest/modeling/modifiers/index.html)
