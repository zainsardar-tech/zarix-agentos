# ============================================================
#  Zarix AgentOS — Tools API Routes
# ============================================================
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.tools import get_registry

router = APIRouter()


class ToolExecuteRequest(BaseModel):
    """Request to execute a tool."""

    tool_name: str
    arguments: dict = {}


@router.get("/")
async def list_tools():
    """List all available tools."""
    registry = get_registry()
    return {"tools": registry.list_tools()}


@router.get("/{tool_name}")
async def get_tool_detail(tool_name: str):
    """Get details of a specific tool."""
    registry = get_registry()
    tool = registry.get_tool(tool_name)
    if tool is None:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    return tool.to_dict()


@router.post("/execute")
async def execute_tool(request: ToolExecuteRequest):
    """Execute a tool with the given arguments."""
    registry = get_registry()
    result = await registry.execute(request.tool_name, **request.arguments)
    return {
        "success": result.success,
        "output": result.output,
        "error": result.error,
        "data": result.data,
    }
