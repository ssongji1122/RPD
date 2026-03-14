"""ElevenLabs TTS engine (paid upgrade).

Provides higher-quality Korean voice synthesis using ElevenLabs API.
Requires an API key from https://elevenlabs.io.

Setup:
    export ELEVENLABS_API_KEY="sk_..."
    OR set in lessonforge.config.yaml:
        tts:
          engine: elevenlabs
          elevenlabs:
            voice_id: "your_voice_id"
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from .base import AudioResult, TTSEngine


class ElevenLabsEngine(TTSEngine):
    """ElevenLabs Multilingual v2 TTS engine."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        voice_id: str = "",
        model: str = "eleven_multilingual_v2",
        stability: float = 0.5,
        similarity_boost: float = 0.8,
    ):
        self._api_key = api_key or os.environ.get("ELEVENLABS_API_KEY", "")
        self._voice_id = voice_id
        self._model = model
        self._stability = stability
        self._similarity_boost = similarity_boost

        if not self._api_key:
            raise ValueError(
                "ElevenLabs API key required.\n"
                "Set ELEVENLABS_API_KEY env var or pass api_key parameter."
            )

    @property
    def name(self) -> str:
        return "ElevenLabs"

    async def synthesize(
        self,
        text: str,
        output_path: Path,
        *,
        voice: str = "",
        rate: str = "+0%",
        pitch: str = "+0Hz",
    ) -> AudioResult:
        """Synthesize text using ElevenLabs API."""
        try:
            from elevenlabs import ElevenLabs
        except ImportError:
            raise ImportError(
                "ElevenLabs SDK required:\n"
                "  pip install elevenlabs"
            )

        voice_id = voice or self._voice_id
        if not voice_id:
            raise ValueError("No voice_id specified for ElevenLabs")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        client = ElevenLabs(api_key=self._api_key)

        audio_generator = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id=self._model,
            voice_settings={
                "stability": self._stability,
                "similarity_boost": self._similarity_boost,
            },
        )

        # Write audio to file
        with open(output_path, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)

        # Get duration
        duration = _get_audio_duration(output_path)

        return AudioResult(
            audio_path=output_path,
            duration_seconds=duration,
            sample_rate=44100,
        )

    async def list_voices(self, language: str = "ko") -> list[dict]:
        """List available ElevenLabs voices."""
        try:
            from elevenlabs import ElevenLabs
        except ImportError:
            return []

        client = ElevenLabs(api_key=self._api_key)
        response = client.voices.get_all()

        voices = []
        for voice in response.voices:
            # Filter for Korean-capable voices if possible
            labels = voice.labels or {}
            voice_lang = labels.get("language", "")
            if language and voice_lang and language not in voice_lang.lower():
                continue

            voices.append({
                "id": voice.voice_id,
                "name": voice.name,
                "gender": labels.get("gender", "unknown"),
                "language": voice_lang,
                "description": labels.get("description", ""),
            })

        return voices


def _get_audio_duration(audio_path: Path) -> float:
    """Get audio duration in seconds."""
    try:
        from mutagen.mp3 import MP3
        return MP3(str(audio_path)).info.length
    except Exception:
        pass

    try:
        import subprocess
        import json
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", str(audio_path)],
            capture_output=True, text=True,
        )
        info = json.loads(result.stdout)
        return float(info["format"]["duration"])
    except Exception:
        return 5.0


async def synthesize_blocks_elevenlabs(
    blocks: list[dict],
    output_dir: Path,
    api_key: str = "",
    voice_id: str = "",
    model: str = "eleven_multilingual_v2",
) -> list[AudioResult]:
    """Batch synthesize narration blocks using ElevenLabs.

    Drop-in replacement for edge_tts_engine.synthesize_blocks().

    Args:
        blocks: List of dicts with 'id' and 'text' keys.
        output_dir: Directory to save audio files.
        api_key: ElevenLabs API key.
        voice_id: Voice ID to use.
        model: Model ID.

    Returns:
        List of AudioResult objects.
    """
    engine = ElevenLabsEngine(api_key=api_key, voice_id=voice_id, model=model)
    results = []

    for block in blocks:
        block_id = block["id"]
        text = block["text"].strip()
        if not text:
            continue

        output_path = output_dir / f"{block_id}.mp3"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        result = await engine.synthesize(text, output_path)
        results.append(result)

    return results
