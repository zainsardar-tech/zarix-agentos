# ============================================================
#  Zarix AgentOS — Anthropic Provider
# ============================================================
#  Models: Claude Opus · Claude Sonnet · Claude Code
# ============================================================
from typing import AsyncIterator, Optional

from anthropic import AsyncAnthropic

from app.llm.base import BaseLLMProvider, LLMConfig, LLMMessage, LLMResponse


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude models via the official SDK."""

    provider_name = "anthropic"
    default_model = "claude-sonnet-4-20250514"
    available_models = [
        "claude-opus-4-20250514",
        "claude-sonnet-4-20250514",
        "claude-3-7-sonnet-20250219",
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-code",  # alias for code-optimised routing
    ]

    def __init__(self, api_key: str, base_url: Optional[str] = None) -> None:
        super().__init__(api_key, base_url)
        self.client = AsyncAnthropic(api_key=api_key, base_url=base_url)

    def _split_messages(
        self, messages: list[LLMMessage]
    ) -> tuple[str, list[dict]]:
        """Anthropic separates system prompt from the message list."""
        system_text = ""
        chat_messages = []
        for m in messages:
            if m.role == "system":
                system_text += m.content + "\n"
            else:
                chat_messages.append({"role": m.role, "content": m.content})
        return system_text.strip(), chat_messages

    def _resolve_model(self, model: str) -> str:
        """Resolve friendly aliases to real model IDs."""
        aliases = {
            "claude-opus": "claude-opus-4-20250514",
            "claude-sonnet": "claude-sonnet-4-20250514",
            "claude-code": "claude-sonnet-4-20250514",
        }
        return aliases.get(model, model)

    async def chat(
        self,
        messages: list[LLMMessage],
        config: Optional[LLMConfig] = None,
    ) -> LLMResponse:
        config = config or LLMConfig()
        model = self._resolve_model(config.model or self.default_model)
        system_text, chat_messages = self._split_messages(messages)

        kwargs: dict = {
            "model": model,
            "messages": chat_messages,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "timeout": config.timeout,
        }
        if system_text:
            kwargs["system"] = system_text

        response = await self.client.messages.create(**kwargs)
        content = ""
        if response.content:
            content = "".join(
                block.text
                for block in response.content
                if hasattr(block, "text")
            )

        usage = {}
        if response.usage:
            usage = {
                "prompt_tokens": response.usage.input_tokens,
                "completion_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.input_tokens
                + response.usage.output_tokens,
            }

        return LLMResponse(
            content=content,
            provider=self.provider_name,
            model=model,
            usage=usage,
            raw=response,
        )

    async def stream_chat(
        self,
        messages: list[LLMMessage],
        config: Optional[LLMConfig] = None,
    ) -> AsyncIterator[str]:
        config = config or LLMConfig()
        model = self._resolve_model(config.model or self.default_model)
        system_text, chat_messages = self._split_messages(messages)

        kwargs: dict = {
            "model": model,
            "messages": chat_messages,
            "max_tokens": config.max_tokens,
            "temperature": config.temperature,
            "timeout": config.timeout,
        }
        if system_text:
            kwargs["system"] = system_text

        async with self.client.messages.stream(**kwargs) as stream:
            async for text in stream.text_stream:
                yield text
