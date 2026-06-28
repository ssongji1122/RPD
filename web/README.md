# rpd-web

> rpd — a studio.soluta series  
> `rpd.soluta.studio` 에 배포되는 정적 수업 자료 사이트

## 구조

```
/                 RPD 소개 + 이번 주 + 주차 미리보기
/syllabus         W01~W15 강의 일정 (단계별)
/weeks            주차 목록 (기초/디테일/중간/고급/마무리)
/weeks/[id]       주차 상세 — 단계·단축키·과제·실수·참고자료
/resources        Blender+AI 레퍼런스
```

## 개발

```bash
npm install
npm run dev      # localhost:4321
npm run build    # dist/ 생성
```

## 배포

`main` 브랜치 push → GitHub Actions 자동 빌드 → GitHub Pages 배포  
커스텀 도메인: `rpd.soluta.studio` (DNS 연결 + course-site 대체 시점 미정)

## 콘텐츠 업데이트 (SSoT = Notion)

이 사이트는 **콘텐츠를 직접 보관하지 않는다.** 모든 주차 데이터는
빌드 타임에 repo 루트의 canonical 파일을 읽어 렌더한다.

- 데이터 원본(SSoT): `../weeks/site-data.json` — Notion → sync 파이프라인이 생성.
  `course-site/` 와 동일 원본을 공유하므로 두 사이트 간 드리프트가 없다.
- 로더: `src/data/curriculum.ts` — canonical 을 읽어 타입 지정 + 단계 라벨 부여.
- 현재 진행 주차: canonical 의 `status: "active"` 에서 자동 도출 (수동 변수 없음).

콘텐츠를 바꾸려면 Notion 을 수정하고 sync 를 돌린다. 이 repo 의 데이터 파일은
직접 편집하지 않는다.

디자인 시스템: `DESIGN.md` 참조 (studio.soluta 동일 적용)
