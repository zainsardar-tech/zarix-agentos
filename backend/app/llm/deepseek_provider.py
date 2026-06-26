# ============================================================
#  Zarix AgentOS — DeepSeek Provider
# ============================================================
#  Models: DeepSeek Coder · DeepSeek Reasoner
# ============================================================
from typing import AsyncIterator, Optional

from openai import AsyncOpenAI

from app.llm.base import BaseLLMProvider, LLMConfig, LLMMessage, LLMResponse


class DeepSeekProvider(BaseLLMProvider):
    """DeepSeek models via their OpenAI-compatible API."""

    provider_name = "deepseek"
    default_model = "deepseek-chat"
    available_models = [
        "deepseek-coder",  # DeepSeek Coder
        "deepseek-reasoner",  # DeepSeek Reasoner (R1)
        "deepseek-chat",
        "deepseek-v3",
    ]

    DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

    def __init__(self, api_key: str, base_url: Optional[str] = None) -> None:
        super().__init__(api_key, base_url or self.DEEPSEEK_BASE_URL)
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=self.base_url,
        )

    def _resolve_model(self, model: str) -> str:
        """Resolve friendly aliases."""
        aliases = {
            "deepseek-coder": "deepseek-coder",
            "deepseek-reasoner": "deepseek-reasoner",
        }
        return aliases.get(model, model)

    def _to_messages(self, messages: list[LLMMessage]) -> list[dict]:
        return [{"role": m.role, "content": m.content} for m in messages]

    async def chat(
        self,
        messages: list[LLMMessage],
        config: Optional[LLMConfig] = None,
    ) -> LLMResponse:
        config = config or LLMConfig()
        model = self._resolve_model(config.model or self.default_model)

        # DeepSeek Reasoner does not support temperature / tools
        kwargs: dict = {
            "model": model,
            "messages": self._to_messages(messages),
            "max_tokens": config.max_tokens,
            "timeout": config.timeout,
        }
        if "reasoner" not in model:
            kwargs["temperature"] = config.temperature

        response = await self.client.chat.completions.create(**kwargs)
        choice = response.choices[0]
        content = choice.message.content or ""

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
        model = self._resolve_model(config.model or self.default_model)

        kwargs: dict = {
            "model": model,
            "messages": self._to_messages(messages),
            "max_tokens": config.max_tokens,
            "stream": True,
            "timeout": config.timeout,
        }
        if "reasoner" not in model:
            kwargs["temperature"] = config.temperature

        stream = await self.client.chat.completions.create(**kwargs)
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
