"""Keystroke timestamp logger for educational video overlays.

Records keypresses with timestamps during screen recording,
then exports as SRT subtitle file for FFmpeg overlay.
"""

from __future__ import annotations

import threading
import time
from datetime import timedelta
from pathlib import Path
from typing import Optional

import srt


# Blender-specific key labels for cleaner display
BLENDER_KEY_LABELS: dict[str, str] = {
    "g": "G  Move",
    "r": "R  Rotate",
    "s": "S  Scale",
    "e": "E  Extrude",
    "i": "I  Insert Keyframe",
    "x": "X  Delete",
    "tab": "Tab  Edit Mode",
    "ctrl+z": "Ctrl+Z  Undo",
    "ctrl+shift+z": "Ctrl+Shift+Z  Redo",
    "ctrl+a": "Ctrl+A  Apply",
    "ctrl+j": "Ctrl+J  Join",
    "ctrl+p": "Ctrl+P  Parent",
    "shift+a": "Shift+A  Add Menu",
    "shift+d": "Shift+D  Duplicate",
    "shift+s": "Shift+S  Snap Menu",
    "a": "A  Select All",
    "alt+a": "Alt+A  Deselect All",
    "numpad1": "Numpad 1  Front View",
    "numpad3": "Numpad 3  Side View",
    "numpad5": "Numpad 5  Ortho",
    "numpad7": "Numpad 7  Top View",
    "numpad0": "Numpad 0  Camera View",
    "z": "Z  Shading Pie",
    "n": "N  Properties Panel",
    "m": "M  Move to Collection",
    "h": "H  Hide",
    "alt+h": "Alt+H  Unhide All",
    "k": "K  Knife",
    "ctrl+r": "Ctrl+R  Loop Cut",
    "ctrl+b": "Ctrl+B  Bevel",
    "ctrl+e": "Ctrl+E  Edge Menu",
    "ctrl+f": "Ctrl+F  Face Menu",
    "ctrl+v": "Ctrl+V  Vertex Menu",
    "p": "P  Separate",
    "u": "U  UV Unwrap",
    "f": "F  Fill Face",
    "y": "Y  Split",
    "v": "V  Rip",
    "alt+s": "Alt+S  Shrink/Fatten",
    "o": "O  Proportional Edit",
}


class KeystrokeLogger:
    """Records keystrokes with timestamps during screen recording.

    Usage:
        logger = KeystrokeLogger()
        logger.start()
        # ... do Blender demo ...
        logger.stop()
        logger.save_srt("keystrokes.srt")
    """

    def __init__(self, display_duration: float = 1.5):
        self.display_duration = display_duration
        self._events: list[tuple[float, str]] = []  # (timestamp, label)
        self._start_time: Optional[float] = None
        self._listener: Optional[object] = None
        self._lock = threading.Lock()
        self._modifier_keys: set[str] = set()

    def start(self) -> None:
        """Begin recording keystrokes."""
        try:
            from pynput import keyboard

            self._start_time = time.time()
            self._events.clear()

            def on_press(key):
                self._handle_key(key, pressed=True)

            def on_release(key):
                self._handle_release(key)

            self._listener = keyboard.Listener(
                on_press=on_press,
                on_release=on_release,
            )
            self._listener.start()
        except ImportError:
            print("⚠️  pynput not installed - keystroke logging disabled")

    def stop(self) -> None:
        """Stop recording keystrokes."""
        if self._listener:
            self._listener.stop()
            self._listener = None

    def _handle_key(self, key, pressed: bool) -> None:
        """Process a key press event."""
        if self._start_time is None:
            return

        try:
            from pynput import keyboard

            # Track modifiers
            if key in (
                keyboard.Key.ctrl, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
                keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r,
                keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r,
                keyboard.Key.cmd, keyboard.Key.cmd_l, keyboard.Key.cmd_r,
            ):
                mod_name = self._modifier_name(key)
                if mod_name:
                    self._modifier_keys.add(mod_name)
                return

            # Build key string with modifiers
            key_str = self._build_key_string(key)
            if not key_str:
                return

            # Look up Blender label
            label = BLENDER_KEY_LABELS.get(key_str.lower(), key_str.upper())

            timestamp = time.time() - self._start_time
            with self._lock:
                self._events.append((timestamp, label))

        except Exception:
            pass

    def _handle_release(self, key) -> None:
        """Remove released modifier keys."""
        try:
            from pynput import keyboard
            mod_name = self._modifier_name(key)
            if mod_name:
                self._modifier_keys.discard(mod_name)
        except Exception:
            pass

    def _modifier_name(self, key) -> Optional[str]:
        """Get normalized modifier name."""
        try:
            from pynput import keyboard
            mapping = {
                keyboard.Key.ctrl: "ctrl", keyboard.Key.ctrl_l: "ctrl",
                keyboard.Key.ctrl_r: "ctrl",
                keyboard.Key.shift: "shift", keyboard.Key.shift_l: "shift",
                keyboard.Key.shift_r: "shift",
                keyboard.Key.alt: "alt", keyboard.Key.alt_l: "alt",
                keyboard.Key.alt_r: "alt",
                keyboard.Key.cmd: "cmd", keyboard.Key.cmd_l: "cmd",
                keyboard.Key.cmd_r: "cmd",
            }
            return mapping.get(key)
        except Exception:
            return None

    def _build_key_string(self, key) -> str:
        """Build a composite key string like 'ctrl+shift+z'."""
        try:
            from pynput import keyboard

            # Get base key name
            if hasattr(key, "char") and key.char:
                base = key.char.lower()
            elif hasattr(key, "name"):
                name_map = {
                    "space": "space", "enter": "enter", "backspace": "backspace",
                    "delete": "delete", "escape": "escape", "tab": "tab",
                    "num0": "numpad0", "num1": "numpad1", "num2": "numpad2",
                    "num3": "numpad3", "num4": "numpad4", "num5": "numpad5",
                    "num6": "numpad6", "num7": "numpad7",
                    "f1": "f1", "f2": "f2", "f3": "f3", "f4": "f4",
                    "f5": "f5", "f12": "f12",
                }
                base = name_map.get(key.name, key.name)
            else:
                return ""

            # Skip pure modifier keys
            if base in ("ctrl", "shift", "alt", "cmd"):
                return ""

            # Build with sorted modifiers for consistent lookup
            mods = sorted(self._modifier_keys)
            parts = mods + [base]
            return "+".join(parts)

        except Exception:
            return ""

    def to_srt(self) -> str:
        """Convert recorded events to SRT subtitle format."""
        with self._lock:
            events = list(self._events)

        subtitles = []
        for i, (ts, label) in enumerate(events):
            start = timedelta(seconds=ts)
            end = timedelta(seconds=ts + self.display_duration)
            subtitles.append(
                srt.Subtitle(index=i + 1, start=start, end=end, content=label)
            )

        return srt.compose(subtitles)

    def save_srt(self, output_path: Path) -> None:
        """Save SRT file for FFmpeg overlay."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_srt(), encoding="utf-8")

    def event_count(self) -> int:
        """Return number of recorded events."""
        with self._lock:
            return len(self._events)
