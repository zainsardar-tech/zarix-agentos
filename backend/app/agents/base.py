# ============================================================
#  Zarix AgentOS — Base Agent Class
# ============================================================
#  Every AI employee inherits from BaseAgent. It wires together
#  the LLM gateway, memory, tools, and provides a clean `run()`
#  interface used by the orchestration engine.
# ============================================================
from __future__ import annotations

import logging
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Optional

from app.llm import LLMConfig, LLMMessage, LLMResponse, get_gateway
from app.memory.manager import MemoryManager

logger = logging.getLogger(__name__)


@dataclass
class AgentContext:
    """Runtime context passed to an agent during execution."""

    task_id: str = ""
    task_title: str = ""
    instruction: str = ""
    shared_state: dict = field(default_factory=dict)
    previous_results: list[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)


@dataclass
class AgentResult:
    """The output of an agent execution."""

    agent_slug: str
    success: bool
    content: str = ""
    data: dict = field(default_factory=dict)
    error: Optional[str] = None


class BaseAgent(ABC):
    """
    Base class for all Zarix AI employees.

    Subclasses define:
        slug, name, department, role, description, system_prompt,
        skills, tools, llm_provider, llm_model
    """

    # ── Identity ────────────────────────────────────────────
    slug: str = "base_agent"
    name: str = "Base Agent"
    department: str = "engineering"
    role: str = "General Agent"
    description: str = ""
    icon: str = "🤖"

    # ── Capabilities ────────────────────────────────────────
    system_prompt: str = "You are a helpful AI assistant."
    skills: list[str] = []
    tool_names: list[str] = []

    # ── LLM config ──────────────────────────────────────────
    llm_provider: str = ""
    llm_model: str = ""
    temperature: float = 0.2
    max_tokens: int = 4096

    def __init__(self) -> None:
        self.gateway = get_gateway()
        self.memory = MemoryManager()

    # ── Core execution ───────────────────────────────────────

    async def run(self, context: AgentContext) -> AgentResult:
        """
        Execute the agent's task.

        1. Build the system prompt.
        2. Retrieve relevant memories.
        3. Call the LLM.
        4. Optionally execute tools.
        5. Store the result in memory.
        """
        logger.info("[%s] starting execution for task '%s'", self.slug, context.task_title)

        try:
            # Build messages
            messages = await self._build_messages(context)

            # Call LLM
            config = LLMConfig(
                model=self.llm_model or None,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            response = await self.gateway.chat(
                messages=messages,
                provider=self.llm_provider or None,
                config=config,
            )

            # Store in memory
            await self.memory.add_short_term(
                agent_slug=self.slug,
                content=f"Task: {context.task_title}\nResult: {response.content[:500]}",
                task_id=context.task_id,
            )

            logger.info("[%s] execution complete", self.slug)
            return AgentResult(
                agent_slug=self.slug,
                success=True,
                content=response.content,
                data={
                    "model": response.model,
                    "provider": response.provider,
                    "usage": response.usage,
                },
            )

        except Exception as exc:
            logger.error("[%s] execution failed: %s", self.slug, exc)
            return AgentResult(
                agent_slug=self.slug,
                success=False,
                error=str(exc),
            )

    async def stream_run(self, context: AgentContext):
        """Execute and yield tokens as they arrive."""
        messages = await self._build_messages(context)
        config = LLMConfig(
            model=self.llm_model or None,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        async for token in self.gateway.stream(
            messages=messages,
            provider=self.llm_provider or None,
            config=config,
        ):
            yield token

    # ── Helpers ─────────────────────────────────────────────

    async def _build_messages(self, context: AgentContext) -> list[LLMMessage]:
        """Construct the message list for the LLM."""
        messages: list[LLMMessage] = []

        # System prompt
        system = self.system_prompt
        if self.skills:
            system += f"\n\nYour skills: {', '.join(self.skills)}."
        messages.append(LLMMessage(role="system", content=system))

        # Retrieve relevant long-term memories
        memories = await self.memory.search_long_term(
            query=context.instruction or context.task_title,
            agent_slug=self.slug,
            top_k=3,
        )
        if memories:
            memory_text = "\n".join(f"- {m}" for m in memories)
            messages.append(
                LLMMessage(
                    role="system",
                    content=f"Relevant knowledge from previous work:\n{memory_text}",
                )
            )

        # Previous step results (collaboration context)
        if context.previous_results:
            for prev in context.previous_results:
                messages.append(
                    LLMMessage(
                        role="assistant",
                        content=f"[{prev.get('agent', 'agent')}]: {prev.get('content', '')}",
                    )
                )

        # The actual instruction
        user_content = context.instruction or context.task_title
        if context.shared_state:
            user_content += f"\n\nShared context: {context.shared_state}"
        messages.append(LLMMessage(role="user", content=user_content))

        return messages

    # ── Metadata ─────────────────────────────────────────────

    def to_dict(self) -> dict:
        """Serialise agent metadata for API responses."""
        return {
            "slug": self.slug,
            "name": self.name,
            "department": self.department,
            "role": self.role,
            "description": self.description,
            "icon": self.icon,
            "skills": self.skills,
            "tools": self.tool_names,
            "llm_provider": self.llm_provider,
            "llm_model": self.llm_model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
