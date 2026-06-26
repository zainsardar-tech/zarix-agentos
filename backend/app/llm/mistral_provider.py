# ============================================================
#  Zarix AgentOS — Mistral Provider
# ============================================================
#  Models: Mistral Large (and variants)
# ============================================================
from typing import AsyncIterator, Optional

from mistralai import Mistral

from app.llm.base import BaseLLMProvider, LLMConfig, LLMMessage, LLMResponse


class MistralProvider(BaseLLMProvider):
    """Mistral models via the official mistralai SDK."""

    provider_name = "mistral"
    default_model = "mistral-large-latest"
    available_models = [
        "mistral-large-latest",
        "mistral-large-2411",
        "mistral-medium-latest",
        "mistral-small-latest",
        "mistral-nemo",
        "codestral-latest",
        "open-mistral-7b",
        "open-mixtral-8x7b",
        "open-mixtral-8x22b",
    ]

    def __init__(self, api_key: str, base_url: Optional[str] = None) -> None:
        super().__init__(api_key, base_url)
        self.client = Mistral(api_key=api_key)

    def _to_messages(self, messages: list[LLMMessage]) -> list[dict]:
        return [{"role": m.role, "content": m.content} for m in messages]

    async def chat(
        self,
        messages: list[LLMMessage],
        config: Optional[LLMConfig] = None,
    ) -> LLMResponse:
        config = config or LLMConfig()
        model = config.model or self.default_model

        response = await self.client.chat.complete_async(
            model=model,
            messages=self._to_messages(messages),
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout=config.timeout,
        )

        content = ""
        if response.choices:
            content = response.choices[0].message.content or ""

        usage = {}
        if response.usage:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
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
        model = config.model or self.default_model

        stream = await self.client.chat.stream_async(
            model=model,
            messages=self._to_messages(messages),
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )
        async for chunk in stream:
            if chunk.data and chunk.data.choices:
                delta = chunk.data.choices[0].delta
                if delta and delta.content:
                    yield delta.content
