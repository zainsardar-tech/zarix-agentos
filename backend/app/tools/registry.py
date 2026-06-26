# ============================================================
#  Zarix AgentOS — Tool Registry
# ============================================================
#  Central registry of all available tools. Agents reference
#  tools by name; the registry handles instantiation + dispatch.
# ============================================================
from __future__ import annotations

import logging
from typing import Optional

from app.tools.base import BaseTool, ToolResult
from app.tools.code_tool import CodeExecutionTool
from app.tools.file_tool import FileListTool, FileReadTool, FileWriteTool
from app.tools.shell_tool import ShellExecutionTool
from app.tools.web_tool import WebFetchTool, WebSearchTool

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Registry and dispatcher for all agent tools.

    Usage:
        registry = ToolRegistry()
        result = await registry.execute("web_search", query="FastAPI")
    """

    _TOOL_CLASSES: dict[str, type[BaseTool]] = {
        "code_exec": CodeExecutionTool,
        "web_search": WebSearchTool,
        "web_fetch": WebFetchTool,
        "file_read": FileReadTool,
        "file_write": FileWriteTool,
        "file_list": FileListTool,
        "shell_exec": ShellExecutionTool,
    }

    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}
        self._init_tools()

    def _init_tools(self) -> None:
        """Instantiate all tools."""
        for name, cls in self._TOOL_CLASSES.items():
            try:
                self._tools[name] = cls()
            except Exception as exc:
                logger.warning("Failed to init tool '%s': %s", name, exc)

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Return a tool instance by name."""
        return self._tools.get(name)

    def list_tools(self) -> list[dict]:
        """Return metadata for all registered tools."""
        return [tool.to_dict() for tool in self._tools.values()]

    def list_tools_for_agent(self, tool_names: list[str]) -> list[dict]:
        """Return metadata for a specific set of tools."""
        return [
            self._tools[name].to_dict()
            for name in tool_names
            if name in self._tools
        ]

    async def execute(self, name: str, **kwargs) -> ToolResult:
        """Execute a tool by name with the given arguments."""
        tool = self._tools.get(name)
        if tool is None:
            return ToolResult(success=False, error=f"Unknown tool: {name}")
        if not tool.enabled:
            return ToolResult(success=False, error=f"Tool '{name}' is disabled")
        try:
            logger.info("Executing tool '%s' with args: %s", name, list(kwargs.keys()))
            return await tool.execute(**kwargs)
        except Exception as exc:
            logger.error("Tool '%s' execution failed: %s", name, exc)
            return ToolResult(success=False, error=str(exc))


# ── Module-level singleton ───────────────────────────────────
_registry: Optional[ToolRegistry] = None


def get_registry() -> ToolRegistry:
    """Return the shared ToolRegistry singleton."""
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry
