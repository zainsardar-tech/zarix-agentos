# ============================================================
#  Zarix AgentOS — File Operations Tool
# ============================================================
from __future__ import annotations

import os
from pathlib import Path

from app.tools.base import BaseTool, ToolResult

# Restrict file access to a workspace directory
WORKSPACE_DIR = Path(os.environ.get("ZARIX_WORKSPACE", "./workspace")).resolve()
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)


def _safe_path(filepath: str) -> Path:
    """Resolve a path within the workspace, preventing directory traversal."""
    resolved = (WORKSPACE_DIR / filepath).resolve()
    if not str(resolved).startswith(str(WORKSPACE_DIR)):
        raise ValueError(f"Path '{filepath}' is outside the workspace")
    return resolved


class FileReadTool(BaseTool):
    """Read the contents of a file from the workspace."""

    name = "file_read"
    description = "Read the contents of a file from the Zarix workspace."
    category = "file"

    async def execute(self, path: str, **kwargs) -> ToolResult:
        try:
            filepath = _safe_path(path)
            if not filepath.exists():
                return ToolResult(success=False, error=f"File not found: {path}")
            content = filepath.read_text(encoding="utf-8")
            return ToolResult(
                success=True,
                output=content,
                data={"path": str(filepath), "size": len(content)},
            )
        except ValueError as exc:
            return ToolResult(success=False, error=str(exc))
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))


class FileWriteTool(BaseTool):
    """Write content to a file in the workspace."""

    name = "file_write"
    description = "Write content to a file in the Zarix workspace."
    category = "file"

    async def execute(self, path: str, content: str, **kwargs) -> ToolResult:
        try:
            filepath = _safe_path(path)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(content, encoding="utf-8")
            return ToolResult(
                success=True,
                output=f"File written: {path} ({len(content)} bytes)",
                data={"path": str(filepath), "size": len(content)},
            )
        except ValueError as exc:
            return ToolResult(success=False, error=str(exc))
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))


class FileListTool(BaseTool):
    """List files in a workspace directory."""

    name = "file_list"
    description = "List files and directories in the Zarix workspace."
    category = "file"

    async def execute(self, path: str = ".", **kwargs) -> ToolResult:
        try:
            dirpath = _safe_path(path)
            if not dirpath.exists():
                return ToolResult(success=False, error=f"Directory not found: {path}")
            entries = []
            for entry in sorted(dirpath.iterdir()):
                entries.append(
                    {
                        "name": entry.name,
                        "type": "dir" if entry.is_dir() else "file",
                        "size": entry.stat().st_size if entry.is_file() else 0,
                    }
                )
            return ToolResult(
                success=True,
                output=f"Listed {len(entries)} entries in {path}",
                data={"entries": entries},
            )
        except ValueError as exc:
            return ToolResult(success=False, error=str(exc))
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))
