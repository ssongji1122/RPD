"""Smoke tests for the Notion-as-SoT safety guards and body-mirror infrastructure.

Run directly:
    python3 tests/test_notion_safety.py
"""
from __future__ import annotations

import inspect
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

PASSED: list[str] = []
FAILED: list[str] = []


def _check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        PASSED.append(name)
        print(f"  ✓ {name}")
    else:
        FAILED.append(f"{name} — {detail}")
        print(f"  ✗ {name} — {detail}")


def section(title: str) -> None:
    print(f"\n=== {title} ===")


# ---------------------------------------------------------------------------
# Step 2: curriculum-push.py safety guard
# ---------------------------------------------------------------------------
section("Step 2: curriculum-push.py safety guard")

env = {**os.environ}
env.pop("NOTION_TOKEN", None)

result = subprocess.run(
    [sys.executable, str(TOOLS / "curriculum-push.py"), "--week", "9"],
    capture_output=True, text=True, env=env, cwd=ROOT,
)
combined = result.stdout + result.stderr
_check(
    "dry-run runs without NOTION_TOKEN",
    result.returncode == 0,
    f"exit {result.returncode}",
)
_check(
    "dry-run prints DRY-RUN MODE banner",
    "DRY-RUN MODE" in combined,
    "banner missing",
)
_check(
    "dry-run does NOT print success ✓ marker (no API call)",
    "✓ Week 09" not in combined,
    "looks like real push happened",
)
_check(
    "dry-run output mentions [dry-run] for week 9",
    "[dry-run] Week 09" in combined,
    "missing dry-run line",
)

result_help = subprocess.run(
    [sys.executable, str(TOOLS / "curriculum-push.py"), "--help"],
    capture_output=True, text=True, cwd=ROOT,
)
_check(
    "--help advertises --confirm-destructive flag",
    "--confirm-destructive" in result_help.stdout,
    "flag missing",
)
_check(
    "--help marks tool as DEPRECATED",
    "DEPRECATED" in result_help.stdout,
    "deprecation note missing",
)


# ---------------------------------------------------------------------------
# Step 2: start-admin.sh sync-to-notion guard
# ---------------------------------------------------------------------------
section("Step 2: start-admin.sh sync-to-notion guard")

result = subprocess.run(
    ["bash", str(ROOT / "start-admin.sh"), "sync-to-notion"],
    capture_output=True, text=True, cwd=ROOT,
)
combined = result.stdout + result.stderr
_check(
    "sync-to-notion exits non-zero",
    result.returncode != 0,
    f"got exit {result.returncode}",
)
_check(
    "sync-to-notion prints DEPRECATED notice",
    "DEPRECATED" in combined,
    "notice missing",
)
_check(
    "sync-to-notion suggests sync-to-notion-force or --confirm-destructive",
    "sync-to-notion-force" in combined or "--confirm-destructive" in combined,
    "no escape hatch hint",
)


# ---------------------------------------------------------------------------
# Step 2: admin-server.py notion_push_enabled() default-false
# ---------------------------------------------------------------------------
section("Step 2: admin-server.py push gate")

env_no_flag = {**os.environ, "NOTION_TOKEN": "fake-token"}
env_no_flag.pop("RPD_ALLOW_NOTION_PUSH", None)
env_with_flag = {**env_no_flag, "RPD_ALLOW_NOTION_PUSH": "1"}

snippet = """
import sys
sys.path.insert(0, %r)
import importlib.util
spec = importlib.util.spec_from_file_location('admin_server', %r)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print('enabled=', mod.notion_push_enabled())
""" % (str(TOOLS), str(TOOLS / "admin-server.py"))

r1 = subprocess.run([sys.executable, "-c", snippet], capture_output=True, text=True, env=env_no_flag, cwd=ROOT)
r2 = subprocess.run([sys.executable, "-c", snippet], capture_output=True, text=True, env=env_with_flag, cwd=ROOT)
_check(
    "notion_push_enabled() = False without RPD_ALLOW_NOTION_PUSH",
    "enabled= False" in r1.stdout,
    f"got: {r1.stdout.strip()}; stderr: {r1.stderr[:200]}",
)
_check(
    "notion_push_enabled() = True when RPD_ALLOW_NOTION_PUSH=1",
    "enabled= True" in r2.stdout,
    f"got: {r2.stdout.strip()}; stderr: {r2.stderr[:200]}",
)


