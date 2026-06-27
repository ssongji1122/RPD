# 사다리타기 고도화 1단계 (네이버 차용) — 설계 문서

- **날짜**: 2026-06-09
- **상태**: 설계 확정 (구현 대기)
- **선행**: [v1 설계](2026-06-08-ladder-presentation-order-design.md) 구현 완료 (`ladder.html`/`ladder.js`/`page-ladder.css`)
- **배경**: v1이 "너무 단순"하다는 피드백 → 네이버 사다리타기 리서치 후 차용 요소를 1단계로 고도화

## 1. 리서치 요약 (네이버 사다리타기)
- 인원 2~24(PC)/12(모바일), 이름 + **결과(당첨 항목) 자유 입력** 1:1 매핑
- 사다리 자동 + 애니메이션, **결과 가림→공개**, 다시하기
- 출처: [픽잇스마트](https://pickitsmart.com/naver-ladder-game-link/), [OJJ](https://ladder.ojj.kr/), [나무위키](https://namu.wiki/w/%EC%82%AC%EB%8B%A4%EB%A6%AC%ED%83%80%EA%B8%B0)

## 2. 1단계 범위 (3요소)
"발표순서는 결과의 한 종류"라는 통찰로 범용화 + 연출. 효과음·인원 빠른설정·사다리 수동편집은 **2단계로 분리(범위 밖)**.

### ① 결과 입력칸 (범용화)
- 이름 textarea 아래 **"결과 직접 입력" 토글**(기본 접힘). 라벨: `결과 직접 입력 (벌칙·역할 등, 비우면 발표순서)`
- 펼치면 결과 textarea 표시. `parseParticipants` 재사용해 줄 단위 파싱
- **outcomes 결정 로직** (build 시):
  - 토글 닫힘 OR 결과 비어있음 → `outcomes = ['1번','2번',…,'N번']` (발표순서 기본)
  - 결과 채워짐 → `outcomes = 파싱된 결과`. **개수가 이름과 다르면** build 막고 hint(`결과를 N개 입력하세요 (현재 M개)`)
- 결과 라벨은 완성형 문자열(기본은 "N번", 커스텀은 입력 그대로). → 기존 `.result-slot::after{content:'번'}` **제거**, 라벨에 직접 포함

### ② 경로 색상 구분
- 참가자 i 고유색: `hsl(i * 360/N, 70%, 62%)` (균등 분포, 다크 배경 가독 채도/명도 고정)
- 경로(polyline) stroke = 고유색. 결과 행 앞에 같은 색 **dot**(점)으로 연결
- 개별/전체 공개 모두 해당 참가자 색
- **DESIGN.md 색 예외**: DESIGN.md "민트 단색·장식색 금지" 이탈 → 모션 예외처럼 **이 페이지 한정** 허용(2026-06-09 사용자 승인). 다른 페이지 전파 금지
- 색맹 대응: 색은 보조, **이름 라벨이 항상 식별자**(기존 유지) — 색 단독 의존 안 함

### ③ 도착 공개 긴장감 (항상 가림)
- 하단 결과(ladder-slot)를 빌드 시 **`?`로 가림**
- 이름 클릭/전체 공개 → 경로 애니메이션 완료(transitionend) 시 **그 칸만 공개**(가림 해제 + outcome 표시 + 기존 pop)
- 발표순서(1~N)도 가림 → "두구두구" 긴장감 일관 (사용자 선택 a)
- `처음부터`/재빌드 시 다시 가림

## 3. 영향 파일
| 파일 | 변경 |
|------|------|
| `course-site/ladder.html` | 결과 토글 + textarea 마크업 추가 |
| `course-site/assets/ladder.js` | outcomes 로직, computeResults 시그니처(outcomes), 색상 생성, 슬롯 가림/공개 |
| `course-site/assets/page-ladder.css` | 색 dot, 가림 `?` 스타일, ::after 제거, 토글 |
| `tests/ladder.spec.js` | 결과 커스텀/자동, 개수검증, 색상 고유, 가림→공개 |

## 4. 핵심 인터페이스 변경
- `computeResults(ladder, participants, outcomes)` — `slot` 숫자 → `outcome` 문자열 라벨. 반환 `{name, startCol, endCol, outcome, path}`
- `bijection` 불변식 유지(endCol 유니크) → outcome도 유니크(자동) 또는 커스텀 1:1
- 기존 테스트의 `slot`(숫자) 단언 → `outcome`(문자열, 기본 "N번")로 갱신. **bijection 검증은 endCol set 크기로 유지**

## 5. 엣지 케이스
- 결과 개수 < 이름 → hint, build 막음 / 결과 빈 줄 trim 후 개수 판정
- 커스텀 결과 중복(예 "꽝" 2개) → 허용(네이버도 허용, 발표순서 아님)
- 색상 N 매우 큼 → hue 균등이라 인접 색 비슷할 수 있음(허용, 라벨로 식별)
- 가림 상태에서 reset → 재가림
- XSS: 결과도 사용자 입력 → `textContent`만 (기존 규약)

## 6. 테스트 계획
- 결과 비움 → outcome `1번..N번` 자동
- 결과 커스텀(개수 일치) → 결과행에 커스텀 텍스트, endCol 유니크
- 결과 개수 불일치 → hint, board 미생성
- 색상: N명 경로 stroke 색이 N가지(고유)
- 가림: build 직후 하단 `?`, 공개 후 outcome 표시
- 기존 회귀(직각·정렬·대규모·도착타이밍) 유지

## 7. 범위 밖 (2단계 후보)
효과음(자동재생/소음 정책), 인원 숫자 빠른설정, 사다리 가로줄 수동 편집, 결과 셔플 애니

## 8. 리스크
- DESIGN.md 색 이탈 — 게임 한정 명시, 전파 금지
- computeResults 시그니처 변경 → 기존 테스트/렌더 동시 수정 필요(누락 주의)
- 복잡도 증가(가림 상태 + 색 + 커스텀) → 단계 커밋으로 관리
