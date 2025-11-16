# /padai-complete — Complete current PadAI task

Use: Mark a task completed. Uses `PADAI_TASK_ID` if set, or accepts an argument.

```bash
export PADAI_MASTER="${PADAI_MASTER:-http://localhost:8000}"

TASK_ID="${1:-${PADAI_TASK_ID:-}}"
if [[ -z "$TASK_ID" ]]; then
  echo "Usage: /padai-complete <task_id> (or set PADAI_TASK_ID)" >&2
  exit 1
fi

curl -s -X POST "$PADAI_MASTER/api/complete" \
  -H "Content-Type: application/json" \
  -d "{\"task_id\": \"$TASK_ID\"}" | jq

echo "✅ Completed: $TASK_ID"
```

