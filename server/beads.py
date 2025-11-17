"""
Wrapper for bd CLI commands using bd CLI (DB as single source of truth).
"""
import subprocess
import logging
import json
import os
import time
from typing import Dict, List, Optional, Any


class BeadsError(Exception):
    """Exception raised when bd command fails."""
    pass


def execute_bd(args: List[str], cwd: str = "/workspace") -> str:
    """
    Execute bd command with --no-db flag.

    Args:
        args: Command arguments to pass to bd
        cwd: Working directory (should contain .beads/ folder)

    Returns:
        stdout from the command

    Raises:
        BeadsError: If command fails or times out
    """
    logger = logging.getLogger("padai.beads")

    # Use bd defaults (auto-discover DB). Some versions don't support --no-db.
    # Build command ensuring global flags precede subcommand
    db_path = os.getenv("BEADS_DB_PATH")
    preflags: List[str] = []
    # Pull out '--json' from args to set as global flag
    args_no_json: List[str] = []
    want_json = False
    for a in args:
        if a == "--json":
            want_json = True
        else:
            args_no_json.append(a)
    if want_json:
        preflags.append("--json")
    if db_path:
        preflags += ["--db", db_path]
    # Speed/stability flags; can be disabled via env if needed
    no_daemon = os.getenv("BD_NO_DAEMON", "1") != "0"
    no_auto_import = os.getenv("BD_NO_AUTO_IMPORT", "1") != "0"
    if no_daemon:
        preflags.append("--no-daemon")
    if no_auto_import:
        preflags.append("--no-auto-import")

    cmd = ["bd", *preflags, *args_no_json]
    timeout_secs = int(os.getenv("BD_TIMEOUT_SECS", "30"))

    logger.info(f"⏱️  BD EXEC START: {' '.join(args_no_json)} | daemon={not no_daemon} auto_import={not no_auto_import} timeout={timeout_secs}s")
    start_time = time.time()

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout_secs
        )

        elapsed = time.time() - start_time

        if result.returncode != 0:
            logger.error(f"❌ BD FAILED in {elapsed:.2f}s ({result.returncode}): {result.stderr.strip()}")
            raise BeadsError(f"bd command failed: {result.stderr}")

        out = result.stdout.strip()
        out_preview = out[:200] + ('...' if len(out) > 200 else '')
        logger.info(f"✅ BD SUCCESS in {elapsed:.2f}s: {' '.join(args_no_json)} | output_size={len(out)} bytes")
        logger.debug(f"BD OUTPUT: {out_preview}")
        return out

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        logger.error(f"⏱️  BD TIMEOUT after {elapsed:.2f}s: {' '.join(args_no_json)}")
        raise BeadsError(f"bd command timed out after {timeout_secs}s")
    except FileNotFoundError:
        elapsed = time.time() - start_time
        logger.error(f"❌ BD NOT FOUND after {elapsed:.2f}s")
        raise BeadsError("bd CLI not found. Install from https://github.com/steveyegge/beads")
    except OSError as e:
        elapsed = time.time() - start_time
        logger.error(f"❌ BD OS ERROR after {elapsed:.2f}s: {e}")
        # Common when the downloaded binary is an HTML error page or wrong arch
        raise BeadsError(f"bd execution failed: {e}")


def add_dependency(issue_id: str, depends_on_id: str, dep_type: str = "blocks", cwd: str = "/workspace") -> bool:
    """
    Add a dependency relation using `bd dep add`.

    Args:
        issue_id: The issue that has the dependency
        depends_on_id: The issue it depends on
        dep_type: Dependency type (blocks|related|parent|discovered-from)
        cwd: Workspace dir

    Returns:
        True if the operation succeeded, False otherwise
    """
    try:
        execute_bd(["dep", "add", issue_id, depends_on_id, "--type", dep_type], cwd)
        return True
    except BeadsError:
        return False


