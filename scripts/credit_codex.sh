#!/usr/bin/env bash
# credit_codex.sh — rewrite last N commits to set Author=codex and add trailer
# Usage:
#   scripts/credit_codex.sh <codex_noreply_email> [branch=rescue-*] [N=10]
# Example:
#   scripts/credit_codex.sh 223734131+codex@users.noreply.github.com rescue-20251116-143914 10

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <codex_noreply_email> [branch] [N]" >&2
  exit 2
fi

CEMAIL="$1"
TARGET_BRANCH="${2:-}"
NCOMMITS="${3:-10}"

ROOT=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [[ -z "$ROOT" ]]; then
  echo "Not inside a git repository" >&2
  exit 1
fi
cd "$ROOT"

if [[ -n "$TARGET_BRANCH" ]]; then
  echo "→ Switching to $TARGET_BRANCH"
  git switch "$TARGET_BRANCH"
else
  TARGET_BRANCH=$(git branch --show-current)
  echo "→ Using current branch $TARGET_BRANCH"
fi

COUNT=$(git rev-list --count HEAD)
if [[ "$COUNT" -lt 2 ]]; then
  echo "Not enough commits to rewrite (count=$COUNT)" >&2
  exit 0
fi

RANGE=$(( COUNT < NCOMMITS ? COUNT-1 : NCOMMITS ))
if [[ "$RANGE" -lt 1 ]]; then
  echo "Computed range too small ($RANGE)" >&2
  exit 0
fi

echo "→ Rewriting last $RANGE commits with Author=codex <$CEMAIL> and adding Co-authored-by trailer"
export GIT_SEQUENCE_EDITOR=:
git rebase -i --rebase-merges --exec "bash -lc 'msg=\$(git log -1 --pretty=%B); line=\"Co-authored-by: codex <${CEMAIL}>\"; echo \"\$msg\" | grep -qF \"\$line\" || msg=\"\$msg\\n\\n\$line\"; git commit --amend -m \"\$msg\" --author=\"codex <${CEMAIL}>\"'" HEAD~$RANGE

echo "→ Top commit header:"
git show --no-patch --pretty=full HEAD | sed -n '1,6p'

echo "→ Done. Push with: git push -u origin $TARGET_BRANCH (force if you rewrote published commits)"
