"""
PadAI Master Server - Phase 1 MVP
FastAPI server for multi-agent Beads coordination.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import subprocess
import shutil
import time
import logging
from dotenv import load_dotenv

from .beads import (
    get_status,
    get_ready_tasks,
    get_all_tasks,
    claim_task,
    complete_task,
    create_task,
    update_task,
    add_dependency,
    BeadsError
)

app = FastAPI(title="PadAI Master Server", version="0.1.0")

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment from .env.local then .env (if present)
load_dotenv(dotenv_path=".env.local", override=False)
load_dotenv(override=False)


def _resolve_workspace() -> str:
    ws = os.getenv("WORKSPACE_PATH")
    if ws and os.path.isdir(ws):
        return ws
    # Default to the current working directory
    return os.getcwd()


# Workspace path (should contain .beads/ folder) and logging level
WORKSPACE = _resolve_workspace()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Logger
logger = logging.getLogger("padai")
if not logger.handlers:
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))


@app.middleware("http")
async def request_logger(request: Request, call_next):
    start = time.time()
    client = request.client.host if request.client else "-"
    logger.info(f"→ {request.method} {request.url.path} from {client}")
    try:
        response = await call_next(request)
        dur_ms = (time.time() - start) * 1000
        logger.info(f"← {request.method} {request.url.path} {response.status_code} {dur_ms:.1f}ms")
        return response
    except Exception:
        dur_ms = (time.time() - start) * 1000
        logger.exception(f"✖ {request.method} {request.url.path} failed after {dur_ms:.1f}ms")
        raise


@app.on_event("startup")
async def on_startup():
    logger.info("PadAI Master Server starting up")
    # Log config values
    bd_path = shutil.which("bd")
    beads_path = os.path.join(WORKSPACE, ".beads", "issues.jsonl")
    logger.info("Config:")
    logger.info(f"  WORKSPACE_PATH={WORKSPACE}")
    logger.info(f"  LOG_LEVEL={LOG_LEVEL}")
    logger.info(f"  BD_PATH={bd_path or 'NOT FOUND'}")
    try:
        ver = subprocess.run(["bd", "--version"], capture_output=True, text=True)
        ver_txt = (ver.stdout or ver.stderr or "").strip()
        if ver.returncode == 0 and ver_txt:
            logger.info(f"  BD_VERSION={ver_txt}")
        else:
            logger.warning(f"  BD_VERSION=unknown (rc={ver.returncode})")
    except Exception as e:
        logger.warning(f"  BD_VERSION unavailable: {e}")
    logger.info(f"  BEADS_JSONL={'present' if os.path.exists(beads_path) else 'missing'} @ {beads_path}")
    logger.info("Routes: /, /api/status, /api/ready, /api/tasks, /api/claim, /api/complete, /api/create, /api/update")


# Request/Response models
class ClaimRequest(BaseModel):
    agent_name: str


class CompleteRequest(BaseModel):
    task_id: str


class StatusResponse(BaseModel):
    total: int
    ready: int
    in_progress: int
    completed: int




# Endpoints

@app.get("/health")
@app.get("/api/health")
async def health():
    """Health check endpoint."""
    logger.debug("Health check")
    return {"status": "ok", "service": "PadAI Master Server"}


@app.get("/api/status", response_model=StatusResponse)
async def api_status():
    """
    Get current project status with task counts.

    Example response:
    {
        "total": 18,
        "ready": 5,
        "in_progress": 2,
        "completed": 11
    }
    """
    try:
        status = get_status(WORKSPACE)
        logger.info(f"/api/status -> {status}")
        return StatusResponse(**status)
    except BeadsError as e:
        logger.exception("/api/status failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/ready")
async def api_ready():
    """
    Get list of tasks ready to be claimed.

    Example response:
    [
        {"id": "padai-4", "title": "GET /api/status endpoint", "status": "ready"}
    ]
    """
    try:
        tasks = get_ready_tasks(WORKSPACE)
        logger.debug(f"Ready tasks: {len(tasks)}")
        return {"tasks": tasks}
    except BeadsError as e:
        logger.exception("/api/ready failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tasks")
async def api_tasks():
    """
    Get all tasks with full details including dependencies.

    Used by React Flow visualization to build dependency graph.

    Example response:
    {
        "tasks": [
            {
                "id": "padai-1",
                "title": "Design PadAI architecture",
                "status": "completed",
                "dependencies": [...]
            }
        ]
    }
    """
    try:
        tasks = get_all_tasks(WORKSPACE)
        logger.info(f"/api/tasks -> count={len(tasks)}")
        if tasks:
            t = tasks[0]
            logger.debug(f"first: id={t.get('id')} title={t.get('title')} status={t.get('status')}")
        return {"tasks": tasks}
    except BeadsError as e:
        logger.exception("/api/tasks failed")
        raise HTTPException(status_code=500, detail=str(e))




@app.post("/api/claim")
async def api_claim(request: ClaimRequest):
    """
    Claim the next available task for an agent.

    Request body:
    {
        "agent_name": "agent-1"
    }

    Response:
    {
        "task": {
            "id": "padai-4",
            "title": "GET /api/status endpoint",
            "status": "in_progress",
            "assignee": "agent-1"
        }
    }

    Returns 404 if no tasks are ready.
    """
    try:
        logger.info(f"Claim requested by '{request.agent_name}'")
        task = claim_task(request.agent_name, WORKSPACE)

        if task is None:
            logger.info("No ready tasks to claim")
            raise HTTPException(status_code=404, detail="No tasks available")

        logger.info(f"Task claimed: {task.get('id')} - {task.get('title')}")
        return {"task": task}

    except BeadsError as e:
        logger.exception("/api/claim failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/complete")
async def api_complete(request: CompleteRequest):
    """
    Mark a task as completed.

    Request body:
    {
        "task_id": "padai-4"
    }

    Response:
    {
        "success": true,
        "task_id": "padai-4"
    }
    """
    try:
        logger.info(f"Complete requested for task_id={request.task_id}")
        success = complete_task(request.task_id, WORKSPACE)

        if not success:
            raise HTTPException(status_code=500, detail="Failed to complete task")

        logger.info(f"Task completed: {request.task_id}")
        return {"success": True, "task_id": request.task_id}

    except BeadsError as e:
        logger.exception("/api/complete failed")
        raise HTTPException(status_code=500, detail=str(e))


class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    issue_type: Optional[str] = "task"  # bug|feature|task|epic|chore
    priority: Optional[int] = 2          # 0-4 (0 highest)
    deps: Optional[List[str]] = None     # ["blocks:padai-3", "padai-2"]
    labels: Optional[List[str]] = None
    assignee: Optional[str] = None
    id: Optional[str] = None             # explicit id


@app.post("/api/create")
async def api_create(request: CreateTaskRequest):
    """
    Create a new task in the Beads workspace using bd CLI.

    Request body:
    {
        "title": "Platformer MVP: Scaffold",
        "description": "Single HTML file with canvas and basic movement",
        "issue_type": "task",
        "priority": 2,
        "deps": ["padai-3", "blocks:padai-2"],
        "labels": ["game", "platformer"],
        "assignee": "littleboy",
        "id": "padai-42"
    }

    Response:
    {
        "task": { ...created issue object... }
    }
    """
    try:
        logger.info(f"Create task: '{request.title}' assignee={request.assignee}")
        created = create_task(
            title=request.title,
            description=request.description or "",
            issue_type=request.issue_type or "task",
            priority=request.priority if request.priority is not None else 2,
            deps=request.deps,
            labels=request.labels,
            assignee=request.assignee,
            explicit_id=request.id,
            cwd=WORKSPACE,
        )
        logger.info(f"Task created: {created.get('id')} - {created.get('title')}")
        return {"task": created}
    except BeadsError as e:
        logger.exception("/api/create failed")
        raise HTTPException(status_code=500, detail=str(e))


class UpdateTaskRequest(BaseModel):
    task_id: str
    status: Optional[str] = None
    assignee: Optional[str] = None
    title: Optional[str] = None
    priority: Optional[int] = None
    notes: Optional[str] = None
    design: Optional[str] = None
    external_ref: Optional[str] = None
    acceptance_criteria: Optional[str] = None


@app.post("/api/update")
async def api_update(request: UpdateTaskRequest):
    """
    Update fields of an existing task via bd update.

    Only provided fields will be updated.

    Request body:
    {
      "task_id": "padai-42",
      "status": "in_progress",
      "assignee": "littleboy",
      "title": "New title",
      "priority": 1,
      "notes": "some notes"
    }
    """
    try:
        if not any([
            request.status is not None,
            request.assignee is not None,
            request.title is not None,
            request.priority is not None,
            request.notes is not None,
            request.design is not None,
            request.external_ref is not None,
            request.acceptance_criteria is not None,
        ]):
            raise HTTPException(status_code=400, detail="No fields provided to update")

        logger.info(
            f"Update task {request.task_id}: "
            f"status={request.status} assignee={request.assignee} title={request.title} priority={request.priority}"
        )
        ok = update_task(
            task_id=request.task_id,
            status=request.status,
            assignee=request.assignee,
            title=request.title,
            priority=request.priority,
            notes=request.notes,
            design=request.design,
            external_ref=request.external_ref,
            acceptance_criteria=request.acceptance_criteria,
            cwd=WORKSPACE,
        )

        if not ok:
            raise HTTPException(status_code=500, detail="Failed to update task")

        # Return updated task snapshot if available
        tasks = get_all_tasks(WORKSPACE)
        updated = next((t for t in tasks if t.get('id') == request.task_id), None)
        logger.info(f"Task updated: {request.task_id}")
        return {"success": True, "task": updated or {"id": request.task_id}}

    except BeadsError as e:
        logger.exception("/api/update failed")
        raise HTTPException(status_code=500, detail=str(e))


class DepAddRequest(BaseModel):
    issue_id: str
    depends_on_id: str
    type: Optional[str] = "blocks"


@app.post("/api/deps/add")
async def api_dep_add(request: DepAddRequest):
    """
    Add a dependency: issue_id depends on depends_on_id, with optional type (default: blocks).
    """
    try:
        ok = add_dependency(request.issue_id, request.depends_on_id, request.type or "blocks", WORKSPACE)
        if not ok:
            raise HTTPException(status_code=500, detail="Failed to add dependency")
        # Return updated snapshot for convenience
        tasks = get_all_tasks(WORKSPACE)
        updated = next((t for t in tasks if t.get('id') == request.issue_id), None)
        return {"success": True, "task": updated or {"id": request.issue_id}}
    except BeadsError as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve React frontend (if built)
if os.path.exists("frontend/dist"):
    app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
