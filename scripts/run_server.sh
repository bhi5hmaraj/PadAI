#!/usr/bin/env bash
set -euo pipefail

# Run the full PadAI stack in one command:
# - Builds the frontend (unless SKIP_BUILD=1)
# - Serves the compiled frontend via FastAPI at '/'
# - Starts the Python server (PORT defaults to 8000)
#
# Usage:
#   ./scripts/run_server.sh            # build FE and run API on :8000
#   PORT=9000 ./scripts/run_server.sh  # run on :9000
#   SKIP_BUILD=1 ./scripts/run_server.sh  # skip FE build (uses existing dist/)

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROOT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)

echo "→ PadAI root: $ROOT_DIR"

if [[ "${SKIP_BUILD:-0}" != "1" ]]; then
  echo "→ Building frontend (Vite)"
  pushd "$ROOT_DIR/frontend" >/dev/null
  # Install deps if node_modules is missing
  if [[ ! -d node_modules ]]; then
    npm ci
  else
    npm install --silent --no-fund --no-audit
  fi
  npm run build
  popd >/dev/null
else
  echo "→ Skipping frontend build (SKIP_BUILD=1)"
fi

PORT=${PORT:-8000}
export PORT
echo "→ Starting FastAPI on :$PORT (serving /frontend/dist)"

pushd "$ROOT_DIR" >/dev/null
python main.py
popd >/dev/null

