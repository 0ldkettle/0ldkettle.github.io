#!/usr/bin/env bash
# Stamps the current commit's short hash into version.txt and amends the commit.
# Run this AFTER `git commit` and BEFORE `git push`.
set -euo pipefail

cd "$(dirname "$0")/.."

HASH="$(git rev-parse --short=7 HEAD)"
echo "$HASH" > version.txt
git add version.txt

# Amend only if version.txt actually changed (idempotent for subsequent runs).
if ! git diff --cached --quiet -- version.txt; then
  git commit --amend --no-edit --no-verify
fi

# Output the final hash (may differ from $HASH after amend).
git rev-parse --short=7 HEAD
