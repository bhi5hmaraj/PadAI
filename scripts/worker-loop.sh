#!/usr/bin/env bash
# worker-loop.sh - Continuous PadAI worker agent

set -euo pipefail

PADAI_MASTER="${PADAI_MASTER:-http://localhost:8000}"
AGENT_NAME="${AGENT_NAME:-padai-worker-$$}"
SLEEP_SECONDS="${SLEEP_SECONDS:-30}"

echo "🤖 Agent: $AGENT_NAME"
echo "🌐 Master: $PADAI_MASTER"
echo

while true; do
  echo "🔍 Checking for available tasks..."

  READY_COUNT=$(curl -s "$PADAI_MASTER/api/status" | jq -r '.ready // 0' || echo 0)

  if [[ "$READY_COUNT" -eq 0 ]]; then
    echo "⏸️  No tasks ready. Waiting ${SLEEP_SECONDS}s..."
    sleep "$SLEEP_SECONDS"
    continue
  fi

  echo "📋 $READY_COUNT tasks available. Claiming one..."

  TASK=$(curl -s -X POST "$PADAI_MASTER/api/claim" \
    -H "Content-Type: application/json" \
    -d "{\"agent_name\": \"$AGENT_NAME\"}")

  TASK_ID=$(echo "$TASK" | jq -r '.task.id')
  TASK_TITLE=$(echo "$TASK" | jq -r '.task.title')

  if [[ "$TASK_ID" == "null" || -z "$TASK_ID" ]]; then
    echo "❌ Failed to claim task. Retrying in 10s..."
    sleep 10
    continue
  fi

  echo "✅ Claimed: $TASK_ID - $TASK_TITLE"
  echo
  echo "Task details:"
  echo "$TASK" | jq '.task'
  echo

  # TODO: Implement task-specific work here. For now, simulate work.
  echo "⚙️  Working on task $TASK_ID..."
  sleep 5

  echo "Completing task $TASK_ID..."
  curl -s -X POST "$PADAI_MASTER/api/complete" \
    -H "Content-Type: application/json" \
    -d "{\"task_id\": \"$TASK_ID\"}" | jq

  echo "✅ Task $TASK_ID completed!"
  echo
  echo "---"
  echo
done

