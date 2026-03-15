# 커리큘럼 전체 데이터 자동 채우기 디자인

## Context

curriculum.js에 15주차 전체 데이터가 존재하지만, 4가지 필드가 대부분의 주차에서 비어 있음:
- **shortcuts[]**: Week 3-4만 채워짐, 나머지 11개 주차 비어 있음
- **references[]**: 전체 15주차 모두 비어 있음
- **showme**: Week 2-3만 연결됨, 나머지 12개 주차 미연결
- **image**: Week 5/7/12에서 일부 step 이미지 누락

## 목표

시간이 있을 때 자동으로 채울 수 있도록 Phase별 파이프라인을 구성하고, 오늘 전체 실행

## 디자인

### Phase A: shortcuts[] + references[] 채우기
- curriculum.js를 직접 편집하여 Blender 공식 단축키/문서 URL 삽입
- 주차별 주제에 맞는 단축키 5~8개, 공식 문서 3~5개
- 데이터 소스: Blender 공식 문서 + 기존 카드의 shortcut-list 참고

### Phase B: 누락 이미지 캡처
- /capture 스킬 또는 Playwright MCP로 Blender docs 스크린샷
- 대상: Week 5 Step 1, Week 7 Step 3, Week 12 Step 1

### Phase C: Show Me 카드 생성
- /showme 스킬로 Week 4~13 필요 카드 병렬 생성
- 기존 Generate 모디파이어 카드 재활용 (Week 3에서 이미 생성됨)
- 새로 필요한 카드: sculpt, material, shader, uv, lighting, keyframe, rigging 등

### Phase D: showme 필드 연결
- curriculum.js에 새 카드 ID 연결 (string 또는 array)

## 실행 순서
A → B → C → D (A와 B는 병렬 가능)

## 검증
- /curriculum validate 실행
- 브라우저에서 전체 주차 확인
