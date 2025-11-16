# MedhAI Architectural Feedback - November 16, 2025

## Current State Assessment

**What you built:** Clean MVP with ~1700 LOC. FastAPI backend wrapping `bd` CLI, React Flow visualization, HTTP REST coordination, polling-based updates. Single source of truth in `.beads/issues.jsonl`.

**What works really well:**
- Clean separation of concerns (beads.py abstraction layer makes everything swappable)
- Visual feedback via React Flow with dependency graph, node types, status coloring
- Simple HTTP API that any agent can consume with curl
- Treating bd as SSoT instead of reinventing task tracking

**Current bottlenecks:**
- Subprocess spawning on every API call (50ms overhead, acceptable for <10 agents)
- Potential race conditions in concurrent claims (depends on bd's internal locking)
- 5-second polling delay (acceptable for visualization, not for reactive agents)
- Zero agent-to-agent communication or collaboration primitives
- No visibility into live agents (who's alive, what they're doing, are they stuck?)

## Question 1: What does the server do if we move to MCP?

**Critical insight: Your server becomes MORE important, not less.**

The beads-mcp is just efficient task storage primitives. It gives you:
- Persistent daemon per project (no subprocess spawning)
- Better concurrency via async RPC + locking
- Connection pooling and ContextVar isolation
- Multi-project routing (one MCP server, many beads projects)

**But it's still just CRUD for tasks.** It doesn't understand:
- Which agents are alive and what they're capable of
- Coordination policies (fairness, priority, load balancing)
- Inter-agent communication (events, mailboxes, broadcasts)
- Multi-agent orchestration (decomposition, handoffs, collaboration)
- Real-time subscriptions (WebSocket for live updates)
- Observability (metrics, agent status, performance tracking)

### Server Architecture with MCP

```
┌──────────────────────────────────────────────────────┐
│ PadAI Orchestration Server (FastAPI)                 │
│                                                       │
│  ┌─────────────────┐      ┌────────────────────┐    │
│  │ HTTP/WS API     │      │ MCP Server         │    │
│  │ /claim          │      │ (optional remote)  │    │
│  │ /heartbeat      │      └────────────────────┘    │
│  │ /events/sub     │              │                  │
│  │ /agents/list    │              ▼                  │
│  └─────────────────┘      ┌────────────────────┐    │
│          │                │ Coordination Logic │    │
│          ▼                │ - Agent registry   │    │
│  ┌─────────────────┐      │ - Event router     │    │
│  │ WebSocket Hub   │      │ - Claim policies   │    │
│  │ (live updates)  │◄─────│ - Heartbeat mon.   │    │
│  └─────────────────┘      │ - Collaboration    │    │
│                           └────────────────────┘    │
│                                   │                  │
└───────────────────────────────────┼──────────────────┘
                                    ▼
                    ┌───────────────────────────────┐
                    │ beads-mcp (storage layer)     │
                    │ - Task CRUD via daemon RPC    │
                    │ - Dependency management       │
                    │ - Status tracking             │
                    └───────────────────────────────┘
```

**What your server owns:**
1. **Agent Registry** - Track which agents are alive, last heartbeat, current task, capabilities
2. **Event System** - Pub/sub for agent communication, task updates, coordination signals
3. **WebSocket Connections** - Real-time push to agents and frontend
4. **Claim Coordinator** - Policies for who gets what task (fairness, priority, capabilities)
5. **Collaboration Orchestrator** - Multi-agent workflows, handoffs, decomposition
6. **Observability** - Metrics, logs, trace task→agent→completion flows

**beads-mcp handles:**
- Fast task CRUD without subprocess overhead
- Persistent daemon with connection pooling
- Dependency graph storage
- Atomic updates with proper locking

## Question 2: How are agents made proactive?

**Current model:** Agents poll `/api/ready`, claim a task, work in isolation. Reactive.

**Proactive model:** Agents watch, analyze, suggest, collaborate, self-organize.

### Proactive Behaviors to Enable

**1. Event-Driven Work Claiming**
```
Agent subscribes: "notify me when tasks tagged 'frontend' become ready"
Task becomes unblocked → Server pushes event → Agent claims instantly
```

**2. Opportunistic Decomposition**
```
Agent claims task-123 (big feature)
Agent analyzes scope, creates subtasks task-124, task-125, task-126
Agent claims task-124, leaves others for the swarm
Other agents see new ready tasks, claim them
Parallel execution of decomposed work
```

**3. Stuck Detection & Help Requests**
```
Agent working on task-42 for 20 minutes, no progress
Agent posts event: "Stuck on task-42, need help with API design"
Other agents see event, one responds with suggestions
Or: Agent creates task-43 "Review API design for task-42", assigns to peer
```

**4. Proactive Monitoring**
```
Agent subscribes to all task status changes
Agent builds mental model of project progress
Agent analyzes critical path, suggests priority changes
Agent creates tasks proactively: "We should add tests for X"
```

**5. Self-Assignment Based on Capabilities**
```
Agent metadata: {"skills": ["frontend", "react", "typescript"]}
Task created with labels: ["frontend", "react"]
Server broadcasts: "New frontend task available"
Agents with matching skills get priority notification
Best-fit agent claims it
```

### Primitives Needed for Proactivity

**WebSocket subscriptions:**
```python
# Agent subscribes
ws.send({"type": "subscribe", "filter": {"labels": ["frontend"], "status": "ready"}})

# Server pushes when matching task changes
ws.receive({"type": "task_ready", "task": {"id": "task-42", ...}})
```

**Event/message system:**
```python
# Agent posts
POST /api/events/publish {"type": "help_request", "task": "task-42", "message": "..."}

# Other agents poll or subscribe
GET /api/events/poll?since=timestamp
WS: {"type": "event", "event": {...}}
```

**Agent capabilities registry:**
```python
# Agent registers on startup
POST /api/agents/register {
  "agent_id": "agent-A",
  "capabilities": ["frontend", "python", "debugging"],
  "max_concurrent_tasks": 2
}

# Agent heartbeat includes current state
POST /api/agents/heartbeat {
  "agent_id": "agent-A",
  "current_tasks": ["task-42"],
  "status": "working"
}
```

**Task analysis tools:**
```python
# Agent queries for insights
GET /api/tasks/critical_path
GET /api/tasks/blocked_tree?task=task-42
GET /api/tasks/ready?labels=frontend&priority_gte=2
```

## Question 3: Should we package padai-mcp?

**Yes, but think of it as a coordination layer, not just a transport.**

### What padai-mcp should be

An MCP server that wraps beads-mcp and adds orchestration primitives.

**Tools it exposes:**
```typescript
// From beads-mcp (pass-through)
beads_create, beads_update, beads_list, beads_dep, beads_stats

// PadAI coordination layer (NEW)
padai_claim           // Claim next task with fairness/priority logic
padai_heartbeat       // Register agent liveness and current state
padai_subscribe       // Subscribe to task/event updates (returns subscription ID)
padai_poll_events     // Poll for events since last timestamp
padai_publish_event   // Publish message/event to other agents
padai_list_agents     // See which agents are alive and what they're doing
padai_decompose       // Helper to create child tasks for a parent
padai_handoff         // Explicitly hand off task to another agent
padai_collaborate     // Join a task as collaborator (multi-agent)
```

**Why package it:**
- Agents get both storage (beads) and coordination (padai) in one MCP connection
- MCP native agents speak the protocol directly (no HTTP wrapper needed)
- Can still expose HTTP/WebSocket for non-MCP agents
- Clean separation: beads-mcp = storage, padai-mcp = orchestration

**Architecture:**
```
┌─────────────────────────────────────────────────┐
│ padai-mcp (MCP Server)                          │
│                                                 │
│  Implements MCP tools:                          │
│  - padai_claim → coordination logic → beads_*   │
│  - padai_subscribe → event system → WS          │
│  - padai_heartbeat → agent registry → memory   │
│  - beads_* → pass-through to beads-mcp          │
│                                                 │
│  Internal:                                      │
│  - Agent registry (in-memory or Redis)          │
│  - Event queue (in-memory or Redis/SQLite)      │
│  - WebSocket hub for subscriptions              │
│  - Coordination policies (pluggable)            │
└─────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│ beads-mcp (daemon per project)                  │
│ - Task storage and retrieval                    │
│ - Dependency graph                              │
│ - SQLite backend                                │
└─────────────────────────────────────────────────┘
```

**Migration path:**
1. Keep current HTTP API server
2. Build padai-mcp alongside it, both calling beads-mcp
3. HTTP API becomes thin wrapper around padai-mcp tools
4. Agents can choose: HTTP (simple, curl-friendly) or MCP (native, typed, efficient)
5. Frontend uses WebSocket endpoint from padai-mcp for real-time updates

## Question 4: How can 2 agents collaborate?

This is the most interesting question. Current model is "1 task = 1 agent". Let's design multi-agent collaboration patterns.

### Pattern 1: Sequential Handoff (Pipeline)

**Use case:** Designer → Implementer → Reviewer

```
1. Agent-Designer claims task-100 "Build auth system"
2. Agent-Designer creates design doc, adds to task notes
3. Agent-Designer updates task: status=designed, adds label "ready_for_impl"
4. Agent-Designer calls padai_handoff(task=100, phase="implementation", preferred_agent="agent-coder")
5. Server broadcasts: "task-100 ready for implementation"
6. Agent-Coder claims task-100
7. Agent-Coder implements, marks status=implemented, label "ready_for_review"
8. Agent-Reviewer claims task-100
9. Agent-Reviewer approves or requests changes via event
10. Task marked completed
```

**Primitives needed:**
- Task phases/stages (designed, implemented, reviewed)
- Handoff API to signal phase completion
- Agent role metadata (designer, implementer, reviewer)
- Event stream per task for communication

### Pattern 2: Decomposition & Parallel Work

**Use case:** One agent breaks down epic, swarm executes

```
1. Agent-Architect claims task-200 "E-commerce checkout"
2. Agent-Architect analyzes scope:
   - task-201: Shopping cart UI
   - task-202: Payment integration
   - task-203: Order confirmation email
   - task-204: Integration tests
3. Agent-Architect creates these as subtasks:
   POST /api/create {parent: task-200, ...}
   POST /api/deps/add {issue: task-200, depends_on: task-201, type: "parent"}
4. Agent-Architect claims task-201 (most critical path)
5. Other agents claim task-202, task-203 in parallel
6. All work concurrently
7. Agent-Integrator waits for 201-203 to complete, then claims 204
8. Task-200 auto-completes when all children complete
```

**Primitives needed:**
- Parent/child task relationships
- Bulk task creation with dependencies
- Auto-completion when all children done
- Critical path analysis to prioritize

### Pattern 3: Pair Programming (Real-time Collaboration)

**Use case:** Two agents actively working on same task

```
1. Agent-A claims task-300 "Fix race condition bug"
2. Agent-A calls padai_collaborate(task=300, invite="agent-B", role="debugger")
3. Server assigns both agents to task-300
4. Agent-A focuses on code changes
5. Agent-B runs tests, analyzes traces
6. Both agents post to task event stream:
   Agent-A: "I think the issue is in mutex.lock() call"
   Agent-B: "Confirmed, test fails 30% of the time on that line"
   Agent-A: "Trying fix with double-checked locking"
   Agent-B: "Running 100 iterations... Success! 0 failures"
7. Agent-A commits fix
8. Both agents call padai_complete(task=300)
9. Task marked completed
```

**Primitives needed:**
- Multi-agent assignment (assignees: [agent-A, agent-B])
- Task-scoped event stream/chat
- Role assignment (coder, debugger, reviewer)
- Shared workspace or file locking for concurrent edits
- Completion requires all assigned agents to approve

### Pattern 4: Swarm Intelligence

**Use case:** Many agents self-organize around an epic

```
1. Epic task-400 "Migrate to TypeScript" created with 50 subtasks
2. All agents subscribe to task-400 events
3. Agents claim ready subtasks based on their capabilities
4. When agent completes a subtask, it unblocks others
5. Agents broadcast discoveries:
   "Found pattern: all API handlers need similar conversion"
6. One agent creates template, others reuse it
7. Agents help each other when stuck via event stream
8. Progress visible in real-time on frontend graph
9. Epic auto-completes when all subtasks done
```

**Primitives needed:**
- Epic/parent task subscriptions (notify on any child change)
- Shared knowledge base (templates, patterns discovered)
- Load balancing (agents claim based on current workload)
- Stuck detection (agent working >30min without progress)
- Helper matching (stuck agent gets routed to expert)

### Implementation: Multi-Agent Task Schema

```json
{
  "id": "task-100",
  "status": "in_progress",
  "phase": "implementation",  // NEW: designed, implementing, reviewing, testing
  "assignees": ["agent-A", "agent-B"],  // NEW: array instead of single
  "roles": {  // NEW: who's doing what
    "agent-A": "implementer",
    "agent-B": "reviewer"
  },
  "collaboration_mode": "sequential",  // sequential, parallel, pair, swarm
  "event_stream": "task-100-events",  // NEW: scoped message channel
  "parent": "task-50",  // NEW: parent task for decomposition
  "children": ["task-101", "task-102"],  // NEW: subtasks
  "handoff_log": [  // NEW: audit trail
    {"from": null, "to": "agent-A", "phase": "design", "timestamp": "..."},
    {"from": "agent-A", "to": "agent-B", "phase": "implementation", "timestamp": "..."}
  ]
}
```

### Implementation: Event Stream

Simple JSONL append-only log per task:

```
.beads/events/task-100.jsonl:

{"type":"claimed","agent":"agent-A","timestamp":"..."}
{"type":"message","agent":"agent-A","text":"Starting design phase","timestamp":"..."}
{"type":"handoff","from":"agent-A","to":"agent-B","phase":"implementation","timestamp":"..."}
{"type":"message","agent":"agent-B","text":"Implementation 50% complete","timestamp":"..."}
{"type":"stuck","agent":"agent-B","reason":"Unclear API contract","timestamp":"..."}
{"type":"message","agent":"agent-A","text":"Added API spec to task notes","timestamp":"..."}
{"type":"completed","agent":"agent-B","timestamp":"..."}
```

Agents can:
```python
# Publish
POST /api/tasks/task-100/events {"type": "message", "text": "..."}

# Subscribe via WebSocket
ws.send({"type": "subscribe_task", "task": "task-100"})
ws.receive({"type": "task_event", "task": "task-100", "event": {...}})

# Poll
GET /api/tasks/task-100/events?since=timestamp
```

### API Design for Collaboration

```python
# Invite collaborator
POST /api/tasks/{task_id}/collaborate
{
  "agent_id": "agent-B",
  "role": "reviewer",  // optional
  "mode": "pair"  // sequential, parallel, pair
}

# Handoff to next phase
POST /api/tasks/{task_id}/handoff
{
  "phase": "implementation",
  "preferred_agent": "agent-coder",  // optional
  "notes": "Design complete, see attached spec"
}

# Decompose into subtasks
POST /api/tasks/{task_id}/decompose
{
  "subtasks": [
    {"title": "Shopping cart UI", "assignee": "agent-A"},
    {"title": "Payment integration", "labels": ["backend"]},
    {"title": "Integration tests"}
  ],
  "mode": "parallel"  // all unblocked, vs "sequential" (waterfall)
}

# Report stuck, request help
POST /api/tasks/{task_id}/stuck
{
  "agent_id": "agent-A",
  "reason": "Unclear how to handle edge case X",
  "request_help_from": ["agent-expert"]  // optional
}

# Complete as team
POST /api/tasks/{task_id}/complete
{
  "agent_id": "agent-A",
  "approval": true
}
// Task only completes when all assignees approve
```

## Phased Implementation Plan

### Phase 1: Real-time Foundation (Do this first)
- [ ] Add WebSocket endpoint to FastAPI server
- [ ] Frontend subscribes to task updates via WS
- [ ] Backend pushes task changes to all connected clients
- [ ] Remove 5-second polling, use WS events
- **Learning:** Real-time systems, WebSocket lifecycle, event-driven UI

### Phase 2: Agent Observability
- [ ] Add POST /api/agents/heartbeat endpoint
- [ ] Track agent registry in memory (agent_id → last_seen, current_tasks, capabilities)
- [ ] Show live agents on frontend (sidebar or overlay)
- [ ] Detect and mark orphaned tasks (agent died mid-work)
- [ ] Add GET /api/agents/list for discovery
- **Learning:** Distributed system monitoring, failure detection, state reconciliation

### Phase 3: Event System
- [ ] Create .beads/events/{task_id}.jsonl for task-scoped messages
- [ ] POST /api/tasks/{task_id}/events to publish
- [ ] GET /api/tasks/{task_id}/events?since=ts to poll
- [ ] WS subscription to specific tasks
- [ ] Frontend shows event timeline for selected task
- **Learning:** Event sourcing, pub/sub patterns, append-only logs

### Phase 4: Multi-Agent Assignment
- [ ] Extend beads schema: assignees (array), roles (map)
- [ ] Update claim logic to support multiple assignees
- [ ] POST /api/tasks/{task_id}/collaborate endpoint
- [ ] Show multiple agent avatars on task nodes
- [ ] Completion requires all assignees to approve
- **Learning:** Consensus, multi-party coordination, conflict resolution

### Phase 5: Task Decomposition
- [ ] Add parent/children fields to task schema
- [ ] POST /api/tasks/{task_id}/decompose endpoint
- [ ] Auto-create dependencies (parent depends on all children)
- [ ] Frontend shows hierarchical view (expand/collapse subtasks)
- [ ] Auto-complete parent when all children done
- **Learning:** Hierarchical data, recursive aggregation, DAG traversal

### Phase 6: beads-mcp Integration
- [ ] Set up beads-mcp daemon
- [ ] Modify beads.py to use RPC instead of subprocess
- [ ] Benchmark: subprocess vs daemon performance
- [ ] Keep HTTP API unchanged (transparent swap)
- **Learning:** RPC protocols, performance profiling, migration strategies

### Phase 7: padai-mcp Server (if valuable)
- [ ] Build MCP server wrapping coordination logic
- [ ] Expose padai_* tools for native MCP agents
- [ ] HTTP API becomes thin wrapper around MCP tools
- [ ] Agents can choose HTTP or MCP transport
- **Learning:** Protocol design, multi-transport APIs, MCP ecosystem

### Phase 8: Advanced Collaboration
- [ ] Handoff workflows (phase transitions)
- [ ] Stuck detection and helper routing
- [ ] Shared workspace/file locking
- [ ] Critical path analysis and suggestions
- **Learning:** Workflow engines, graph algorithms, AI agent orchestration

## Key Architectural Principles

**1. Simple primitives, emergent complexity**
Don't build a workflow engine. Provide: tasks, events, subscriptions, multi-assignment. Let collaboration patterns emerge from agent behavior.

**2. Observability first**
Every coordination primitive should produce events. Make the system introspectable. Debugging distributed agents is hard - logs and traces are critical.

**3. Incremental migration**
Never break existing agents. Add new capabilities alongside old ones. HTTP + MCP coexist. Polling + WebSocket coexist. Deprecate only when usage drops to zero.

**4. Optimize for learning**
This is a side project. Prioritize learning value over "best practices". Build WebSockets before microservices. Build event sourcing before Kafka. Understand the primitives before adopting complex tools.

**5. Visualization drives understanding**
Every new capability should be visible in the React Flow graph. Live agents, event streams, collaboration mode, critical path - make it visual.

## Recommended Next Steps

**Week 1: WebSockets + Live Updates**
Replace polling with WebSocket push. Frontend gets instant updates. Agents can subscribe to task changes. This is high-value, low-complexity, and teaches real-time systems.

**Week 2: Agent Heartbeats + Registry**
Agents POST heartbeat every 30s. Server tracks live agents, shows them on UI. Detect stuck/dead agents. This makes the system observable.

**Week 3: Task Event Streams**
Simple JSONL log per task. Agents can post messages. Frontend shows timeline. This enables coordination beyond just status updates.

**Week 4: Multi-Agent Assignment**
Support multiple assignees per task. Build the collaboration primitive. Test with two agents pair-programming on a task.

**Then decide:** Do you care more about performance (→ beads-mcp) or richer coordination (→ decomposition, handoffs)? Follow your curiosity.

## References

- **beads-mcp daemon model:** Per-project isolation, connection pooling, async RPC
- **MCP code execution pattern:** Progressive disclosure, local filtering, privacy preservation (not directly applicable but interesting for future analytics tools)
- **Current PadAI:** Clean MVP with good separation of concerns, ready for incremental evolution

---

## Personal Take

You've built something genuinely interesting. Most multi-agent frameworks abstract away the coordination primitives - you're building them from scratch, which means you'll actually understand how agents coordinate.

The move to MCP isn't about performance (you don't have bottlenecks yet). It's about:**standardization**. If agents speak MCP natively, they get typed tools, better error handling, and ecosystem compatibility. But don't rush it - HTTP works fine for learning.

The real value is in the collaboration primitives. How DO you make two agents work together? There's no playbook for this yet. You get to discover the patterns. That's rare and valuable.

Start with WebSockets and agent heartbeats. Make the system observable. Once you can SEE agents coordinating in real-time, you'll know what to build next. The architecture will emerge from usage, not from planning.
