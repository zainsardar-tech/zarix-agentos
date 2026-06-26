# ============================================================
#  Zarix AgentOS — Base Tool Class
# ============================================================
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ToolResult:
    """Standardised result from a tool execution."""

    success: bool
    output: str = ""
    error: Optional[str] = None
    data: dict = field(default_factory=dict)


class BaseTool(ABC):
    """
    Abstract base for all agent tools.

    Each tool has a name, description, and an async `execute` method.
    Tools are registered in the ToolRegistry and invoked by agents.
    """

    name: str = "base_tool"
    description: str = "A base tool."
    category: str = "general"  # code | web | file | shell
    enabled: bool = True

    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult:
        """Run the tool with the given arguments."""
        ...

    def to_dict(self) -> dict:
        """Serialise tool metadata."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "enabled": self.enabled,
        }
