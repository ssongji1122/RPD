from __future__ import annotations

import os
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parent
DEFAULT_ROOT = TOOLS_DIR.parent


def _resolve_path(env_name: str, default: Path) -> Path:
    raw_value = os.environ.get(env_name)
    if raw_value:
        return Path(raw_value).expanduser().resolve()
    return default.expanduser().resolve()


ROOT = _resolve_path("RPD_ROOT_DIR", DEFAULT_ROOT)
COURSE_SITE = _resolve_path("RPD_COURSE_SITE_DIR", ROOT / "course-site")
WEEKS_DIR = _resolve_path("RPD_WEEKS_DIR", ROOT / "weeks")
CANONICAL_JSON = _resolve_path("RPD_CANONICAL_JSON", WEEKS_DIR / "site-data.json")
SCHEMA_JSON = _resolve_path("RPD_SCHEMA_JSON", WEEKS_DIR / "site-data.schema.json")
CONTRACTS_SCHEMA_JSON = _resolve_path(
    "RPD_CONTRACTS_SCHEMA_JSON",
    WEEKS_DIR / "contracts.schema.json",
)
GENERATED_JSON = _resolve_path("RPD_GENERATED_JSON", COURSE_SITE / "data" / "curriculum.json")
GENERATED_JS = _resolve_path("RPD_GENERATED_JS", COURSE_SITE / "data" / "curriculum.js")
IMAGES_DIR = _resolve_path("RPD_IMAGES_DIR", COURSE_SITE / "assets" / "images")
VIDEOS_DIR = _resolve_path("RPD_VIDEOS_DIR", COURSE_SITE / "assets" / "videos")
AUDIT_LOG_PATH = _resolve_path("RPD_AUDIT_LOG_PATH", ROOT / "tmp" / "admin-audit.log")
