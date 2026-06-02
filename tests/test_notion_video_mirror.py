"""Regression tests for Notion-uploaded video mirroring (presigned-URL expiry fix).

Background: file-type videos were saved as 1-hour presigned S3 URLs and broke on the
live site once a sync lagged past the TTL. The fix mirrors+transcodes them to a
committed compressed .mp4 and points the renderer at `local_url`. These tests pin the
two regression traps:
  - local_url must be gated on `target.exists()`, NOT download-success, or cached
    images/videos lose local_url on the next sync and start expiring.
  - video local_url must carry the .mp4 extension (transcoded), not the source .mov.

Run directly (no pytest needed):
    python3 tests/test_notion_video_mirror.py
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import notion_api  # noqa: E402


def test_cached_image_keeps_local_url():
    """Cached file image keeps local_url (placement gated on target.exists → no image regression)."""
    d = Path(tempfile.mkdtemp())
    (d / "abc.png").write_bytes(b"x")
    blocks = [{"id": "a-bc", "type": "image", "image": {"type": "file", "file": {"url": "https://expired/x.png"}}}]
    n = notion_api.download_block_assets(blocks, d, "assets/notion-images/week01")
    assert blocks[0].get("local_url") == "assets/notion-images/week01/abc.png", blocks[0]
    assert n == 0


def test_cached_video_uses_mp4_local_url():
    """Cached file video exposes a .mp4 local_url (transcoded) → survives sync #2."""
    d = Path(tempfile.mkdtemp())
    (d / "vid.mp4").write_bytes(b"x")
    blocks = [{"id": "v-id", "type": "video", "video": {"type": "file", "file": {"url": "https://expired/x.mov"}}}]
    n = notion_api.download_block_assets(blocks, d, "assets/notion-images/week13")
    assert blocks[0].get("local_url") == "assets/notion-images/week13/vid.mp4", blocks[0]
    assert n == 0


def test_external_video_no_local_url():
    """External (YouTube) video gets no local_url → renderer keeps the iframe embed."""
    d = Path(tempfile.mkdtemp())
    blocks = [{"id": "y-1", "type": "video", "video": {"type": "external", "external": {"url": "https://youtube.com/watch?v=abc"}}}]
    notion_api.download_block_assets(blocks, d, "assets/notion-images/week06")
    assert "local_url" not in blocks[0], blocks[0]


def test_failed_download_no_dangling_local_url():
    """Failed download leaves no local_url (no broken local path; renderer uses remote fallback)."""
    d = Path(tempfile.mkdtemp())
    blocks = [{"id": "f-1", "type": "video", "video": {"type": "file", "file": {"url": "https://nonexistent.invalid/x.mov"}}}]
    notion_api.download_block_assets(blocks, d, "assets/notion-images/week13")
    assert "local_url" not in blocks[0], blocks[0]


def test_transcode_produces_mp4():
    """ffmpeg transcode yields a non-empty mp4 (skipped if ffmpeg/sample missing)."""
    if not shutil.which("ffmpeg"):
        print("  - skip: ffmpeg not installed")
        return
    src = ROOT / "course-site" / "assets" / "clips" / "week03" / "head-edit.mp4"
    if not src.exists():
        print("  - skip: sample clip missing")
        return
    d = Path(tempfile.mkdtemp())
    target = d / "out.mp4"
    uri = src.resolve().as_uri()
    notion_api._download_and_transcode_video(uri, target, urllib.request.Request(uri))
    assert target.exists() and target.stat().st_size > 0


if __name__ == "__main__":
    tests = [
        test_cached_image_keeps_local_url,
        test_cached_video_uses_mp4_local_url,
        test_external_video_no_local_url,
        test_failed_download_no_dangling_local_url,
        test_transcode_produces_mp4,
    ]
    passed = failed = 0
    for fn in tests:
        try:
            fn()
            print(f"  ✓ {fn.__name__}")
            passed += 1
        except AssertionError as exc:
            print(f"  ✗ {fn.__name__} — {exc}")
            failed += 1
        except Exception as exc:  # noqa: BLE001
            print(f"  ✗ {fn.__name__} — ERROR {exc}")
            failed += 1
    print(f"\nPASSED: {passed}  FAILED: {failed}")
    sys.exit(1 if failed else 0)
