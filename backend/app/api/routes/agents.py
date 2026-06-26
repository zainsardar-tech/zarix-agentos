# ============================================================
#  Zarix AgentOS — Agents API Routes
# ============================================================
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agents import (
    DEPARTMENTS,
    get_agent,
    list_agents,
    list_agents_by_department,
)

router = APIRouter()


class AgentRunRequest(BaseModel):
    """Request to run a single agent."""

    agent_slug: str
    instruction: str
    task_id: str = ""


@router.get("/")
async def get_all_agents():
    """List all available AI employees."""
    return {"agents": list_agents(), "total": len(list_agents())}


@router.get("/departments")
async def get_departments():
    """List agents grouped by department."""
    return {"departments": list_agents_by_department()}


@router.get("/{slug}")
async def get_agent_detail(slug: str):
    """Get details of a specific agent."""
    agent = get_agent(slug)
    if agent is None:
        raise HTTPException(status_code=404, detail=f"Agent '{slug}' not found")
    return agent.to_dict()


@router.post("/run")
async def run_agent(request: AgentRunRequest):
    """Run a single agent on an instruction (synchronous)."""
    agent = get_agent(request.agent_slug)
    if agent is None:
        raise HTTPException(
            status_code=404,
            detail=f"Agent '{request.agent_slug}' not found",
        )

    from app.agents.base import AgentContext

    context = AgentContext(
        task_id=request.task_id or f"api_{request.agent_slug}",
        task_title=request.instruction,
        instruction=request.instruction,
    )

    result = await agent.run(context)
    return {
        "agent": request.agent_slug,
        "success": result.success,
        "content": result.content,
        "error": result.error,
        "data": result.data,
    }
