# ============================================================
#  Zarix AgentOS — LLM Base Provider Interface
# ============================================================
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Optional


@dataclass
class LLMMessage:
    """A single chat message."""

    role: str  # "system" | "user" | "assistant" | "tool"
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None


@dataclass
class LLMResponse:
    """Normalised response from any provider."""

    content: str
    provider: str
    model: str
    usage: dict = field(default_factory=dict)
    raw: Any = None


@dataclass
class LLMConfig:
    """Runtime configuration for a completion request."""

    model: str = ""
    temperature: float = 0.2
    max_tokens: int = 4096
    timeout: int = 120
    stream: bool = False
    tools: list = field(default_factory=list)
    extra: dict = field(default_factory=dict)


class BaseLLMProvider(ABC):
    """Abstract base every LLM provider must implement."""

    provider_name: str = "base"
    default_model: str = ""
    available_models: list[str] = []

    def __init__(self, api_key: str, base_url: Optional[str] = None) -> None:
        self.api_key = api_key
        self.base_url = base_url

    @abstractmethod
    async def chat(
        self,
        messages: list[LLMMessage],
        config: Optional[LLMConfig] = None,
    ) -> LLMResponse:
        """Generate a completion."""
        ...

    @abstractmethod
    async def stream_chat(
        self,
        messages: list[LLMMessage],
        config: Optional[LLMConfig] = None,
    ) -> AsyncIterator[str]:
        """Stream a completion token-by-token."""
        ...

    def is_available(self) -> bool:
        """Whether this provider is configured (has an API key)."""
        return bool(self.api_key)

    def list_models(self) -> list[str]:
        """Return the models this provider supports."""
        return list(self.available_models)
