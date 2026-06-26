# ============================================================
#  Zarix AgentOS — Celery Background Tasks
# ============================================================
#  Long-running orchestration tasks executed by the Celery worker.
# ============================================================
from __future__ import annotations

import logging

from app.core.celery_app import celery_app
from app.orchestration.orchestrator import Orchestrator

logger = logging.getLogger(__name__)


@celery_app.task(name="orchestration.run_task", bind=True)
def run_task(self, goal: str):
    """
    Background task: orchestrate a full multi-agent task.

    Args:
        goal: The high-level objective.

    Returns:
        Dict with the orchestration result.
    """
    import asyncio

    orchestrator = Orchestrator()

    def on_progress(data: dict):
        """Report progress back to Celery / frontend."""
        logger.info("[task %s] %s", self.request.id, data)
        self.update_state(state="PROGRESS", meta=data)

    result = asyncio.run(orchestrator.execute(goal=goal, on_progress=on_progress))
    return result.to_dict()


@celery_app.task(name="orchestration.run_single_agent", bind=True)
def run_single_agent(self, agent_slug: str, instruction: str):
    """Background task: run a single agent on an instruction."""
    import asyncio

    from app.agents import AgentContext, get_agent

    agent = get_agent(agent_slug)
    if agent is None:
        return {"success": False, "error": f"Agent '{agent_slug}' not found"}

    context = AgentContext(
        task_id=self.request.id,
        task_title=instruction,
        instruction=instruction,
    )

    result = asyncio.run(agent.run(context))
    return {
        "success": result.success,
        "content": result.content,
        "error": result.error,
        "agent": agent_slug,
    }