def create_task(
    title: str,
    description: str = "",
    issue_type: str = "task",
    priority: int = 2,
    deps: Optional[List[str]] = None,
    labels: Optional[List[str]] = None,
    assignee: Optional[str] = None,
    explicit_id: Optional[str] = None,
    cwd: str = "/workspace",
) -> Dict[str, Any]:
    """
    Create a new task using bd CLI and return the created task object.

    Args:
        title: Issue title
        description: Description text
        issue_type: One of bug|feature|task|epic|chore
        priority: 0-4 (0 highest)
        deps: Optional list like ["blocks:padai-3", "padai-2"]
        labels: Optional list of label strings
        assignee: Optional assignee name
        explicit_id: Optional explicit ID (e.g., 'padai-42')
        cwd: Workspace directory containing .beads/

    Returns:
        Dict representing the created issue (parsed from bd --json output)
    """
    args: List[str] = ["--json", "create", title]
    if description:
        args += ["--description", description]
    if issue_type:
        args += ["--type", issue_type]
    if priority is not None:
        args += ["--priority", str(priority)]

    if assignee:
        args += ["--assignee", assignee]
    if deps:
        # bd expects comma-separated deps in format 'type:id' or 'id'
        args += ["--deps", ",".join(deps)]

    out = execute_bd(args, cwd)
    try:
        created = json.loads(out)
        if isinstance(created, dict):
            return created
        # Some versions may return a list with a single item
        if isinstance(created, list) and created:
            return created[0]
        raise BeadsError("Unexpected bd create output format")
    except json.JSONDecodeError as e:
        raise BeadsError(f"Failed to parse bd create output as JSON: {e}")


def get_status(cwd: str = "/workspace") -> Dict[str, Any]:
    """
    Get current Beads project status.

    Returns dict with:
    - total: total issues
    - ready: ready to work
    - in_progress: currently in progress
    - completed: done
    """
    logger = logging.getLogger("padai.beads")
    start_time = time.time()
    logger.info("📊 get_status() called")

    # Prefer bd stats; fall back to computing from bd export (DB-only)
    try:
        output = execute_bd(["stats"], cwd)

        status = {
            "total": 0,
            "ready": 0,
            "in_progress": 0,
            "completed": 0
        }

        for line in output.split('\n'):
            line = line.strip()
            if 'Total Issues:' in line:
                status['total'] = int(line.split(':')[1].strip())
            elif 'Ready to Work:' in line:
                status['ready'] = int(line.split(':')[1].strip())
            elif 'In Progress:' in line:
                status['in_progress'] = int(line.split(':')[1].strip())
            elif 'Closed:' in line or 'Completed:' in line:
                status['completed'] = int(line.split(':')[1].strip())

        elapsed = time.time() - start_time
        logger.info(f"✅ get_status() completed in {elapsed:.2f}s: {status}")
        return status
    except BeadsError as e:
        logger.error(f"⚠️  get_status() bd stats failed, falling back to bd export")
        # Fallback: compute counts via bd export
        tasks = get_all_tasks(cwd)
        total = len(tasks)
        completed = sum(1 for t in tasks if t.get('status') in ('completed','closed'))
        in_prog = sum(1 for t in tasks if t.get('status') == 'in_progress')

        by_id: Dict[str, Dict[str, Any]] = {t.get('id'): t for t in tasks if 'id' in t}

        def is_blocked(task: Dict[str, Any]) -> bool:
            deps = task.get('dependencies') or []
            for d in deps:
                dep_id = d.get('depends_on_id')
                if not dep_id:
                    continue
                dep = by_id.get(dep_id)
                if dep and dep.get('status') != 'completed':
                    return True
            return False

        ready = 0
        for t in tasks:
            status_t = t.get('status')
            if status_t in (None, 'open', 'ready') and not is_blocked(t):
                ready += 1

        result = {
            "total": total,
            "ready": ready,
            "in_progress": in_prog,
            "completed": completed,
        }
        elapsed = time.time() - start_time
        logger.info(f"✅ get_status() completed via fallback in {elapsed:.2f}s: {result}")
        return result


