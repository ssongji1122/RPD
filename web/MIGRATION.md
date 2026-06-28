# course-site → web 이행 (parity) 계획

> web/ 이 course-site 를 **대체**하려면 학생용 페이지를 모두 옮겨 상위집합이 되어야 한다.
> 현재 web/ 은 부분집합이다. 이 문서는 남은 갭과 이행 순서를 정리한다.
> 조사 기준: course-site 의 공개 배포 대상(= `tools/content_pipeline.py`
> `PUBLIC_EXCLUDED_RELATIVE_PATHS` 에서 admin·운영 데이터를 뺀 나머지 html).

## 현재 상태

| course-site 페이지 | 역할 | web/ 대응 | 상태 |
|---|---|---|---|
| `index.html` | 홈 | `/` | 완료 (canonical 연동) |
| `week.html` | 주차 상세 (notion-blocks 렌더) | `/weeks/[id]` | 완료 (canonical 연동) |
| `shortcuts.html` | 단축키 DB (전체) | `/shortcuts` | 완료 — canonical `weeks[].shortcuts` 131개 집계 + 주차별 그룹 + 클라이언트 검색 |
| `final-projects.html` | 기말 작품 갤러리 | `/final-projects` | 완료 — `course-site/data/final-projects.js`(작품 23) 빌드타임 로드 + 미디어 13MB를 `public/assets/final-projects/` 복사 |
| `inha.html` | 인하대 코스 랜딩 | `/inha` | 완료 — canonical 기반 진행 채움 타임라인으로 단순화 재작성 (app-shell·i18n 제외) |
| `library.html` | Show Me 카드 라이브러리 | `/library` + `/showme/*.html` | 완료 — `_registry.js`/`_catalog.json` 빌드타임 파싱으로 인덱스(82개, 카테고리별·검색), 카드 87개 + `_helpers.js`를 `public/showme/`로 복사(정적·view-only) |
| `subpage.html` | 자료 모음 | `/resources` | 부분 — 큐레이션 링크는 옮김, 원본과 항목 대조 필요 |

## 남은 갭

없음. 모든 학생용 페이지 이행 완료. (`subpage`/`/resources` 는 항목 대조만 남은 마이너 후속.)

## 드롭 후보 (이행 불필요)

| 페이지 | 사유 |
|---|---|
| `admin.html` | 운영 도구. 공개 배포 제외 대상. web/ 으로 옮기지 않음 |
| `preview-style-v2.html` | 스타일 실험본. 실 콘텐츠 아님 |
| `ladder*.html` | 발표순서 사다리타기 유틸. 사용자 결정으로 이행 제외 |
| `studio.html` | "My Studio" 덱 빌더 도구(관리자 패널 성격) — 학생용 콘텐츠 아님 |

## 이행 원칙

- **데이터는 SSoT 유지**: 새 페이지도 하드코딩하지 말고 canonical/기존 데이터 파일을 빌드 타임에 읽는다.
  library·shortcuts·final-projects 의 데이터 소스를 먼저 식별하고 `src/data/` 로더로 흡수한다.
- **자산 이전**: 미디어 바이너리는 web/ `public/assets/` 로 복사한다(final-projects 13MB 적용 완료). course-site 은퇴 시 중복 해소.
- **이행 완료**: ~~shortcuts~~ → ~~final-projects~~ → ~~inha~~ → ~~library~~. studio·ladder 는 드롭.

## 전환 게이트

학생용 페이지 이행이 모두 끝나 web/ 이 course-site 의 **상위집합**이 됐다(`subpage`→`/resources` 항목 대조만 남음).

**전환 실행됨 (옵션 1 — 슬롯 교체, 학기 종료 후):**
- 루트 `.github/workflows/deploy-pages.yml` 을 Astro(web/) 빌드로 교체. github.io/RPD 가 web/ 이 됨.
- `astro.config.mjs`: `base: '/RPD/'` (project pages 하위 경로). 내부 링크는 `src/lib/url.ts` 의 `url()` 헬퍼가 base 를 따른다.
- `public/CNAME` 제거(커스텀 도메인 보류). course-site 는 repo 에 남되 더는 배포되지 않는다.

**도메인 전환(나중, 별도 작업):** `rpd.soluta.studio` DNS 연결 시 — `astro.config` 의 `base` 를 `'/'`, `site` 를 도메인으로 바꾸고 `public/CNAME`(rpd.soluta.studio) 재생성. `url()` 헬퍼 덕에 링크는 자동 적응.
