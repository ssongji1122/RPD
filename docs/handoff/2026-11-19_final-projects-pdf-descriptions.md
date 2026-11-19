---
title: 기말 작품 아카이브 — 발표 자료 PDF와 작품 설명 인계
last_updated: 2026-11-19
status: active
---

# 기말 작품 아카이브 — 발표 자료 PDF와 작품 설명 인계

대표 요청(2026-11-19): 기말 작품 상세에 **작품 설명**을 넣고, 학생이 PDF · PPTX로 낸 발표 자료도 **이름만 빼고** 넣는다. 상세 화면은 「소개 · 이미지 · 웹사이트(발표 자료) 바로 가기」로 간추린 상태이며, 노션 주차별 진행 사항은 넣지 않기로 했다.

## 이미 라이브에 반영된 것 (PR #147 ~ #153)

- 상세 구조: 소개(작품명 · 설명 · 버튼) → 진행 과정 격자 → 완성 결과 격자 → 아래 버튼. 베이지 띠 없음.
- 웹사이트 버튼: 24점 중 20점. project-05 · 07 · 08 · 23은 학생 HTML을 `course-site/assets/final-projects/project-NN/presentation.html`로 올림(실명 · 학번 제거).
- 작품 설명(`description` 필드): 01 · 05 · 07 · 08 · 10 · 13 · 15 · 16 · 17 · 18 · 22 · 23.
- 화면 코드: `web/src/pages/final-projects.astro`. 버튼은 링크 kind가 웹페이지 · 작품 페이지 · 발표 자료 · Behance면 자동으로 붙는다(`isPrimaryLink`).

## 남은 일

1. 아래 「변환 끝난 PDF」를 `course-site/assets/final-projects/project-NN/presentation.pdf`로 복사하고, 링크 `{label: "발표 자료", url: "assets/final-projects/project-NN/presentation.pdf", kind: "Presentation"}`를 더한다. kind가 Presentation이면 버튼 문구가 「발표 자료 바로 가기」가 된다.
2. 설명이 없는 12점(02 · 03 · 04 · 06 · 09 · 11 · 12 · 14 · 19 · 20 · 21 · 24)에 2~3문장 설명을 쓴다. 근거는 그 작품 발표 자료 본문뿐이다. 합니다체, 과장 없이.
3. 대기 중인 두 파일(sub-03 · sub-20)을 받아 같은 방식으로 변환 · 검증 · 짝 맞추기를 한다. 남은 작품 중 PDF가 없는 것(04 · 06 · 09 · 12 · 19 · 24 중 일부)은 Canva · 노션 링크가 이미 있으면 그대로 두고 설명만 쓴다.
4. 빌드(`cd web && npm run build`), `python3 tools/check_final_project_assets.py`, 로컬 확인 → PR → CI → 머지 → 배포 → 라이브 확인(주소에 `?v=` 붙여 캐시 회피). 대표에게 링크를 보여 준다.

## 변환 끝난 PDF (scratchpad, 저장소 밖)

위치: `/private/tmp/claude-501/-Users-ssongji-Developer-Workspace-studio-soluta--claude-worktrees-rpd-class-links-58a9b4/4a77fc78-bcb8-4e71-a350-32724ecd9e38/scratchpad/pdfout/sub-NN.pdf`

이미지 대조로 맞춘 짝(제출 페이지 번호 → 작품):

| 파일 | 작품 | 비고 |
|---|---|---|
| sub-04.pdf | project-18 Kku-ing | 웹사이트 버튼 있음, 발표 자료 추가 |
| sub-06.pdf | project-20 | 노란 박스형 로봇, 작품명 없음 → 발표 자료 표지 · 본문에서 근거 찾기 |
| sub-07.pdf | project-14 Tebi | |
| sub-11.pdf | project-17 STIMO WORLD | |
| sub-13.pdf | project-23 묘한 | 웹페이지 있음, 발표 자료 추가 |
| sub-14.pdf | project-21 ME-O | |
| sub-15.pdf | project-02 Tesla x | 화성 탐사 차량 |
| sub-16.pdf | project-03 HOPE | |
| sub-19.pdf | project-11 | 차량, 작품명 없음 |

- sub-03.pdf는 끊긴 원본으로 만든 빈 파일이라 쓰지 않는다. 원본 재다운로드 중(`subs/sub-03/00.pdf`, `subs/sub-20/00.pptx`).
- 변환 도구: `redact_pdf.py`(쪽을 긴 변 1600px 이미지로 다시 그리고, 글자 층 검색 + macOS Vision OCR(`ocr`)로 찾은 실명 · 학번 · 이메일 자리를 칠함), `verify_pdf.py`(결과를 다시 OCR로 읽어 남은 항목 확인). 실행은 `scratchpad/venv/bin/python`. 위 9개 모두 남은 항목 0건.
- PPTX가 LibreOffice에서 안 열리면 Keynote AppleScript로 PDF로 바꾼다(sub-11 사례).
- 학생 실명 · 학번 대응표는 `redact_pdf.py`의 `PEOPLE`에만 있다. 저장소 · 커밋 · PR에 실명을 쓰지 않는다.

## 주의

- 짝 맞추기는 반드시 이미지로 한다. 노트 문장 일치로 맞췄다가 「묘한」을 project-20에 잘못 붙인 사고가 있었다(#151에서 바로잡음).
- design-gate가 학생 HTML의 가는 글자 · keep-all을 잡는다. PDF는 해당 없음.
- 공개 저장소다. PR 본문 · 커밋에 실명 · 학번 금지.
