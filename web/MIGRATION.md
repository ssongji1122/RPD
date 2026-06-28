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
| `subpage.html` | 자료 모음 | `/resources` | 부분 — 큐레이션 링크는 옮김, 원본과 항목 대조 필요 |

## 남은 갭 (web/ 에 없는 학생용 페이지)

우선순위는 index/inha 내비게이션에서 참조되는 빈도 기준.

| 페이지 | 역할 | 데이터 의존 | 난이도 | 비고 |
|---|---|---|---|---|
| `library.html` | Show Me 카드 라이브러리 | 카드 데이터 + 이미지 자산 | 중–상 | index에서 4회 링크. 자산 경로 이전 필요 |
| `inha.html` | 인하대 RPD 아카이브 랜딩 | 정적/일부 데이터 | 중 | 보조 허브 역할 (index·library·shortcuts·studio·week 링크) |
| `final-projects.html` | 기말 작품 갤러리 | 제출물 데이터 | 중 | 제출물 소스 연동 방식 확인 필요 |
| `studio.html` | My Studio | 정적 (173줄) | 하 | 소형 페이지 |
| `ladder*.html` | 발표순서 사다리타기 (인터랙티브) | 클라이언트 JS | 중 | `ladder-standalone.html` 1403줄. Astro client island 또는 그대로 이식. 3변형(ladder/standalone/sample) 정리 |

## 드롭 후보 (이행 불필요)

| 페이지 | 사유 |
|---|---|
| `admin.html` | 운영 도구. 공개 배포 제외 대상. web/ 으로 옮기지 않음 |
| `preview-style-v2.html` | 스타일 실험본. 실 콘텐츠 아님 |

## 이행 원칙

- **데이터는 SSoT 유지**: 새 페이지도 하드코딩하지 말고 canonical/기존 데이터 파일을 빌드 타임에 읽는다.
  library·shortcuts·final-projects 의 데이터 소스를 먼저 식별하고 `src/data/` 로더로 흡수한다.
- **자산 이전**: library 카드 이미지 등 `output/`(gitignored) 의존 자산은 web/ `public/` 또는 별도 호스팅으로 옮길지 결정한다.
- **순서 제안**: ~~shortcuts~~(완료) → studio → inha → final-projects → ladder → library
  (데이터 단순·정적 우선, 자산/인터랙션 복잡한 것 후순위).

## 전환 게이트

위 갭이 web/ 에서 모두 채워져 **course-site 의 상위집합**이 된 뒤에만 배포 전환을 한다.
전환은 학기 경계(다음 학기 시작 직전)에서 수행한다. 두 경로:

1. **슬롯 교체**: 루트 `.github/workflows/deploy-pages.yml` 을 Astro 빌드로 교체 → 같은 GitHub Pages(github.io/RPD)가 web/ 이 됨. 도메인 불필요, 라이브가 한 번에 전환.
2. **별도 호스팅 + 도메인**: web/ 을 별도 Pages/Vercel + `rpd.soluta.studio` DNS 로 띄워 병행 검증 후 전환.
