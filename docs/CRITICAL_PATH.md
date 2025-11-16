# Critical Path Analysis for PadAI

This document outlines how to compute and visualize the critical path (CP) of a task graph managed by PadAI.

## What is the Critical Path?
- The longest chain of dependent tasks (by total weight) that determines the earliest completion time.
- Tasks on the critical path have zero slack: any delay on them delays overall delivery.

## Why Show It?
- Focus team effort where it matters most
- Identify bottlenecks and remove blockers quickly
- Coordinate parallel work by de‑emphasizing non‑critical tasks

## Inputs and Assumptions
- Graph: Directed Acyclic Graph (DAG) with edges `depends_on -> dependent`
- Weight per node (configurable):
  - `estimate_point` or `point` if available
  - fallback to `1` (unweighted)
- Scope:
  - Default excludes `completed` tasks (only future work)
  - Optional toggle to include them for historical analysis

## Algorithm (Longest Path in DAG)
1. Topological sort of the DAG.
2. Dynamic programming:
   - `dist[u] = w[u] + max(dist[pred])` for all predecessors `pred` of `u`.
   - Track `pred[u]` for path reconstruction.
3. The CP ends at sink node `t` maximizing `dist[t]`.
4. Reconstruct path by following `pred` back to a source.

Complexity: O(V + E).

## Slack (Optional)
- Compute `distFromStart[u]` and `distToEnd[u]` (reverse DAG for latter)
- `slack[u] = CPLength - distFromStart[u] - distToEnd[u]`
- Nodes with `slack == 0` are critical

## API Proposal (Phase 1)
`GET /api/analysis/critical-path`

Query params:
- `weight=estimate|points|uniform` (default: `uniform`)
- `include_completed=true|false` (default: false)

Response:
```
{
  "path": ["game-1", "game-2", "game-3"],
  "total_weight": 7,
  "weight_mode": "uniform",
  "notes": "Unweighted critical path (1 per node)."
}
```

## UI Proposal
- Toggle in header: “Critical Path”
- When on:
  - highlight nodes/edges on CP (e.g., amber)
  - optional: dim non‑CP nodes
- Tooltip/badge: show `slack` if computed

## Edge Cases
- Cycles: detect; return 400 with an error message (invalid project state)
- Disconnected subgraphs: compute CP per component; show the one with max total (or let user switch)
- Missing estimates: fallback to uniform weights, clearly label as unweighted

## Implementation Plan (Phase 1)
- Server: compute uniform CP (no estimates), return path ids via `/api/analysis/critical-path`
- Client: add toggle + highlight styling (reusing the existing highlight system)
- Phase 2: add estimate-based weighting and slack

