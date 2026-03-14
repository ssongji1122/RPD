"""OBS Studio controller via WebSocket API.

Controls OBS recording start/stop programmatically.
Requires OBS 28+ with built-in WebSocket server enabled.

Setup in OBS:
  Tools > WebSocket Server Settings > Enable WebSocket server
  Default port: 4455, no password required for local use
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Optional


class OBSController:
    """Controls OBS Studio via WebSocket for automated recording.

    Usage:
        obs = OBSController()
        if obs.connect():
            obs.start_recording()
            time.sleep(60)  # record for 60 seconds
            output_path = obs.stop_recording()
    """

    def __init__(self, host: str = "localhost", port: int = 4455, password: str = ""):
        self.host = host
        self.port = port
        self.password = password
        self._client = None
        self._available = False

    def connect(self) -> bool:
        """Attempt to connect to OBS WebSocket server."""
        try:
            import obsws_python as obs

            self._client = obs.ReqClient(
                host=self.host,
                port=self.port,
                password=self.password,
                timeout=3,
            )
            self._available = True
            return True
        except ImportError:
            print("⚠️  obsws-python not installed. Install: pip install obsws-python")
            return False
        except Exception as e:
            print(f"⚠️  OBS not connected: {e}")
            print("   Make sure OBS is running with WebSocket server enabled")
            print("   OBS > Tools > WebSocket Server Settings")
            return False

    def start_recording(self) -> bool:
        """Start OBS recording."""
        if not self._available or not self._client:
            return False
        try:
            self._client.start_record()
            time.sleep(1)  # Give OBS a moment to start
            return True
        except Exception as e:
            print(f"⚠️  Failed to start recording: {e}")
            return False

    def stop_recording(self) -> Optional[Path]:
        """Stop OBS recording and return output file path."""
        if not self._available or not self._client:
            return None
        try:
            response = self._client.stop_record()
            # OBS returns the output path
            output_file = getattr(response, "output_path", None)
            if output_file:
                return Path(output_file)
            return None
        except Exception as e:
            print(f"⚠️  Failed to stop recording: {e}")
            return None

    def is_recording(self) -> bool:
        """Check if OBS is currently recording."""
        if not self._available or not self._client:
            return False
        try:
            status = self._client.get_record_status()
            return getattr(status, "output_active", False)
        except Exception:
            return False

    def set_output_directory(self, directory: Path) -> None:
        """Set OBS recording output directory."""
        if not self._available or not self._client:
            return
        try:
            self._client.set_profile_parameter(
                "SimpleOutput", "FilePath", str(directory)
            )
        except Exception:
            pass

    def disconnect(self) -> None:
        """Disconnect from OBS."""
        if self._client:
            try:
                self._client.disconnect()
            except Exception:
                pass
            self._client = None
            self._available = False
