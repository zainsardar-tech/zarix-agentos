# ============================================================
#  Zarix AgentOS — Google Gemini Provider
# ============================================================
#  Models: Gemini (Pro / Flash / variants)
# ============================================================
import asyncio
from typing import AsyncIterator, Optional

import google.generativeai as genai

from app.llm.base import BaseLLMProvider, LLMConfig, LLMMessage, LLMResponse


class GoogleProvider(BaseLLMProvider):
    """Google Gemini models via the google-generativeai SDK."""

    provider_name = "google"
    default_model = "gemini-2.0-flash"
    available_models = [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
    ]

    def __init__(self, api_key: str, base_url: Optional[str] = None) -> None:
        super().__init__(api_key, base_url)
        genai.configure(api_key=api_key)

    def _build_prompt(self, messages: list[LLMMessage]) -> tuple[str, list[dict]]:
        """Gemini uses a single system instruction + contents list."""
        system_text = ""
        contents = []
        for m in messages:
            if m.role == "system":
                system_text += m.content + "\n"
            else:
                role = "user" if m.role == "user" else "model"
                contents.append({"role": role, "parts": [m.content]})
        return system_text.strip(), contents

    async def chat(
        self,
        messages: list[LLMMessage],
        config: Optional[LLMConfig] = None,
    ) -> LLMResponse:
        config = config or LLMConfig()
        model = config.model or self.default_model
        system_text, contents = self._build_prompt(messages)

        gen_config = genai.types.GenerationConfig(
            temperature=config.temperature,
            max_output_tokens=config.max_tokens,
        )

        model_obj = genai.GenerativeModel(
            model_name=model,
            system_instruction=system_text if system_text else None,
        )

        # google SDK is sync — run in a thread
        response = await asyncio.to_thread(
            model_obj.generate_content,
            contents,
            generation_config=gen_config,
        )

        content = response.text or ""
        usage = {}
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            usage = {
                "prompt_tokens": getattr(
                    response.usage_metadata, "prompt_token_count", 0
                ),
                "completion_tokens": getattr(
                    response.usage_metadata, "candidates_token_count", 0
                ),
                "total_tokens": getattr(
                    response.usage_metadata, "total_token_count", 0
                ),
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
        system_text, contents = self._build_prompt(messages)

        gen_config = genai.types.GenerationConfig(
            temperature=config.temperature,
            max_output_tokens=config.max_tokens,
        )

        model_obj = genai.GenerativeModel(
            model_name=model,
            system_instruction=system_text if system_text else None,
        )

        # google SDK streaming is sync — wrap in a thread
        def _sync_stream():
            return model_obj.generate_content(
                contents,
                generation_config=gen_config,
                stream=True,
            )

        stream = await asyncio.to_thread(_sync_stream)
        for chunk in stream:
            if chunk.text:
                yield chunk.text
