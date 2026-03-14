"""Free Korean TTS using Microsoft Edge's neural voices.

edge-tts provides access to Microsoft's high-quality neural TTS voices
completely free of charge with no API key required. Korean voices:
- ko-KR-SunHiNeural (female, warm, clear)
- ko-KR-InJoonNeural (male, calm, professional)
"""

from __future__ import annotations

import asyncio
import json
import tempfile
from pathlib import Path

import edge_tts

from .base import AudioResult, TTSEngine

# Default Korean voices
DEFAULT_VOICE = "ko-KR-SunHiNeural"
AVAILABLE_KOREAN_VOICES = [
    {"id": "ko-KR-SunHiNeural", "name": "선희 (여성)", "gender": "Female"},
    {"id": "ko-KR-InJoonNeural", "name": "인준 (남성)", "gender": "Male"},
]


class EdgeTTSEngine(TTSEngine):
    """Free TTS engine using Microsoft Edge neural voices."""

    @property
    def name(self) -> str:
        return "Edge TTS (Free)"

    async def synthesize(
        self,
        text: str,
        output_path: Path,
        *,
        voice: str = "",
        rate: str = "+0%",
        pitch: str = "+0Hz",
    ) -> AudioResult:
        voice = voice or DEFAULT_VOICE
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Generate audio + subtitle data
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            pitch=pitch,
        )

        # Save audio
        audio_path = output_path.with_suffix(".mp3")
        subtitle_path = output_path.with_suffix(".srt")

        submaker = edge_tts.SubMaker()

        with open(audio_path, "wb") as audio_file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    submaker.feed(chunk)

        # Save subtitles
        srt_content = submaker.get_srt()
        if srt_content:
            subtitle_path.write_text(srt_content, encoding="utf-8")
        else:
            subtitle_path = None

        # Get audio duration
        duration = await _get_audio_duration(audio_path)

        return AudioResult(
            audio_path=audio_path,
            duration_seconds=duration,
            sample_rate=24000,
            subtitle_path=subtitle_path,
        )

    async def list_voices(self, language: str = "ko") -> list[dict]:
        voices = await edge_tts.list_voices()
        return [
            {"id": v["ShortName"], "name": v["FriendlyName"], "gender": v["Gender"]}
            for v in voices
            if v["Locale"].startswith(language)
        ]


async def _get_audio_duration(audio_path: Path) -> float:
    """Get audio duration in seconds using mutagen."""
    try:
        from mutagen.mp3 import MP3

        audio = MP3(str(audio_path))
        return audio.info.length
    except Exception:
        # Fallback: estimate from file size (128kbps MP3 ≈ 16KB/sec)
        size = audio_path.stat().st_size
        return size / 16000


async def synthesize_blocks(
    blocks: list[dict],
    output_dir: Path,
    voice: str = DEFAULT_VOICE,
    rate: str = "+5%",
) -> list[AudioResult]:
    """Synthesize multiple narration blocks to audio files.

    Args:
        blocks: List of dicts with 'id' and 'text' keys.
        output_dir: Directory to save audio files.
        voice: Korean voice to use.
        rate: Speech rate.

    Returns:
        List of AudioResult objects.
    """
    engine = EdgeTTSEngine()
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[AudioResult] = []

    for block in blocks:
        block_id = block["id"]
        text = block["text"]

        if not text.strip():
            continue

        output_path = output_dir / f"{block_id}"
        result = await engine.synthesize(
            text=text,
            output_path=output_path,
            voice=voice,
            rate=rate,
        )
        results.append(result)

    return results
