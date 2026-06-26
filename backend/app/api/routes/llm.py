# ============================================================
#  Zarix AgentOS — LLM Gateway API Routes
# ============================================================
from fastapi import APIRouter
from pydantic import BaseModel

from app.llm import LLMConfig, LLMMessage, get_gateway

router = APIRouter()


class ChatRequest(BaseModel):
    """Direct LLM chat request."""

    message: str
    provider: str = ""
    model: str = ""
    system_prompt: str = ""
    temperature: float = 0.2
    max_tokens: int = 4096


@router.get("/providers")
async def list_providers():
    """List all configured LLM providers and their models."""
    gateway = get_gateway()
    return {"providers": gateway.list_providers()}


@router.get("/models")
async def list_all_models():
    """List all available models across all providers."""
    gateway = get_gateway()
    return {"models": gateway.list_all_models()}


@router.post("/chat")
async def chat(request: ChatRequest):
    """Send a direct message to an LLM provider."""
    gateway = get_gateway()

    messages: list[LLMMessage] = []
    if request.system_prompt:
        messages.append(LLMMessage(role="system", content=request.system_prompt))
    messages.append(LLMMessage(role="user", content=request.message))

    config = LLMConfig(
        model=request.model or None,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    response = await gateway.chat(
        messages=messages,
        provider=request.provider or None,
        config=config,
    )

    return {
        "content": response.content,
        "provider": response.provider,
        "model": response.model,
        "usage": response.usage,
    }
