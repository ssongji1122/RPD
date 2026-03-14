"""Blender automation agent — blender-mcp v1.5.5 + subprocess fallback.

Primary mode: blender-mcp (JSON-over-TCP socket, localhost:9876)
  - Requires: Blender running with BlenderMCP addon enabled
  - Advantage: Live viewport recording with real UI interaction

Fallback mode: subprocess (headless --background)
  - No addon needed; for rendering/data operations only
  - No live screen recording possible

blender-mcp protocol (v1.5.5):
  - TCP socket: BLENDER_HOST:BLENDER_PORT (default localhost:9876)
  - Framing: 4-byte big-endian uint32 length + UTF-8 JSON body
  - Request types:
      {"type": "execute_code", "code": "<python>"}
      {"type": "get_viewport_screenshot"}
      {"type": "get_scene_info"}
  - Response: {"status": "success"|"error", "result": ..., "message": "..."}

Addon setup:
  1. Download addon.py from https://github.com/ahujasid/blender-mcp
  2. Blender > Edit > Preferences > Add-ons > Install > select addon.py
  3. Enable "Interface: BlenderMCP"
  4. Blender sidebar (N) > BlenderMCP tab > Connect
"""

from __future__ import annotations

import base64
import importlib.util
import json
import os
import socket
import struct
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


# Environment-based configuration (matches blender-mcp addon defaults)
_MCP_HOST = os.environ.get("BLENDER_HOST", "localhost")
_MCP_PORT = int(os.environ.get("BLENDER_PORT", "9876"))
_BLENDER_APP = "/Applications/Blender.app/Contents/MacOS/Blender"


# ─────────────────────────────────────────────────────────────────────────────
# blender-mcp live client (primary mode)
# ─────────────────────────────────────────────────────────────────────────────

class BlenderMCPClient:
    """JSON-over-TCP client for blender-mcp v1.5.5 addon.

    Connects to a running Blender instance with the BlenderMCP addon
    enabled and executes Python code inside Blender's context.
    """

    def __init__(self, host: str = _MCP_HOST, port: int = _MCP_PORT):
        self.host = host
        self.port = port
        self._sock: Optional[socket.socket] = None

    def connect(self, timeout: float = 5.0) -> bool:
        """Connect to blender-mcp socket. Returns True on success."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((self.host, self.port))
            self._sock = sock
            return True
        except (ConnectionRefusedError, OSError) as exc:
            print(f"  BlenderMCP: cannot connect to {self.host}:{self.port}")
            print(f"   Error: {exc}")
            print("   Open Blender, enable BlenderMCP addon, click Connect")
            return False

    def disconnect(self) -> None:
        sock = self._sock
        if sock is not None:
            try:
                sock.close()
            except Exception:
                pass
            self._sock = None

    @property
    def connected(self) -> bool:
        return self._sock is not None

    def _send_recv(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send request JSON, receive response JSON (length-prefixed)."""
        sock = self._sock
        if sock is None:
            raise RuntimeError("Not connected. Call connect() first.")
        raw = json.dumps(payload).encode("utf-8")
        sock.sendall(struct.pack(">I", len(raw)) + raw)
        resp_len = struct.unpack(">I", self._recv_n(4))[0]
        return json.loads(self._recv_n(resp_len).decode("utf-8"))

    def _recv_n(self, n: int) -> bytes:
        """Read exactly n bytes from socket."""
        buf = bytearray()
        while len(buf) < n:
            chunk = self._sock.recv(n - len(buf))  # type: ignore[union-attr]
            if not chunk:
                raise ConnectionError("Blender socket closed unexpectedly")
            buf.extend(chunk)
        return bytes(buf)

    def execute(self, python_code: str) -> Dict[str, Any]:
        """Run Python code inside Blender and return the response dict."""
        response = self._send_recv({"type": "execute_code", "code": python_code})
        if response.get("status") == "error":
            msg: str = str(response.get("message", ""))
            print(f"  Blender exec error: {msg[:200]}")  # type: ignore[index]
        return response

    def get_scene_info(self) -> Dict[str, Any]:
        """Retrieve scene object list from Blender."""
        return self._send_recv({"type": "get_scene_info"})

    def get_viewport_screenshot(self) -> Optional[bytes]:
        """Capture current viewport as PNG bytes (base64 decoded)."""
        resp = self._send_recv({"type": "get_viewport_screenshot"})
        b64 = resp.get("result", "")
        if isinstance(b64, str) and b64:
            return base64.b64decode(b64)
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Headless subprocess agent (fallback mode)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class BlenderConfig:
    """Blender executable and settings for subprocess mode."""
    executable: str = _BLENDER_APP
    default_scene: Optional[str] = None


