---
marp: true
theme: rpd
paginate: true
---

# Week 04: 기초 모델링 2 - Modifier

## 로봇프러덕트 디자인

2026 Spring | 인하대학교 | 송지희

---

## Modifier란?

- **Non-destructive 워크플로우의 핵심**
  - 원본 메쉬를 변경하지 않고 효과를 적용
  - 언제든 파라미터 조절/삭제 가능
- Properties > Modifier Properties (렌치 아이콘)
- 최종 확정 전까지 자유롭게 실험 가능

---

## Modifier Stack 순서

- Modifier는 **위에서 아래로** 순서대로 적용
- 순서가 결과에 영향을 미침
- 드래그로 순서 변경 가능
- 권장 순서: **Mirror > Subdivision Surface > 기타**

| 순서 | 올바른 예 | 잘못된 예 |
|------|-----------|-----------|
| 1 | Mirror | Subdivision Surface |
| 2 | Subdivision Surface | Mirror |

---

## Subdivision Surface

- 메쉬를 세분화하여 **부드러운 곡면** 생성
- **Viewport 레벨:** 작업 중 미리보기 (1~2 권장)
- **Render 레벨:** 최종 렌더링 (2~3 권장)
- 단축키: Ctrl+1, Ctrl+2, Ctrl+3
- **Shade Smooth** (Right-click)과 함께 사용
- **Crease** (Shift+E): 날카로운 Edge 유지

---

## Mirror Modifier (대칭 모델링)

- 한쪽만 모델링 > 반대쪽 **자동 생성**
- 작업 시간 절반으로 단축
- X/Y/Z 축 선택 (기본: X축)
- **Clipping 옵션:** Vertex가 중심선을 넘지 않도록 제한
- 실습 흐름:
  1. Cube의 한쪽 절반 삭제
  2. Mirror Modifier 추가
  3. Edit Mode에서 한쪽만 모델링

---

## Solidify Modifier

- 면(Face)에 **두께를 추가**
- 얇은 Panel, 갑옷, 외장재 표현에 유용
- **Thickness:** 두께 값 설정
- **Offset:** -1 (안쪽) ~ 0 (중앙) ~ 1 (바깥쪽)
- 활용: 로봇 외장 패널, 보호대, 날개

---

## Array Modifier

- 오브젝트를 **규칙적으로 복제**
- **Relative Offset:** 오브젝트 크기 기준 상대적 거리
- **Constant Offset:** 절대적 거리값 (미터 단위)
- **Object Offset:** 다른 오브젝트의 Transform 기준
- Count: 복제 개수 설정
- 활용: 관절 마디, 손가락, 척추, 반복 패턴

---

## Boolean: Union / Difference / Intersect

- 두 오브젝트 간의 **논리 연산**

| Operation | 설명 | 활용 |
|-----------|------|------|
| Union | 두 오브젝트를 하나로 결합 | 파츠 합치기 |
| Difference | 한 오브젝트에서 다른 형태 제거 | 구멍 뚫기, 소켓 |
| Intersect | 겹치는 부분만 남김 | 교차 형태 추출 |

- 주의: Apply 후 메쉬 정리(토폴로지 정리) 필요

---

## 실습: Mirror + Subdivision 대칭 로봇

1. Cube에서 시작
2. **Mirror Modifier** 추가 (X축, Clipping ON)
3. Edit Mode에서 바디 형태 잡기
4. **Subdivision Surface** 추가 (레벨 2)
5. **Crease** (Shift+E)로 날카로운 Edge 유지
6. **Shade Smooth** 적용

---

## Boolean으로 디테일 추가

1. Cylinder로 소켓/구멍 형태 만들기
2. Boolean **Difference**로 바디에 구멍 뚫기
3. Boolean **Union**으로 파츠 결합

**Modifier Apply 순서**
- 모델링 완료 후 Apply
- 위에서 아래 순서: Mirror > Boolean > Subdivision
- Apply 전 반드시 파일 저장

---

## 과제 안내

- **제출:** Discord #week04-assignment 채널
- **내용:** Modifier를 활용한 로봇/캐릭터 형태 제작
- **형식:**
  - 스크린샷 2장 (Modifier 표시된 상태 + 결과물)
  - 사용한 Modifier 목록 설명
  - 한줄 코멘트
- **기한:** 다음 수업 전까지

| 평가 항목 | 비율 |
|-----------|------|
| Modifier 활용 | 40% |
| 완성도 | 30% |
| 창의성 | 30% |

---

## 다음 주 예고

**Week 05: AI 3D 생성 + Sculpting + MCP 활용**

- AI 도구(Meshy, Tripo)로 3D 모델 생성
- Blender Sculpt Mode 기초 브러시
- Blender MCP로 씬 자동 생성
- AI 모델을 Blender에서 수정하는 워크플로우
