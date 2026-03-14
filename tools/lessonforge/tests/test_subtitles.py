from pathlib import Path

from lessonforge.subtitles import (
    ClipNotes,
    SubtitleNoteLibrary,
    generate_subtitle_draft,
    parse_clip_notes,
    parse_week_video_map,
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
