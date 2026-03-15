#!/usr/bin/env python3
"""Sync lecture-note managed blocks from course-site/data/curriculum.js."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ADMIN_SERVER_PATH = ROOT / "tools" / "admin-server.py"


def _load_admin_server():
    spec = importlib.util.spec_from_file_location("admin_server", ADMIN_SERVER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load admin server module from {ADMIN_SERVER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    admin_server = _load_admin_server()
    curriculum = admin_server.read_curriculum()
    updated = admin_server.sync_lecture_notes(curriculum)

    print(f"Lecture notes synced: {len(updated)}")
    for path in updated:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
