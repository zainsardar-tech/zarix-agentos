# ============================================================
#  Zarix AgentOS — Task Planner
# ============================================================
#  Uses an LLM to decompose a high-level goal into an ordered
#  list of steps, each assigned to the best agent.
# ============================================================
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Optional

from app.agents.registry import AGENT_REGISTRY, list_agents
from app.llm import LLMConfig, LLMMessage, get_gateway

logger = logging.getLogger(__name__)


@dataclass
class PlanStep:
    """A single step in an execution plan."""

    order: int
    agent_slug: str
    instruction: str
    depends_on: list[int] = field(default_factory=list)


@dataclass
class ExecutionPlan:
    """A decomposed plan for a task."""

    goal: str
    steps: list[PlanStep] = field(default_factory=list)
    requires_approval: bool = False

    def to_dict(self) -> dict:
        return {
            "goal": self.goal,
            "requires_approval": self.requires_approval,
            "steps": [
                {
                    "order": s.order,
                    "agent_slug": s.agent_slug,
                    "instruction": s.instruction,
                    "depends_on": s.depends_on,
                }
                for s in self.steps
            ],
        }


class TaskPlanner:
    """
    Decomposes a natural-language goal into a structured plan
    using the LLM and knowledge of available agents.
    """

    PLANNER_PROMPT = """You are the Task Planner for Zarix AgentOS — an AI Workforce Operating System.

Your job is to decompose a high-level goal into an ordered list of steps, each assigned to the most suitable AI agent.

Available agents and their roles:
{agents}

Rules:
1. Break the goal into 2-8 logical, sequential steps.
2. Assign each step to exactly ONE agent using its slug.
3. Write a clear, specific instruction for each step.
4. Order steps logically (architecture → design → build → test → deploy).
5. If the goal involves critical/irreversible actions, set requires_approval to true.

Respond ONLY with valid JSON in this exact format:
{{
  "requires_approval": false,
  "steps": [
    {{
      "order": 1,
      "agent_slug": "cto_agent",
      "instruction": "Design the system architecture for ..."
    }}
  ]
}}"""

    def __init__(self) -> None:
        self.gateway = get_gateway()

    def _build_agent_catalog(self) -> str:
        """Build a text catalog of available agents."""
        lines = []
        for agent in list_agents():
            lines.append(
                f"- {agent['slug']}: {agent['name']} — {agent['description']} "
                f"(skills: {', '.join(agent['skills'][:5])})"
            )
        return "\n".join(lines)

    async def plan(self, goal: str) -> ExecutionPlan:
        """
        Decompose a goal into an ExecutionPlan.

        Args:
            goal: The high-level objective in natural language.

        Returns:
            An ExecutionPlan with ordered steps.
        """
        logger.info("Planning task: %s", goal[:100])

        catalog = self._build_agent_catalog()
        system_prompt = self.PLANNER_PROMPT.format(agents=catalog)

        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(
                role="user",
                content=f"Goal: {goal}\n\nDecompose this into an execution plan.",
            ),
        ]

        config = LLMConfig(temperature=0.1, max_tokens=2048)
        response = await self.gateway.chat(
            messages=messages,
            provider="anthropic",
            config=config,
        )

        plan = self._parse_plan(response.content, goal)
        logger.info("Plan created with %d steps", len(plan.steps))
        return plan

    def _parse_plan(self, content: str, goal: str) -> ExecutionPlan:
        """Parse the LLM's JSON response into an ExecutionPlan."""
        # Extract JSON from the response (handle markdown fences)
        text = content.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Failed to parse plan JSON, using fallback")
            return self._fallback_plan(goal)

        steps = []
        for s in data.get("steps", []):
            slug = s.get("agent_slug", "")
            # Validate agent exists
            if slug not in AGENT_REGISTRY:
                logger.warning("Unknown agent '%s' in plan, skipping", slug)
                continue
            steps.append(
                PlanStep(
                    order=s.get("order", len(steps) + 1),
                    agent_slug=slug,
                    instruction=s.get("instruction", ""),
                    depends_on=s.get("depends_on", []),
                )
            )

        if not steps:
            return self._fallback_plan(goal)

        return ExecutionPlan(
            goal=goal,
            steps=steps,
            requires_approval=data.get("requires_approval", False),
        )

    def _fallback_plan(self, goal: str) -> ExecutionPlan:
        """Simple fallback plan if LLM parsing fails."""
        return ExecutionPlan(
            goal=goal,
            requires_approval=False,
            steps=[
                PlanStep(
                    order=1,
                    agent_slug="cto_agent",
                    instruction=f"Analyse the goal and provide an architecture overview: {goal}",
                ),
                PlanStep(
                    order=2,
                    agent_slug="fullstack_engineer_agent",
                    instruction=f"Implement the solution for: {goal}",
                ),
                PlanStep(
                    order=3,
                    agent_slug="qa_engineer_agent",
                    instruction=f"Test and validate the implementation for: {goal}",
                ),
            ],
        )
