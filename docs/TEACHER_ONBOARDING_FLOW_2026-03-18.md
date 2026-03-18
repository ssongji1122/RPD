# Teacher Onboarding Flow

## Goal

새 교수자가 1일 안에 샘플 코스를 복제하고, 1주 안에 실제 수업 운영을 시작하는 것을 목표로 합니다.

## Flow

1. 환경 준비
   - `.env.example` 복사
   - `ADMIN_KEY`, `NOTION_TOKEN` 설정
   - 관리자 서버 로컬 실행

2. 샘플 코스 복제
   - `weeks/templates/sample-course-template.json` 참고
   - 새 강의용 canonical curriculum 초안 생성

3. 커리큘럼 점검
   - `python3 tools/content_pipeline.py check`
   - `python3 tools/content_pipeline.py build`

4. 관리자 편집
   - `admin.html` 접속
   - 주차 제목/실습/자료/과제 수정
   - `변경 미리보기` 확인 후 저장

5. 공개 검수
   - `week.html`, `library.html`, `shortcuts.html` 확인
   - 모바일/데스크톱 핵심 흐름 확인

6. 선택적 Notion publish
   - push 전 검증 확인
   - 필요한 주차만 publish

7. 수업 운영 시작
   - 주차별 수정 로그 확인
   - 과제/영상/Show Me 카드 운영

## Success Criteria

- 교수자가 canonical curriculum 구조를 이해한다.
- 공개 사이트와 비공개 운영 도구의 경계를 이해한다.
- 수정 → diff → 저장 → publish 흐름을 혼자 반복할 수 있다.
