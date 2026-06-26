# ============================================================
#  Zarix AgentOS — Meta Llama Provider
# ============================================================
#  Models: Llama (via OpenAI-compatible endpoints — Together / Groq / local)
# ============================================================
from typing import AsyncIterator, Optional

from openai import AsyncOpenAI

from app.llm.base import BaseLLMProvider, LLMConfig, LLMMessage, LLMResponse


class MetaProvider(BaseLLMProvider):
    """Meta Llama models served through an OpenAI-compatible endpoint."""

    provider_name = "meta"
    default_model = "meta-llama/Llama-3.3-70B-Instruct-Turbo"
    available_models = [
        "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "meta-llama/Llama-3.3-70B-Instruct",
        "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "llama-3.3-70b-versatile",  # Groq
        "llama-3.1-8b-instant",  # Groq
    ]

    def __init__(self, api_key: str, base_url: Optional[str] = None) -> None:
        super().__init__(api_key, base_url)
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    def _to_messages(self, messages: list[LLMMessage]) -> list[dict]:
        return [
            {"role": m.role, "content": m.content, **({"name": m.name} if m.name else {})}
            for m in messages
        ]

    async def chat(
        self,
        messages: list[LLMMessage],
        config: Optional[LLMConfig] = None,
    ) -> LLMResponse:
        config = config or LLMConfig()
        model = config.model or self.default_model

        response = await self.client.chat.completions.create(
            model=model,
            messages=self._to_messages(messages),
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout=config.timeout,
        )
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
        model = config.model or self.default_model

        stream = await self.client.chat.completions.create(
            model=model,
            messages=self._to_messages(messages),
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            stream=True,
            timeout=config.timeout,
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
