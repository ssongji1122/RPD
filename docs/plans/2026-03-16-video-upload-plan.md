# Video Upload Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Admin 페이지의 videos 섹션에 로컬 영상 파일 업로드 기능 추가

**Architecture:** 기존 이미지 업로드 패턴(`_handle_upload`)을 복제하여 동영상 전용 엔드포인트를 추가. 프론트엔드는 각 video 항목에 업로드 버튼을 추가하고, 업로드 완료 시 url 필드에 로컬 경로를 자동 입력.

**Tech Stack:** Python stdlib HTTP server, vanilla JS (ES5), HTML/CSS

**Design doc:** `docs/plans/2026-03-16-video-upload-design.md`

---

### Task 1: Backend — VIDEOS_DIR 상수 추가

**Files:**
- Modify: `tools/admin-server.py:37`

**Step 1: Add VIDEOS_DIR constant**

`admin-server.py:37` 의 `IMAGES_DIR` 바로 아래에 추가:

```python
VIDEOS_DIR = COURSE_SITE / "assets" / "videos"
```

**Step 2: Commit**

```bash
git add tools/admin-server.py
git commit -m "feat: add VIDEOS_DIR constant for video uploads"
```

---

### Task 2: Backend — 동영상 업로드 엔드포인트 라우팅

**Files:**
- Modify: `tools/admin-server.py:1046-1047`

**Step 1: Add route matching after image upload route**

`admin-server.py:1046` (`return` 뒤) 아래에 추가:

```python
        # POST /api/upload-video/{weekNum}/{videoIdx}
        video_upload_match = re.match(r"^/api/upload-video/(\d+)/(\d+)$", path)
        if video_upload_match:
            week_num = int(video_upload_match.group(1))
            video_idx = int(video_upload_match.group(2))
            self._handle_video_upload(week_num, video_idx)
            return
```

**Step 2: Commit**

```bash
git add tools/admin-server.py
git commit -m "feat: add video upload route in do_POST"
```

---

### Task 3: Backend — `_handle_video_upload` 핸들러 구현

**Files:**
- Modify: `tools/admin-server.py` (after `_handle_upload` method, around line 1200)

**Step 1: Implement handler**

`_handle_upload` 메서드 끝난 직후에 추가. 패턴은 `_handle_upload`와 동일하되, 필드명 `"video"`, 확장자 목록, 저장 경로만 다름:

```python
    def _handle_video_upload(self, week_num: int, video_idx: int) -> None:
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self._send_error_json(400, "Expected multipart/form-data")
            return

        body = self._read_body()
        try:
            fields = parse_multipart(body, content_type)
        except Exception as exc:
            self._send_error_json(400, f"Multipart parse error: {exc}")
            return

        if "video" not in fields:
            self._send_error_json(400, 'No field named "video" found')
            return

        filename, file_data = fields["video"]
        if not filename:
            self._send_error_json(400, "No filename provided")
            return

        ext = os.path.splitext(filename)[1].lower()
        if not ext:
            ext = ".mp4"

        allowed_ext = {".mp4", ".webm", ".mov", ".ogg", ".avi"}
        if ext not in allowed_ext:
            self._send_error_json(
                400, f"Unsupported video type: {ext}. Allowed: {sorted(allowed_ext)}"
            )
            return

        # Build destination path
        week_dir = VIDEOS_DIR / f"week-{week_num:02d}"
        week_dir.mkdir(parents=True, exist_ok=True)
        dest_filename = f"video-{video_idx}{ext}"
        dest_path = week_dir / dest_filename

        # Write file
        dest_path.write_bytes(file_data)

        # Relative path from course-site/ root
        relative_path = f"assets/videos/week-{week_num:02d}/{dest_filename}"

        # Update curriculum.js
        try:
            data = read_curriculum()
        except Exception as exc:
            self._send_error_json(500, f"Read curriculum failed: {exc}")
            return

        week_entry = None
        for entry in data:
            if entry.get("week") == week_num:
                week_entry = entry
                break

        if week_entry is None:
            self._send_error_json(404, f"Week {week_num} not found in curriculum")
            return

        videos = week_entry.get("videos", [])
        if video_idx < 0 or video_idx >= len(videos):
            self._send_error_json(
                400,
                f"Video index {video_idx} out of range (week {week_num} has {len(videos)} videos)",
            )
            return

        videos[video_idx]["url"] = relative_path

        try:
            write_curriculum(data)
        except Exception as exc:
            self._send_error_json(500, f"Write curriculum failed: {exc}")
            return

        self._send_json({"ok": True, "path": relative_path})
```

**Step 2: Commit**

```bash
git add tools/admin-server.py
git commit -m "feat: implement _handle_video_upload handler"
```

---

### Task 4: Frontend — CSS for video upload button

**Files:**
- Modify: `course-site/admin.html:277` (after `.image-upload-btn input[type="file"]` rule)

**Step 1: Add video upload button styles**

기존 `.image-upload-btn` 스타일을 재사용. `admin.html:277` 뒤에 추가:

```css
    /* ── Video upload ─────────────────────────────────── */
    .video-upload-btn {
      display: inline-flex; align-items: center; gap: 6px;
      padding: 6px 12px; border-radius: 999px;
      border: 1px solid rgba(147,197,253,.18);
      background: transparent; color: var(--muted-strong);
      cursor: pointer; font: inherit; font-size: .78rem;
      transition: border-color .15s, color .15s;
      white-space: nowrap;
    }
    .video-upload-btn:hover {
      border-color: rgba(147,197,253,.36); color: var(--text);
    }
    .video-upload-btn input[type="file"] {
      display: none;
    }
```