def get_ready_tasks(cwd: str = "/workspace") -> List[Dict[str, Any]]:
    """
    Get list of tasks that are ready to work on.

    Returns list of task dicts with id, title, status, etc.
    """
    logger = logging.getLogger("padai.beads")
    start_time = time.time()
    logger.info("🎯 get_ready_tasks() called")

    output = execute_bd(["ready"], cwd)

    tasks: List[Dict[str, Any]] = []
    for line in output.split('\n'):
        line = line.strip()
        # Skip empty lines and headers
        if not line or line.startswith('📋') or line.startswith('#'):
            continue

        # Parse format: "1. [P0] padai-10: Deploy to Railway"
        if '. [P' in line and ':' in line:
            try:
                parts = line.split(':', 1)
                if len(parts) >= 2:
                    id_part = parts[0].strip()
                    task_id = id_part.split()[-1]
                    title = parts[1].strip()
                    tasks.append({
                        "id": task_id,
                        "title": title,
                        "status": "ready"
                    })
            except Exception:
                continue

    elapsed = time.time() - start_time
    logger.info(f"✅ get_ready_tasks() completed in {elapsed:.2f}s | {len(tasks)} ready tasks")
    return tasks


def get_all_tasks(cwd: str = "/workspace") -> List[Dict[str, Any]]:
    """
    Get all tasks with full details including dependencies.

    Returns list of task dicts parsed from JSONL.
    """
    logger = logging.getLogger("padai.beads")
    start_time = time.time()
    logger.info("📋 get_all_tasks() called")

    # Export from DB as JSONL via bd export
    output = execute_bd(["export"], cwd)

    parse_start = time.time()
    tasks: List[Dict[str, Any]] = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            tasks.append(obj)
        except json.JSONDecodeError:
            continue

    parse_elapsed = time.time() - parse_start
    total_elapsed = time.time() - start_time
    logger.info(f"✅ get_all_tasks() completed in {total_elapsed:.2f}s (parse: {parse_elapsed:.2f}s) | {len(tasks)} tasks")
    return tasks


def update_task(
    task_id: str,
    status: Optional[str] = None,
    assignee: Optional[str] = None,
    title: Optional[str] = None,
    priority: Optional[int] = None,
    notes: Optional[str] = None,
    design: Optional[str] = None,
    external_ref: Optional[str] = None,
    acceptance_criteria: Optional[str] = None,
    cwd: str = "/workspace",
) -> bool:
    """
    Update a task's status or assignee.

    Args:
        task_id: Task ID to update
        status: New status (ready, in_progress, completed)
        assignee: Agent name to assign to

    Returns:
        True if successful
    """
    try:
        updated = False
        if status:
            execute_bd(["update", task_id, "--status", status], cwd)
            updated = True

        if assignee:
            execute_bd(["update", task_id, "--assignee", assignee], cwd)
            updated = True

        if title:
            execute_bd(["update", task_id, "--title", title], cwd)
            updated = True

        if priority is not None:
            execute_bd(["update", task_id, "--priority", str(priority)], cwd)
            updated = True

        if notes:
            execute_bd(["update", task_id, "--notes", notes], cwd)
            updated = True

        if design:
            execute_bd(["update", task_id, "--design", design], cwd)
            updated = True

        if external_ref:
            execute_bd(["update", task_id, "--external-ref", external_ref], cwd)
            updated = True

        if acceptance_criteria:
            execute_bd(["update", task_id, "--acceptance-criteria", acceptance_criteria], cwd)
            updated = True

        return updated

    except BeadsError:
        return False


def claim_task(agent_name: str, cwd: str = "/workspace") -> Optional[Dict[str, Any]]:
    """
    Claim the first available ready task for an agent.

    Args:
        agent_name: Name of the agent claiming the task

    Returns:
        Task dict if successful, None if no tasks available
    """
    ready = get_ready_tasks(cwd)

    if not ready:
        return None

    task = ready[0]

    # Update to in_progress and assign
    success = update_task(task['id'], status="in_progress", assignee=agent_name, cwd=cwd)

    if success:
        # Get full task details
        all_tasks = get_all_tasks(cwd)
        for t in all_tasks:
            if t.get('id') == task['id']:
                return t
        return task

    return None


def complete_task(task_id: str, cwd: str = "/workspace") -> bool:
    """
    Mark a task as completed.

    Args:
        task_id: Task ID to complete

    Returns:
        True if successful
    """
    # bd uses 'closed' for completed issues
    return update_task(task_id, status="closed", cwd=cwd)
