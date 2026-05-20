# rpd-web

> rpd — a studio.soluta series  
> `rpd.soluta.studio` 에 배포되는 정적 수업 자료 사이트

## 구조

```
/                 RPD 소개 + 학기 일정
/syllabus         W01~W15 강의계획
/modules          R0~R5 모듈 목록
/modules/[id]     모듈 상세 + 수업 자료
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
커스텀 도메인: `rpd.soluta.studio`

## 콘텐츠 업데이트

- 모듈 데이터: `src/data/modules.ts`
- 강의 일정: `src/data/syllabus.ts`
- 현재 진행 주차: `src/pages/index.astro` → `currentWeek` 변수

디자인 시스템: `DESIGN.md` 참조 (studio.soluta 동일 적용)
