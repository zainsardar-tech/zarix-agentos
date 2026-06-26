# ============================================================
#  Zarix AgentOS — Orchestrator
# ============================================================
#  Executes an ExecutionPlan step-by-step. Each step runs the
#  assigned agent, passes previous results as context, and
#  supports human-in-the-loop approval for critical steps.
# ============================================================
from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Optional

from app.agents import AgentContext, AgentResult, get_agent
from app.agents.registry import AGENT_REGISTRY
from app.orchestration.planner import ExecutionPlan, PlanStep, TaskPlanner

logger = logging.getLogger(__name__)


@dataclass
class StepResult:
    """Result of a single orchestration step."""

    order: int
    agent_slug: str
    success: bool
    content: str = ""
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class OrchestrationResult:
    """Final result of an orchestrated task."""

    goal: str
    success: bool
    steps: list[StepResult] = field(default_factory=list)
    final_output: str = ""
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "goal": self.goal,
            "success": self.success,
            "final_output": self.final_output,
            "error": self.error,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "steps": [
                {
                    "order": s.order,
                    "agent_slug": s.agent_slug,
                    "success": s.success,
                    "content": s.content[:500] if s.content else "",
                    "error": s.error,
                    "started_at": s.started_at,
                    "completed_at": s.completed_at,
                }
                for s in self.steps
            ],
        }


class Orchestrator:
    """
    Coordinates multi-agent execution of a task plan.

    Features:
    - Sequential step execution with dependency awareness
    - Passes previous step results to subsequent agents (collaboration)
    - Human-in-the-loop approval for critical steps
    - Real-time progress callbacks
    """

    def __init__(self) -> None:
        self.planner = TaskPlanner()

    async def execute(
        self,
        goal: str,
        plan: Optional[ExecutionPlan] = None,
        on_progress: Optional[Callable[[dict], None]] = None,
        approval_callback: Optional[Callable[[ExecutionPlan], bool]] = None,
    ) -> OrchestrationResult:
        """
        Execute a task end-to-end.

        Args:
            goal:                 The high-level objective.
            plan:                 Pre-built plan (if None, planner generates one).
            on_progress:          Callback invoked after each step.
            approval_callback:    Called when a plan requires human approval.

        Returns:
            OrchestrationResult with all step outputs.
        """
        started = datetime.now(timezone.utc).isoformat()
        logger.info("Orchestrating task: %s", goal[:100])

        # ── Plan ─────────────────────────────────────────────
        if plan is None:
            self._emit(on_progress, {"phase": "planning", "message": "Decomposing goal..."})
            plan = await self.planner.plan(goal)

        # ── Approval ─────────────────────────────────────────
        if plan.requires_approval and approval_callback:
            self._emit(on_progress, {"phase": "approval", "message": "Awaiting human approval..."})
            approved = approval_callback(plan)
            if not approved:
                return OrchestrationResult(
                    goal=goal,
                    success=False,
                    error="Task was not approved by human operator",
                    started_at=started,
                    completed_at=datetime.now(timezone.utc).isoformat(),
                )

        self._emit(
            on_progress,
            {"phase": "execution", "message": f"Executing {len(plan.steps)} steps..."},
        )

        # ── Execute steps ────────────────────────────────────
        step_results: list[StepResult] = []
        previous_results: list[dict] = []
        shared_state: dict[str, Any] = {}

        for step in plan.steps:
            step_result = await self._execute_step(
                step=step,
                goal=goal,
                previous_results=previous_results,
                shared_state=shared_state,
                on_progress=on_progress,
            )
            step_results.append(step_result)
            previous_results.append(
                {
                    "agent": step.agent_slug,
                    "content": step_result.content,
                    "success": step_result.success,
                }
            )

            if not step_result.success:
                logger.error("Step %d failed, stopping execution", step.order)
                return OrchestrationResult(
                    goal=goal,
                    success=False,
                    steps=step_results,
                    error=f"Step {step.order} ({step.agent_slug}) failed: {step_result.error}",
                    started_at=started,
                    completed_at=datetime.now(timezone.utc).isoformat(),
                )

        # ── Final output ─────────────────────────────────────
        final_output = step_results[-1].content if step_results else ""

        result = OrchestrationResult(
            goal=goal,
            success=True,
            steps=step_results,
            final_output=final_output,
            started_at=started,
            completed_at=datetime.now(timezone.utc).isoformat(),
        )

        self._emit(on_progress, {"phase": "complete", "message": "Task completed", "result": result.to_dict()})
        logger.info("Orchestration complete: %d steps, success=%s", len(step_results), result.success)
        return result

    async def _execute_step(
        self,
        step: PlanStep,
        goal: str,
        previous_results: list[dict],
        shared_state: dict,
        on_progress: Optional[Callable],
    ) -> StepResult:
        """Execute a single plan step."""
        started = datetime.now(timezone.utc).isoformat()
        agent_slug = step.agent_slug

        self._emit(
            on_progress,
            {
                "phase": "step",
                "step": step.order,
                "agent": agent_slug,
                "message": f"Step {step.order}: {agent_slug} is working...",
            },
        )

        agent = get_agent(agent_slug)
        if agent is None:
            return StepResult(
                order=step.order,
                agent_slug=agent_slug,
                success=False,
                error=f"Agent '{agent_slug}' not found",
                started_at=started,
                completed_at=datetime.now(timezone.utc).isoformat(),
            )

        context = AgentContext(
            task_id=f"orchestration_{step.order}",
            task_title=goal,
            instruction=step.instruction,
            shared_state=shared_state,
            previous_results=previous_results,
        )

        result: AgentResult = await agent.run(context)

        completed = datetime.now(timezone.utc).isoformat()

        if result.success:
            shared_state[agent_slug] = result.content[:2000]

        return StepResult(
            order=step.order,
            agent_slug=agent_slug,
            success=result.success,
            content=result.content,
            error=result.error,
            started_at=started,
            completed_at=completed,
        )

    def _emit(self, callback: Optional[Callable], data: dict) -> None:
        """Safely invoke the progress callback."""
        if callback:
            try:
                callback(data)
            except Exception as exc:
                logger.warning("Progress callback error: %s", exc)
