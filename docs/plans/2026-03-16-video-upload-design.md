# Video Upload Feature Design

## Summary

Admin 페이지의 기존 videos 섹션(`{title, url}`)에 파일 업로드 기능을 추가한다.
업로드된 영상은 로컬에 저장되고, url 필드에 상대 경로가 자동 입력된다.
기존 URL 직접 입력도 그대로 유지된다.

## Data Model

변경 없음. 기존 `videos: [{title, url}]` 구조 유지.
- 외부 링크: `url: "https://youtube.com/..."`
- 로컬 업로드: `url: "assets/videos/week-01/video-0.mp4"`

## Backend (`tools/admin-server.py`)

### New Endpoint

```
POST /api/upload-video/{weekNum}/{videoIdx}
Content-Type: multipart/form-data
Field: "video" (file)
```

### Behavior

1. multipart/form-data에서 "video" 필드 추출
2. 확장자 검증: `.mp4`, `.webm`, `.mov`, `.ogg`, `.avi`
3. 저장 경로: `assets/videos/week-{N:02d}/video-{idx}{ext}`
4. `curriculum.js`의 해당 week videos[idx].url 업데이트
5. 응답: `{"ok": true, "path": "assets/videos/week-01/video-0.mp4"}`

### File Structure

```
course-site/assets/videos/
  week-01/
    video-0.mp4
    video-1.webm
  week-02/
    video-0.mov
```

### No Size Limit

서버가 로컬이므로 파일 크기 제한 없음.

## Frontend (`course-site/admin.html`)

### UI Changes

각 video 항목의 URL 입력 옆에 업로드 버튼 추가:

```
[제목 입력]
[URL 입력] [🎬 영상 업로드] [x]
```

### Upload Flow

1. 파일 선택 → `POST /api/upload-video/{weekNum}/{videoIdx}`
2. 응답의 path를 해당 video의 url 필드에 반영
3. `markDirty()` 호출 + `renderEditor()` 재렌더
4. toast("영상 업로드 완료", "success")

### CSS

기존 `.image-upload-btn` 스타일을 `.video-upload-btn`으로 복제/재사용.

## Implementation Scope

- `admin-server.py`: upload-video 엔드포인트 + VIDEOS_DIR 상수
- `admin.html`: videos 섹션 UI + uploadVideo() 함수 + CSS