# ---------------------------------------------------------------------------
# Step 2: admin.html button hidden
# ---------------------------------------------------------------------------
section("Step 2: admin.html push button disabled")

admin_html = (ROOT / "course-site" / "admin.html").read_text(encoding="utf-8")
button_match = re.search(r'<button[^>]*id="notionPushAllBtn"[^>]*>', admin_html)
_check("notionPushAllBtn element still present", button_match is not None, "")
if button_match:
    tag = button_match.group(0)
    _check("button has 'hidden' attribute", "hidden" in tag, tag[:120])
    _check("button has 'disabled' attribute", "disabled" in tag, tag[:120])


# ---------------------------------------------------------------------------
# Step 3: notion_api new functions
# ---------------------------------------------------------------------------
section("Step 3: notion_api body-mirror surface")

import notion_api

_check("fetch_block_tree exists", hasattr(notion_api, "fetch_block_tree"), "")
_check("download_block_assets exists", hasattr(notion_api, "download_block_assets"), "")
_check("_resolve_block_file_url exists", hasattr(notion_api, "_resolve_block_file_url"), "")

if hasattr(notion_api, "fetch_block_tree"):
    sig = inspect.signature(notion_api.fetch_block_tree)
    _check(
        "fetch_block_tree signature(page_id, token=None)",
        list(sig.parameters.keys()) == ["page_id", "token"],
        f"got {list(sig.parameters.keys())}",
    )

if hasattr(notion_api, "download_block_assets"):
    sig = inspect.signature(notion_api.download_block_assets)
    _check(
        "download_block_assets signature(blocks, dest_dir, public_prefix)",
        list(sig.parameters.keys()) == ["blocks", "dest_dir", "public_prefix"],
        f"got {list(sig.parameters.keys())}",
    )

# _resolve_block_file_url unit test (no network)
if hasattr(notion_api, "_resolve_block_file_url"):
    block_image_file = {
        "type": "image",
        "image": {"type": "file", "file": {"url": "https://prod-files.com/abc.png?signed"}},
    }
    block_image_external = {
        "type": "image",
        "image": {"type": "external", "external": {"url": "https://example.com/img.png"}},
    }
    block_paragraph = {"type": "paragraph", "paragraph": {"rich_text": []}}

    r = notion_api._resolve_block_file_url(block_image_file)
    _check(
        "_resolve_block_file_url(file image) returns (url, 'file')",
        r is not None and r[1] == "file",
        f"got {r}",
    )
    r = notion_api._resolve_block_file_url(block_image_external)
    _check(
        "_resolve_block_file_url(external image) returns (url, 'external')",
        r is not None and r[1] == "external",
        f"got {r}",
    )
    r = notion_api._resolve_block_file_url(block_paragraph)
    _check(
        "_resolve_block_file_url(paragraph) returns None",
        r is None,
        f"got {r}",
    )


# ---------------------------------------------------------------------------
# Step 3: notion-sync.py CLI flags
# ---------------------------------------------------------------------------
section("Step 3: notion-sync.py CLI surface")

result = subprocess.run(
    [sys.executable, str(TOOLS / "notion-sync.py"), "--help"],
    capture_output=True, text=True, cwd=ROOT,
)
_check("notion-sync.py --help works", result.returncode == 0, result.stderr[:200])
_check("--no-body flag advertised", "--no-body" in result.stdout, "")
_check("--weeks N flag advertised", "--weeks" in result.stdout, "")


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print(f"PASSED: {len(PASSED)}")
print(f"FAILED: {len(FAILED)}")
if FAILED:
    print("\nFailed tests:")
    for f in FAILED:
        print(f"  - {f}")
    sys.exit(1)
print("\nAll smoke tests passed ✓")
sys.exit(0)
