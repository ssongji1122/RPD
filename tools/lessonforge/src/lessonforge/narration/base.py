"""Abstract base class for TTS engines.

Strategy pattern allows swapping between free (edge-tts) and paid (ElevenLabs,
Supertone) TTS providers with a single config change.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AudioResult:
    """Result of a TTS synthesis operation."""

    audio_path: Path
    duration_seconds: float
    sample_rate: int = 44100
    subtitle_path: Path | None = None  # SRT/VTT if available


class TTSEngine(ABC):
    """Abstract TTS engine interface."""

    @abstractmethod
    async def synthesize(
        self,
        text: str,
        output_path: Path,
        *,
        voice: str = "",
        rate: str = "+0%",
        pitch: str = "+0Hz",
    ) -> AudioResult:
        """Synthesize text to audio file.

        Args:
            text: Korean text to synthesize.
            output_path: Where to save the audio file (.mp3 or .wav).
            voice: Voice ID or name (engine-specific).
            rate: Speech rate adjustment (e.g., "+10%", "-5%").
            pitch: Pitch adjustment (e.g., "+2Hz", "-1Hz").

        Returns:
            AudioResult with file path and duration.
        """
        ...

    @abstractmethod
    async def list_voices(self, language: str = "ko") -> list[dict]:
        """List available voices for a language.

        Returns list of dicts with at least 'id' and 'name' keys.
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of this TTS engine."""
        ...
