#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <skill-name>" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_NAME="$1"
SOURCE_DIR="${REPO_ROOT}/.claude/skills/${SKILL_NAME}"
CODEX_HOME_DIR="${CODEX_HOME:-${HOME}/.codex}"
TARGET_DIR="${CODEX_HOME_DIR}/skills/${SKILL_NAME}"

if [[ ! -d "${SOURCE_DIR}" ]]; then
  echo "Skill not found in repo: ${SOURCE_DIR}" >&2
  exit 1
fi

mkdir -p "${CODEX_HOME_DIR}/skills"
rsync -a --delete "${SOURCE_DIR}/" "${TARGET_DIR}/"
echo "Synced ${SKILL_NAME} -> ${TARGET_DIR}"
