#!/usr/bin/env bash
# Records the current HEAD commit's short hash into version.txt and creates
# a second "stamp" commit. The stamp commit contains ONLY version.txt so the
# feature commit (HEAD~1 after stamping) stays the one users see.
#
# Usage: run AFTER `git commit` and BEFORE `git push`.
# Idempotent — re-running on an already-stamped head is a no-op.
set -euo pipefail

cd "$(dirname "$0")/.."

# If HEAD is already a stamp commit, do nothing (avoid infinite chains).
LAST_MSG="$(git log -1 --pretty=%s)"
if [ "$LAST_MSG" = "chore: stamp build hash" ]; then
  echo "HEAD is already a stamp commit, skipping."
  git rev-parse --short=7 HEAD
  exit 0
fi

HASH="$(git rev-parse --short=7 HEAD)"
echo "$HASH" > version.txt
git add version.txt

# Only commit if version.txt actually changed (prevents empty commits).
if ! git diff --cached --quiet -- version.txt; then
  git commit -m "chore: stamp build hash" --no-verify
fi

git rev-parse --short=7 HEAD
