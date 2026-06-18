#!/usr/bin/env sh
# Download the prebuilt GitNexus database for gajae-code so the GitNexus MCP tools
# and wiki work immediately, without re-running (paid) AI analysis.
#
# The database (.gitnexus/lbug, ~283MB) exceeds GitHub's 100MB per-file limit, so
# it is shipped as a GitHub Release asset instead of being committed to the repo.
set -eu

REPO="HyunjunJeon/fastcampus-harness-engineering-course"
TAG="gitnexus-db-v1"
ASSET="gajae-code-lbug"

DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
DEST="$DIR/lbug"
URL="https://github.com/$REPO/releases/download/$TAG/$ASSET"

echo "Downloading GitNexus DB"
echo "  from: $URL"
echo "  to:   $DEST"
curl -fL --progress-bar -o "$DEST" "$URL"
echo "Done ($(du -h "$DEST" | cut -f1)). GitNexus is ready to use."
echo
echo "Parser caches (parse-cache/, parsedfile-cache/) are optional, only needed for"
echo "incremental re-analysis. They regenerate as a side effect of re-running analysis,"
echo "which re-runs the (paid) AI step -- most viewers should skip it:"
echo "  bun run gitnexus:analyze"
