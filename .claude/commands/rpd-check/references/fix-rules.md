# rpd-check --fix 자동 수정 규칙

| 이슈 | 자동 수정 | 방법 |
|------|----------|------|
| 누락 supplement | skeleton 생성 | `_supplements.json`에 템플릿 엔트리 추가 |
| task ID 중복 | 재번호 | 중복 ID를 순차 번호로 변경 |
| registry 누락 | 엔트리 추가 | curriculum의 showme ID를 registry에 추가 |
| 누락 이미지 | **수정 안 함** | 목록만 출력 (수동 대응) |
| orphan 파일 | **수정 안 함** | 목록만 출력 (수동 판단) |
| 테마 불일치 | **수정 안 함** | 목록만 출력 (CSS 수정 필요) |

## 재검증 루프

`--fix` 실행 시:
1. Phase 1 실행 → 이슈 수집
2. auto-fixable 항목 수정
3. Phase 1 재실행 (수정 검증)
4. 잔여 이슈만 리포트
5. 최종 PASS/FAIL 판정
