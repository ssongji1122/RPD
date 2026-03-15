from pathlib import Path

from lessonforge.subtitles import (
    ClipNotes,
    OutlineCardContent,
    SubtitleNoteLibrary,
    SubtitleDraft,
    SubtitleCue,
    VideoProbeInfo,
    build_outline_card_content,
    build_outline_bullets,
    generate_subtitle_draft,
    parse_clip_notes,
    parse_week_video_map,
    prepend_outline_opener,
)


def test_parse_clip_notes_reads_week02_markdown() -> None:
    root = Path(__file__).resolve().parents[3]
    notes_path = root / "Blender_2026" / "week_02" / "video_notes.md"

    notes = parse_clip_notes(notes_path).by_number

    assert 4 in notes
    assert notes[4].title.startswith("인터페이스 소개")
    assert "Blender UI의 4가지 주요 영역" in notes[4].core
    assert any("3D Viewport" in detail for detail in notes[4].details)


def test_generate_subtitle_draft_uses_note_content(monkeypatch) -> None:
    note = ClipNotes(
        clip_number=4,
        title="인터페이스 소개",
        core="Blender UI의 4가지 주요 영역",
        details=[
            "3D Viewport — 메인 작업 공간",
            "Outliner — 씬 오브젝트 목록",
            "Properties — 선택 오브젝트 세부 설정",
        ],
    )
    library = SubtitleNoteLibrary(by_number={4: note})

    monkeypatch.setattr("lessonforge.subtitles.get_video_duration", lambda _: 32.0)

    draft = generate_subtitle_draft(Path("/tmp/004_blender_interface.mov"), library)

    assert draft.cue_source == "notes"
    assert draft.title == "인터페이스 소개"
    assert len(draft.cues) >= 2
    assert "인터페이스 소개" in draft.cues[0].text


def test_parse_week_video_map_maps_cute_robot_filename() -> None:
    root = Path(__file__).resolve().parents[1]
    map_path = root / "week_video_map.yaml"

    notes = parse_week_video_map(map_path)
    clip_note = notes.get_for_video(Path("/tmp/007.Cute_robot_body.mp4"))

    assert clip_note is not None
    assert "몸통 모델링" in clip_note.title
    assert any("기초 모델링 1" in detail for detail in clip_note.details)


def test_build_outline_bullets_deduplicates_title_prefix() -> None:
    draft = SubtitleDraft(
        video_path=Path("/tmp/demo.mp4"),
        duration_seconds=12.0,
        clip_number=1,
        title="인터페이스 소개",
        cue_source="notes",
        cues=[
            SubtitleCue(0.0, 4.0, "인터페이스 소개: Blender UI의 4가지 주요 영역."),
            SubtitleCue(4.0, 8.0, "3D Viewport — 메인 작업 공간."),
            SubtitleCue(8.0, 12.0, "3D Viewport — 메인 작업 공간."),
        ],
    )

    bullets = build_outline_bullets(draft)

    assert bullets == [
        "Blender UI의 4가지 주요 영역.",
        "3D Viewport — 메인 작업 공간.",
    ]


def test_build_outline_card_content_uses_summary_and_numbered_items() -> None:
    draft = SubtitleDraft(
        video_path=Path("/tmp/demo.mp4"),
        duration_seconds=18.0,
        clip_number=4,
        title="인터페이스 소개",
        cue_source="notes",
        cues=[
            SubtitleCue(0.0, 6.0, "인터페이스 소개: Blender UI의 4가지 주요 영역."),
            SubtitleCue(6.0, 12.0, "3D Viewport — 메인 작업 공간."),
            SubtitleCue(12.0, 18.0, "Outliner — 씬 오브젝트 목록."),
        ],
    )

    content = build_outline_card_content(draft)

    assert isinstance(content, OutlineCardContent)
    assert content.summary == "Blender UI의 4가지 주요 영역."
    assert content.items[0].title == "3D Viewport"
    assert content.items[0].subtitle == "메인 작업 공간"


def test_prepend_outline_opener_prefers_concat_copy_for_audio(monkeypatch, tmp_path: Path) -> None:
    output_path = tmp_path / "output.mp4"

    monkeypatch.setattr("lessonforge.subtitles.find_ffmpeg", lambda: "ffmpeg")
    monkeypatch.setattr(
        "lessonforge.subtitles.probe_video",
        lambda _: VideoProbeInfo(
            width=1920,
            height=1080,
            duration_seconds=42.0,
            fps=30.0,
            has_audio=True,
            sample_rate=44100,
        ),
    )
    monkeypatch.setattr(
        "lessonforge.subtitles._prepend_outline_opener_concat_copy",
        lambda *args, **kwargs: output_path,
    )

    def _unexpected_reencode(*args, **kwargs):
        raise AssertionError("reencode fallback should not run")

    monkeypatch.setattr(
        "lessonforge.subtitles._prepend_outline_opener_reencode",
        _unexpected_reencode,
    )

    result = prepend_outline_opener(
        tmp_path / "input.mp4",
        tmp_path / "card.png",
        output_path,
    )

    assert result == output_path


def test_prepend_outline_opener_falls_back_when_concat_copy_fails(
    monkeypatch,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "output.mp4"

    monkeypatch.setattr("lessonforge.subtitles.find_ffmpeg", lambda: "ffmpeg")
    monkeypatch.setattr(
        "lessonforge.subtitles.probe_video",
        lambda _: VideoProbeInfo(
            width=1920,
            height=1080,
            duration_seconds=42.0,
            fps=30.0,
            has_audio=True,
            sample_rate=44100,
        ),
    )

    def _raise_concat(*args, **kwargs):
        raise RuntimeError("concat failed")

    monkeypatch.setattr(
        "lessonforge.subtitles._prepend_outline_opener_concat_copy",
        _raise_concat,
    )
    monkeypatch.setattr(
        "lessonforge.subtitles._prepend_outline_opener_reencode",
        lambda *args, **kwargs: output_path,
    )

    result = prepend_outline_opener(
        tmp_path / "input.mp4",
        tmp_path / "card.png",
        output_path,
    )

    assert result == output_path
