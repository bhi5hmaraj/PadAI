"""
Direct SQLite database access for Beads - bypasses bd CLI for speed.
"""
import sqlite3
import json
import logging
import os
from typing import Dict, List, Any, Optional
from contextlib import contextmanager


logger = logging.getLogger("padai.beads_db")


def find_beads_db(workspace: str) -> str:
    """Find the beads database file in the workspace."""
    beads_dir = os.path.join(workspace, ".beads")
    if not os.path.exists(beads_dir):
        raise FileNotFoundError(f"Beads directory not found at {beads_dir}")

    # Look for any .db file in the .beads directory
    db_files = [f for f in os.listdir(beads_dir) if f.endswith('.db')]

    if not db_files:
        raise FileNotFoundError(f"No database files found in {beads_dir}")

    if len(db_files) > 1:
        logger.warning(f"Multiple database files found in {beads_dir}: {db_files}, using first one")

    db_path = os.path.join(beads_dir, db_files[0])
    logger.debug(f"Found beads database at {db_path}")
    return db_path


@contextmanager
def get_db_connection(workspace: str = "/workspace"):
    """Get a connection to the beads database."""
    db_path = find_beads_db(workspace)
    logger.debug(f"Connecting to beads database at {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Return rows as dicts
    try:
        yield conn
    finally:
        conn.close()


def get_status_fast(workspace: str = "/workspace") -> Dict[str, int]:
    """
    Get project status by querying the database directly.

    Returns:
        Dict with total, ready, in_progress, completed counts
    """
    logger.info("📊 get_status_fast() - querying SQLite directly")

    with get_db_connection(workspace) as conn:
        cursor = conn.cursor()

        # Total issues
        cursor.execute("SELECT COUNT(*) as count FROM issues")
        total = cursor.fetchone()["count"]

        # Completed/closed
        cursor.execute(
            "SELECT COUNT(*) as count FROM issues WHERE status IN ('completed', 'closed')"
        )
        completed = cursor.fetchone()["count"]

        # In progress
        cursor.execute("SELECT COUNT(*) as count FROM issues WHERE status = 'in_progress'")
        in_progress = cursor.fetchone()["count"]

        # Ready (open/ready status and not blocked by dependencies)
        # Simplified: just count ready/open issues
        # TODO: Add dependency blocking logic
        cursor.execute(
            "SELECT COUNT(*) as count FROM issues "
            "WHERE status IN ('ready', 'open', 'todo') OR status IS NULL"
        )
        ready = cursor.fetchone()["count"]

    result = {
        "total": total,
        "ready": ready,
        "in_progress": in_progress,
        "completed": completed,
    }
    logger.info(f"✅ get_status_fast() completed: {result}")
    return result


def get_all_tasks_fast(workspace: str = "/workspace") -> List[Dict[str, Any]]:
    """
    Get all tasks by querying the database directly.

    Returns:
        List of task dicts with all fields
    """
    logger.info("📋 get_all_tasks_fast() - querying SQLite directly")

    with get_db_connection(workspace) as conn:
        cursor = conn.cursor()

        # Get all issues with their fields
        cursor.execute("""
            SELECT
                id, title, description, status, priority, assignee,
                issue_type, created_at, updated_at, closed_at,
                notes, design, external_ref, acceptance_criteria,
                approval, epic_id
            FROM issues
            ORDER BY priority ASC, created_at DESC
        """)

        rows = cursor.fetchall()
        tasks = []

        for row in rows:
            task = dict(row)

            # Get dependencies for this issue
            cursor.execute("""
                SELECT depends_on_id, type
                FROM dependencies
                WHERE issue_id = ?
            """, (task["id"],))

            deps = cursor.fetchall()
            task["dependencies"] = [dict(d) for d in deps]

            tasks.append(task)

    logger.info(f"✅ get_all_tasks_fast() completed: {len(tasks)} tasks")
    return tasks


def get_ready_tasks_fast(workspace: str = "/workspace") -> List[Dict[str, Any]]:
    """
    Get ready tasks by querying the database directly.

    Returns:
        List of ready task dicts
    """
    logger.info("🎯 get_ready_tasks_fast() - querying SQLite directly")

    with get_db_connection(workspace) as conn:
        cursor = conn.cursor()

        # Get tasks that are ready (not blocked)
        # Simplified: just get ready/open status tasks
        # TODO: Add proper dependency blocking check
        cursor.execute("""
            SELECT id, title, status, priority
            FROM issues
            WHERE status IN ('ready', 'open', 'todo') OR status IS NULL
            ORDER BY priority ASC
        """)

        rows = cursor.fetchall()
        tasks = [dict(row) for row in rows]

    logger.info(f"✅ get_ready_tasks_fast() completed: {len(tasks)} ready tasks")
    return tasks
