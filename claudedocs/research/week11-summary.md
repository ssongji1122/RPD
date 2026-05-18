# Week 11 리서치 요약: Rigging 기초

## 개념 흐름

Armature(뼈대 구조 설계) → Skinning/Automatic Weights(메쉬 연결) → Pose Mode(포즈 조작) → Weight Paint(영향 범위 수동 보정)

자동화(Automatic Weights)로 빠르게 시작하고, Weight Paint로 정밀 수정하는 2단계 워크플로우가 핵심이에요.

## 학습 순서 권장

1. **선수 개념 확인**: Object Mode / Edit Mode 전환, 부모-자식 관계, 오브젝트 원점
2. **armature-basics**: Armature 추가 → Edit Mode에서 뼈 구조 설계 → 이름 규칙
3. **Skinning (브리프 없음)**: 메시-아마추어 연결 (Ctrl+P → With Automatic Weights)
4. **Pose Mode (브리프 없음)**: 포즈 조작 단축키 실습
5. **weight-paint**: 자동 웨이트 문제 부분 수동 수정

## 주차 공통 혼란 포인트

- **모드 전환 혼동**: Tab이 Pose Mode 진입이라고 착각. Ctrl+Tab 파이 메뉴 사용 필수.
- **선택 순서**: 메시 먼저, Armature 나중에 Shift+클릭. 거꾸로 하면 연결 실패.
- **Blender 4.x 단축키 변경**: Weight Paint에서 본 선택이 Ctrl+LMB → Ctrl+Shift+LMB로 바뀜.
- **Edit Mode vs Pose Mode 변경 범위**: Edit Mode = 구조(Rest Pose) 수정, Pose Mode = 애니메이션용 변형. 혼동하면 "원래대로 돌아간다" 착각.

## 개별 브리프

- [armature-basics](./armature-basics-brief.md)
- [weight-paint](./weight-paint-brief.md)
