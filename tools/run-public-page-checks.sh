#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_ROOT}"

python3 -m pytest \
  tools/tests/test_public_pages.py \
  tools/tests/test_public_page_styles_e2e.py \
  tools/tests/test_admin_e2e.py \
  -q \
  -k 'public_pages or public_page_styles_e2e or sidebar_section_active_link_uses_text_priority_state'
