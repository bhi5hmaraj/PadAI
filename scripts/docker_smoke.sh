#!/usr/bin/env bash
set -euo pipefail

# docker_smoke.sh — Build and run the container locally and probe endpoints.
#
# Usage:
#   scripts/docker_smoke.sh [--no-build] [--keep] [--port 8000] [--name tensegrity-smoke]
#
# Steps:
#   1) docker build -t tensegrity-local:smoke .   (unless --no-build)
#   2) docker run -d --rm -p <port>:8080 --name <name> tensegrity-local:smoke
#   3) Wait for /api/health to be ready (30s)
#   4) GET /, /api/health, /api/status, /api/tasks
#   5) Show BD_VERSION and config from logs
#   6) Stop container unless --keep

NO_BUILD=0
KEEP=0
PORT=8000
NAME="tensegrity-smoke"
IMAGE="tensegrity-local:smoke"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-build) NO_BUILD=1; shift ;;
    --keep) KEEP=1; shift ;;
    --port) PORT="$2"; shift 2 ;;
    --name) NAME="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker not found. Install Docker and retry." >&2
  exit 1
fi

echo "[smoke] Image:  $IMAGE"
echo "[smoke] Name:   $NAME"
echo "[smoke] Port:   http://localhost:$PORT"

if [[ $NO_BUILD -eq 0 ]]; then
  echo "[smoke] Building image..."
  docker build -t "$IMAGE" .
else
  echo "[smoke] Skipping build (--no-build)"
fi

# Stop if already running
if docker ps -a --format '{{.Names}}' | grep -qx "$NAME"; then
  echo "[smoke] Container '$NAME' exists; stopping it first"
  docker stop "$NAME" >/dev/null || true
fi

echo "[smoke] Running container..."
docker run -d --rm \
  -e LOG_LEVEL=DEBUG \
  -p "$PORT:8080" \
  --name "$NAME" \
  "$IMAGE" >/dev/null

cleanup() {
  if [[ $KEEP -eq 0 ]]; then
    echo "[smoke] Stopping container..."
    docker stop "$NAME" >/dev/null || true
  else
    echo "[smoke] Keeping container running (--keep). Name: $NAME"
  fi
}
trap cleanup EXIT

echo "[smoke] Waiting for /api/health (up to 30s)..."
for i in {1..30}; do
  if curl -fsS "http://localhost:$PORT/api/health" >/dev/null; then
    break
  fi
  sleep 1
  if [[ $i -eq 30 ]]; then
    echo "[smoke][ERROR] Backend did not become healthy in time" >&2
    docker logs "$NAME" | tail -n 200 || true
    exit 1
  fi
done

echo "[smoke] GET /";           curl -fsS "http://localhost:$PORT/" >/dev/null && echo "  → OK" || echo "  → FAIL"
echo "[smoke] GET /api/health"; curl -fsS "http://localhost:$PORT/api/health" && echo
echo "[smoke] GET /api/status"; curl -fsS "http://localhost:$PORT/api/status" && echo
echo "[smoke] GET /api/tasks";  curl -fsS "http://localhost:$PORT/api/tasks" | head -c 300 && echo "..." || echo "  → FAIL"

echo "[smoke] Recent logs (BD_VERSION, Config):"
docker logs "$NAME" 2>/dev/null | rg -n "BD_VERSION|Config:|WORKSPACE_PATH|BD_PATH|BEADS_JSONL" || true

echo "[smoke] Done."

