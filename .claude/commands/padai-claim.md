# /padai-claim — Claim next PadAI task

Use: Claim the next ready task from the PadAI master server and print details.

```bash
export PADAI_MASTER="${PADAI_MASTER:-http://localhost:8000}"
export AGENT_NAME="${AGENT_NAME:-padai-worker-$$}"

TASK=$(curl -s -X POST "$PADAI_MASTER/api/claim" \
  -H "Content-Type: application/json" \
  -d "{\"agent_name\": \"$AGENT_NAME\"}")

echo "$TASK" | jq

# Convenience exports for follow-up commands
export PADAI_TASK_ID=$(echo "$TASK" | jq -r '.task.id')
export PADAI_TASK_TITLE=$(echo "$TASK" | jq -r '.task.title')
echo "📋 Working on: ${PADAI_TASK_ID:-none} — ${PADAI_TASK_TITLE:-}"
```

