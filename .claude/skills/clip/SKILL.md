---
name: clip
description: 영상 클립 추출 자동화. 예: /clip week 3 001.mov 1:30-3:00 "이미지 불러오기"
user_invocable: true
---

# Clip 추출 스킬

튜토리얼 영상에서 구간을 추출하여 course-site에 인라인 클립으로 추가합니다.

## 사용법

```
/clip week <주차> <source.mov> <start>-<end> "<label>"
/clip list week <주차>
```

## 동작 순서

1. ffmpeg으로 소스 영상에서 지정 구간 추출
2. 720p (1280px width) H.264 MP4로 압축, 오디오 제거
3. `course-site/assets/clips/week{NN}/` 에 저장
4. curriculum.js의 해당 주차 step에 clips 엔트리 추가

## 추출 명령 템플릿

```bash
ffmpeg -ss <start_seconds> -i "<source_path>" -t <duration_seconds> \
  -vf "scale=1280:-2" -c:v libx264 -preset slow -crf 26 \
  -an -movflags +faststart \
  "course-site/assets/clips/week{NN}/<slug>.mp4"
```

## 파일명 규칙

- 소문자 영문, 하이픈 구분
- 내용을 2-3 단어로 요약
- 예: `ref-import.mp4`, `mirror-setup.mp4`, `head-scale.mp4`

## curriculum.js 업데이트

해당 step의 `clips` 배열에 추가:
```js
{ "label": "<label>", "src": "assets/clips/week{NN}/<slug>.mp4" }
```
clips 배열이 없으면 새로 생성합니다.

## /clip list

`course-site/assets/clips/week{NN}/` 디렉토리의 파일 목록과 크기를 표시합니다.

## 소스 영상 위치

튜토리얼 영상은 보통 다음 경로에 있습니다:
```
/Users/ssongji/Developer/Workspace/RPD/Blender_2026/Mint_robot/MR_Tutorial_videos/
```

## 주의사항

- 클립은 10-120초 범위 권장
- 파일 크기 10MB 이하 유지 (crf 값 조절)
- 무음(오디오 제거): `-an` 플래그 필수
