# ============================================================
#  Zarix AgentOS — LLM Gateway (Unified Registry)
# ============================================================
#  Single entry point for all LLM calls across 6 providers.
#  Supports: provider selection, model listing, fallback chains,
#  streaming, and automatic retry.
# ============================================================
from __future__ import annotations

import logging
from typing import AsyncIterator, Optional

from app.core.config import settings
from app.llm.anthropic_provider import AnthropicProvider
from app.llm.base import (
    BaseLLMProvider,
    LLMConfig,
    LLMMessage,
    LLMResponse,
)
from app.llm.deepseek_provider import DeepSeekProvider
from app.llm.google_provider import GoogleProvider
from app.llm.meta_provider import MetaProvider
from app.llm.mistral_provider import MistralProvider
from app.llm.openai_provider import OpenAIProvider

logger = logging.getLogger(__name__)


class LLMGateway:
    """
    Unified gateway to all configured LLM providers.

    Usage:
        gateway = LLMGateway()
        response = await gateway.chat(
            provider="anthropic",
            model="claude-sonnet",
            messages=[LLMMessage(role="user", content="Hello")],
        )
    """

    # Provider class registry
    _PROVIDER_CLASSES: dict[str, type[BaseLLMProvider]] = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "google": GoogleProvider,
        "meta": MetaProvider,
        "mistral": MistralProvider,
        "deepseek": DeepSeekProvider,
    }

    def __init__(self) -> None:
        self._providers: dict[str, BaseLLMProvider] = {}
        self._init_providers()

    def _init_providers(self) -> None:
        """Instantiate every provider that has an API key configured."""
        configs = {
            "openai": (settings.openai_api_key, None),
            "anthropic": (settings.anthropic_api_key, None),
            "google": (settings.google_api_key, None),
            "meta": (settings.meta_api_key, settings.meta_base_url),
            "mistral": (settings.mistral_api_key, None),
            "deepseek": (settings.deepseek_api_key, None),
        }
        for name, (key, base_url) in configs.items():
            if key:
                cls = self._PROVIDER_CLASSES[name]
                try:
                    self._providers[name] = cls(api_key=key, base_url=base_url)
                    logger.info("LLM provider '%s' initialised", name)
                except Exception as exc:
                    logger.warning("Failed to init provider '%s': %s", name, exc)
            else:
                logger.debug("LLM provider '%s' skipped (no API key)", name)

    # ── Public API ───────────────────────────────────────────

    def get_provider(self, name: str) -> Optional[BaseLLMProvider]:
        """Return an initialised provider by name, or None."""
        return self._providers.get(name.lower())

    def list_providers(self) -> list[dict]:
        """Return metadata for every available provider."""
        result = []
        for name, provider in self._providers.items():
            result.append(
                {
                    "provider": name,
                    "default_model": provider.default_model,
                    "models": provider.list_models(),
                    "available": provider.is_available(),
                }
            )
        return result

    def list_all_models(self) -> dict[str, list[str]]:
        """Return {provider: [models]} for all providers."""
        return {
            name: provider.list_models()
            for name, provider in self._providers.items()
        }

    async def chat(
        self,
        messages: list[LLMMessage],
        provider: Optional[str] = None,
        model: Optional[str] = None,
        config: Optional[LLMConfig] = None,
        fallback: Optional[list[str]] = None,
    ) -> LLMResponse:
        """
        Generate a completion.

        Args:
            messages:    Conversation messages.
            provider:     Provider name (defaults to settings.default_llm_provider).
            model:        Model id (defaults to provider default).
            config:       Runtime config (temperature, max_tokens, ...).
            fallback:    Ordered list of provider names to try if the primary fails.
        """
        config = config or LLMConfig()
        if model:
            config.model = model

        provider_name = (provider or settings.default_llm_provider).lower()
        chain = [provider_name] + (fallback or [])

        last_error: Optional[Exception] = None
        for p_name in chain:
            p = self._providers.get(p_name)
            if p is None:
                logger.warning("Provider '%s' not available, skipping", p_name)
                continue
            try:
                response = await p.chat(messages, config)
                logger.info(
                    "LLM chat success via %s/%s (tokens=%s)",
                    p_name,
                    response.model,
                    response.usage.get("total_tokens", "?"),
                )
                return response
            except Exception as exc:
                last_error = exc
                logger.error("Provider '%s' failed: %s", p_name, exc)
                continue

        raise RuntimeError(
            f"All LLM providers failed. Last error: {last_error}"
        )

    async def stream(
        self,
        messages: list[LLMMessage],
        provider: Optional[str] = None,
        model: Optional[str] = None,
        config: Optional[LLMConfig] = None,
    ) -> AsyncIterator[str]:
        """Stream a completion token-by-token."""
        config = config or LLMConfig()
        if model:
            config.model = model

        provider_name = (provider or settings.default_llm_provider).lower()
        p = self._providers.get(provider_name)
        if p is None:
            raise RuntimeError(f"Provider '{provider_name}' not available")

        async for token in p.stream_chat(messages, config):
            yield token


# ── Module-level singleton ───────────────────────────────────
_gateway: Optional[LLMGateway] = None


def get_gateway() -> LLMGateway:
    """Return the shared LLMGateway singleton."""
    global _gateway
    if _gateway is None:
        _gateway = LLMGateway()
    return _gateway