**Step 2: Commit**

```bash
git add course-site/admin.html
git commit -m "feat: add video upload button CSS"
```

---

### Task 5: Frontend — videos 섹션 UI에 업로드 버튼 추가

**Files:**
- Modify: `course-site/admin.html:1272-1281` (videos forEach loop)

**Step 1: Add upload button to each video item**

현재 각 video 항목 HTML (line 1273-1280):
```js
      parts.push(
        '<div class="preview-link-edit">',
        '<div class="link-fields">',
        '<input class="edit-inline" data-video-field="title" data-idx="', i, '" ... />',
        '<input class="edit-inline" data-video-field="url" data-idx="', i, '" ... />',
        '</div>',
        '<button class="btn-icon danger" data-remove="videos" data-idx="', i, '" ...>&times;</button>',
        '</div>'
      );
```

교체하여 URL 입력과 삭제 버튼 사이에 업로드 버튼 추가:

```js
      videos.forEach(function(v, i) {
        parts.push(
          '<div class="preview-link-edit">',
          '<div class="link-fields">',
          '<input class="edit-inline" data-video-field="title" data-idx="', i, '" value="', esc(v.title), '" placeholder="영상 제목" style="font-size:.88rem" />',
          '<div style="display:flex;gap:6px;align-items:center">',
          '<input class="edit-inline" data-video-field="url" data-idx="', i, '" value="', esc(v.url), '" placeholder="URL 또는 업로드" style="font-size:.78rem;color:var(--muted);flex:1" />',
          '<label class="video-upload-btn">',
          '&#127916; 업로드',
          '<input type="file" accept="video/*" data-upload-video="', i, '" data-week="', weekNum, '" />',
          '</label>',
          '</div>',
          '</div>',
          '<button class="btn-icon danger" data-remove="videos" data-idx="', i, '" type="button">&times;</button>',
          '</div>'
        );
      });
```

Key data attributes: `data-upload-video="{idx}"`, `data-week="{weekNum}"`

**Step 2: Commit**

```bash
git add course-site/admin.html
git commit -m "feat: add video upload button to videos section UI"
```

---

### Task 6: Frontend — 파일 선택 이벤트 핸들러

**Files:**
- Modify: `course-site/admin.html:1724-1731` (change event listener, after image upload handler)

**Step 1: Add video upload change handler**

`admin.html:1731` (`return;` + `}`) 뒤, `});` (line 1732) 앞에 추가:

```js
      // Video upload
      if (el.dataset.uploadVideo !== undefined) {
        var vi = parseInt(el.dataset.uploadVideo, 10);
        var weekNum = parseInt(el.dataset.week, 10);
        var file = el.files[0];
        if (file) uploadVideo(weekNum, vi, file);
        return;
      }
```

**Step 2: Commit**

```bash
git add course-site/admin.html
git commit -m "feat: add video upload change event handler"
```

---

### Task 7: Frontend — `uploadVideo()` 함수

**Files:**
- Modify: `course-site/admin.html:1896` (after `uploadImage` function)

**Step 1: Add uploadVideo function**

`uploadImage` 함수 끝 (`}`) 뒤, keyboard shortcut 섹션 앞에 추가:

```js
    // ─── Video upload ────────────────────────────────────
    async function uploadVideo(weekNum, videoIdx, file) {
      var form = new FormData();
      form.append("video", file);
      try {
        var res = await fetch("/api/upload-video/" + weekNum + "/" + videoIdx, {
          method: "POST",
          headers: uploadApiHeaders(),
          body: form,
        });
        if (!res.ok) throw new Error("HTTP " + res.status);
        var data = await res.json();
        curriculum[selectedIdx].videos[videoIdx].url = data.path;
        markDirty();
        renderEditor();
        toast("영상 업로드 완료", "success");
      } catch (e) {
        toast("영상 업로드 실패: " + e.message, "error");
      }
    }
```

**Step 2: Commit**

```bash
git add course-site/admin.html
git commit -m "feat: implement uploadVideo() function"
```

---

### Task 8: 통합 테스트

**Step 1: 서버 기동 확인**

```bash
python3 tools/admin-server.py --port 8799 &
```

**Step 2: 비디오 업로드 API 테스트 (curl)**

```bash
# 테스트용 더미 비디오 파일 생성
dd if=/dev/zero of=/tmp/test-video.mp4 bs=1024 count=10

# 업로드 테스트 (week 1, video index 0이 존재한다고 가정)
curl -X POST http://localhost:8799/api/upload-video/1/0 \
  -F "video=@/tmp/test-video.mp4"
```

Expected: `{"ok": true, "path": "assets/videos/week-01/video-0.mp4"}`

**Step 3: 확장자 거부 테스트**

```bash
cp /tmp/test-video.mp4 /tmp/test-video.exe
curl -X POST http://localhost:8799/api/upload-video/1/0 \
  -F "video=@/tmp/test-video.exe"
```

Expected: 400 error with "Unsupported video type"

**Step 4: Clean up and commit**

```bash
kill %1  # stop test server
rm /tmp/test-video.mp4 /tmp/test-video.exe
git add -A
git commit -m "feat: video upload complete — backend + frontend"
```
