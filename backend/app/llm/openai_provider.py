# ============================================================
#  Zarix AgentOS — OpenAI Provider
# ============================================================
#  Models: GPT-5.5 · GPT-4.1 · Codex models
# ============================================================
from typing import AsyncIterator, Optional

from openai import AsyncOpenAI

from app.llm.base import BaseLLMProvider, LLMConfig, LLMMessage, LLMResponse


class OpenAIProvider(BaseLLMProvider):
    """OpenAI GPT models via the official SDK."""

    provider_name = "openai"
    default_model = "gpt-4.1"
    available_models = [
        "gpt-5.5",
        "gpt-4.1",
        "gpt-4.1-mini",
        "gpt-4o",
        "gpt-4o-mini",
        "codex-mini",
        "o3-mini",
    ]

    def __init__(self, api_key: str, base_url: Optional[str] = None) -> None:
        super().__init__(api_key, base_url)
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    def _to_openai_messages(self, messages: list[LLMMessage]) -> list[dict]:
        result = []
        for m in messages:
            msg = {"role": m.role, "content": m.content}
            if m.name:
                msg["name"] = m.name
            if m.tool_call_id:
                msg["tool_call_id"] = m.tool_call_id
            result.append(msg)
        return result

    async def chat(
        self,
        messages: list[LLMMessage],
        config: Optional[LLMConfig] = None,
    ) -> LLMResponse:
        config = config or LLMConfig()
        model = config.model or self.default_model

        kwargs: dict = {
            "model": model,
            "messages": self._to_openai_messages(messages),
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "timeout": config.timeout,
        }
        if config.tools:
            kwargs["tools"] = config.tools

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
        model = config.model or self.default_model

        stream = await self.client.chat.completions.create(
            model=model,
            messages=self._to_openai_messages(messages),
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            stream=True,
            timeout=config.timeout,
        )
        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