class BlenderSubprocessAgent:
    """Runs bpy Python scripts in headless Blender (--background)."""

    def __init__(self, config: Optional[BlenderConfig] = None):
        self.config = config or BlenderConfig()

    def verify_blender(self) -> bool:
        try:
            r = subprocess.run(
                [self.config.executable, "--version"],
                capture_output=True, text=True, timeout=10,
            )
            return r.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def run_script(
        self,
        script: str,
        *,
        blend_file: Optional[Path] = None,
        background: bool = True,
        timeout: int = 120,
    ) -> str:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(script)
            script_path = f.name
        cmd = [self.config.executable]
        if background:
            cmd.append("--background")
        if blend_file:
            cmd.append(str(blend_file))
        cmd.extend(["--python", script_path])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        Path(script_path).unlink(missing_ok=True)
        if result.returncode != 0:
            err: str = result.stderr  # type: ignore[assignment]
            raise RuntimeError(f"Blender script failed:\n{err[:500]}")  # type: ignore[index]
        return result.stdout

    def run_script_with_gui(
        self,
        script: str,
        *,
        blend_file: Optional[Path] = None,
    ) -> subprocess.Popen:
        """Launch Blender with GUI for screen recording."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(script)
            script_path = f.name
        cmd = [self.config.executable]
        if blend_file:
            cmd.append(str(blend_file))
        cmd.extend(["--python", script_path])
        return subprocess.Popen(cmd)


# ─────────────────────────────────────────────────────────────────────────────
# Unified BlenderAgent
# ─────────────────────────────────────────────────────────────────────────────

class BlenderAgent:
    """Unified Blender controller.

    Prefers blender-mcp live mode for interactive recordings.
    Falls back to subprocess headless mode for offline operations.

    Usage:
        agent = BlenderAgent()
        if agent.connect_mcp():
            agent.execute("bpy.ops.mesh.primitive_cube_add()")
            agent.disconnect()
        else:
            agent.run_script("import bpy; ...")   # headless fallback
    """

    def __init__(
        self,
        mcp_host: str = _MCP_HOST,
        mcp_port: int = _MCP_PORT,
        blender_config: Optional[BlenderConfig] = None,
    ):
        self._mcp = BlenderMCPClient(host=mcp_host, port=mcp_port)
        self._subprocess = BlenderSubprocessAgent(config=blender_config)
        self._using_mcp = False

    def connect_mcp(self, timeout: float = 5.0) -> bool:
        """Try to connect to running Blender via blender-mcp addon."""
        if self._mcp.connect(timeout=timeout):
            self._using_mcp = True
            print(f"  BlenderMCP connected ({self._mcp.host}:{self._mcp.port})")
            return True
        return False

    def disconnect(self) -> None:
        self._mcp.disconnect()
        self._using_mcp = False

    @property
    def is_live(self) -> bool:
        """True if connected to live Blender via MCP."""
        return self._using_mcp and self._mcp.connected

    def execute(self, python_code: str) -> Dict[str, Any]:
        """Execute Python code in Blender (MCP mode required)."""
        if not self.is_live:
            raise RuntimeError("Not connected to live Blender. Call connect_mcp() first.")
        return self._mcp.execute(python_code)

    def wait(self, seconds: float) -> None:
        """Pause between steps so the viewer can follow along."""
        time.sleep(seconds)

    def clear_scene(self) -> Dict[str, Any]:
        return self.execute(
            "import bpy\n"
            "bpy.ops.object.select_all(action='SELECT')\n"
            "bpy.ops.object.delete(use_global=False)\n"
        )

    def set_viewport_shading(self, mode: str = "MATERIAL") -> Dict[str, Any]:
        """Set 3D viewport shading: WIREFRAME, SOLID, MATERIAL, RENDERED."""
        code = "\n".join([
            "import bpy",
            "for area in bpy.context.screen.areas:",
            "    if area.type == 'VIEW_3D':",
            "        for space in area.spaces:",
            "            if space.type == 'VIEW_3D':",
            f"                space.shading.type = '{mode}'",
            "                break",
        ])
        return self.execute(code)

    def take_screenshot(self) -> Optional[bytes]:
        """Capture viewport PNG (MCP mode only)."""
        if not self.is_live:
            return None
        return self._mcp.get_viewport_screenshot()

    def run_demo_script(self, script_path: Path) -> None:
        """Execute a week-specific demo script via blender-mcp.

        Demo scripts are Python modules that define a STEPS list:
            STEPS = [
                {
                    "label": "Clear scene",
                    "code": "bpy.ops.object.select_all(action='SELECT')\\nbpy.ops.object.delete()",
                    "wait": 2.0,
                },
                ...
            ]

        Scripts are loaded as Python modules via importlib (safe import,
        not eval/exec) and must define a top-level STEPS variable.
        """
        if not script_path.exists():
            print(f"Demo script not found: {script_path}")
            return

        spec = importlib.util.spec_from_file_location("blender_demo", str(script_path))
        if spec is None or spec.loader is None:
            print(f"Cannot load demo module: {script_path}")
            return

        assert spec is not None  # narrow for pyright after None-guard above
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[union-attr]

        steps: List[Dict[str, Any]] = getattr(module, "STEPS", [])
        if not steps:
            print(f"No STEPS list defined in {script_path.name}")
            return

        print(f"  Running {len(steps)} steps from {script_path.name}")
        for i, step in enumerate(steps):
            label = step.get("label", f"Step {i + 1}")
            code = step.get("code", "")
            wait_sec = float(step.get("wait", 2.0))
            print(f"    [{i + 1}/{len(steps)}] {label}")
            if code and self.is_live:
                result = self.execute(code)
                if result.get("status") == "error":
                    print(f"    Error: {result.get('message', '')[:100]}")
            if wait_sec > 0:
                self.wait(wait_sec)

    # Subprocess fallback passthroughs

    def run_script(self, script: str, **kwargs) -> str:
        """Headless script execution (subprocess fallback)."""
        return self._subprocess.run_script(script, **kwargs)

    def run_script_with_gui(self, script: str, **kwargs) -> subprocess.Popen:
        """Launch Blender GUI for recording (subprocess fallback)."""
        return self._subprocess.run_script_with_gui(script, **kwargs)

    def verify_blender(self) -> bool:
        return self._subprocess.verify_blender()


# ─────────────────────────────────────────────────────────────────────────────
# Pre-built Blender demonstration script strings
# ─────────────────────────────────────────────────────────────────────────────

DEMO_SCRIPTS = {
    "view_navigation": (
        "import bpy\n"
        "if 'Cube' not in bpy.data.objects:\n"
        "    bpy.ops.mesh.primitive_cube_add()\n"
        "for area in bpy.context.screen.areas:\n"
        "    if area.type == 'VIEW_3D':\n"
        "        for space in area.spaces:\n"
        "            if space.type == 'VIEW_3D':\n"
        "                space.shading.type = 'SOLID'\n"
        "                break\n"
        "print('View navigation demo complete')\n"
    ),
    "transform_basics": (
        "import bpy, math\n"
        "bpy.ops.object.select_all(action='SELECT')\n"
        "bpy.ops.object.delete()\n"
        "bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))\n"
        "cube = bpy.context.active_object\n"
        "cube.location = (2, 0, 0)\n"
        "cube.rotation_euler = (0, 0, math.radians(45))\n"
        "cube.scale = (1.5, 1.5, 1.5)\n"
        "print('Transform basics demo complete')\n"
    ),
    "basic_modeling": (
        "import bpy\n"
        "bpy.ops.object.select_all(action='SELECT')\n"
        "bpy.ops.object.delete()\n"
        "bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))\n"
        "body = bpy.context.active_object\n"
        "body.name = 'RobotBody'\n"
        "body.scale = (1, 0.6, 1.5)\n"
        "bpy.ops.object.transform_apply(scale=True)\n"
        "bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 3))\n"
        "head = bpy.context.active_object\n"
        "head.name = 'RobotHead'\n"
        "print('Basic robot modeling demo complete')\n"
    ),
    "setup_scene": (
        "import bpy\n"
        "bpy.ops.object.select_all(action='SELECT')\n"
        "bpy.ops.object.delete()\n"
        "bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))\n"
        "bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1))\n"
        "bpy.ops.object.camera_add(location=(7, -7, 5))\n"
        "bpy.context.active_object.rotation_euler = (1.1, 0, 0.8)\n"
        "bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))\n"
        "print('Scene setup complete')\n"
    ),
}


def get_demo_script(step_title: str) -> Optional[str]:
    """Match a step title to a pre-built demo script string."""
    title_lower = step_title.lower()
    if "뷰" in title_lower and ("조작" in title_lower or "navigation" in title_lower):
        return DEMO_SCRIPTS["view_navigation"]
    elif "transform" in title_lower and "기초" in title_lower:
        return DEMO_SCRIPTS["transform_basics"]
    elif "모델링" in title_lower or "modeling" in title_lower:
        return DEMO_SCRIPTS["basic_modeling"]
    elif "씬" in title_lower or "scene" in title_lower:
        return DEMO_SCRIPTS["setup_scene"]
    return None
