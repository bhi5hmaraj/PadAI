#!/usr/bin/env bash
set -euo pipefail

# gp.sh - Convenience wrapper for `git push` with extra flags
#
# Usage:
#   scripts/gp.sh [--skip-docker] [--no-verify] [<git push args...>]
#
# Flags:
#   --skip-docker   Skip the Docker build smoke test in pre-push hook (one-shot)
#   --no-verify     Pass through to `git push --no-verify`

ROOT_DIR=$(git rev-parse --show-toplevel)
cd "$ROOT_DIR"

PASS_ARGS=()
SKIP_DOCKER=0
NO_VERIFY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-docker)
      SKIP_DOCKER=1; shift ;;
    --no-verify)
      NO_VERIFY=1; shift ;;
    *)
      PASS_ARGS+=("$1"); shift ;;
  esac
done

if [[ $SKIP_DOCKER -eq 1 ]]; then
  mkdir -p "$ROOT_DIR/.git"
  echo "$(date -Is)" > "$ROOT_DIR/.git/prepush.skip_docker"
  echo "[gp] Set one-shot flag to skip Docker build in pre-push"
fi

if [[ $NO_VERIFY -eq 1 ]]; then
  echo "[gp] Running: git push --no-verify ${PASS_ARGS[*]}"
  git push --no-verify "${PASS_ARGS[@]}"
else
  echo "[gp] Running: git push ${PASS_ARGS[*]}"
  git push "${PASS_ARGS[@]}"
fi

