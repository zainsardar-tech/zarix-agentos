# ============================================================
#  Zarix AgentOS — Code Execution Tool
# ============================================================
#  Safely executes Python code in a subprocess with a timeout.
# ============================================================
from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

from app.core.config import settings
from app.tools.base import BaseTool, ToolResult


class CodeExecutionTool(BaseTool):
    """Execute Python code in an isolated subprocess."""

    name = "code_exec"
    description = (
        "Execute Python code and return stdout, stderr, and the exit code. "
        "Use for running scripts, tests, data analysis, and computations."
    )
    category = "code"

    async def execute(self, code: str, language: str = "python", **kwargs) -> ToolResult:
        if not settings.enable_code_execution:
            return ToolResult(success=False, error="Code execution is disabled")

        if language != "python":
            return ToolResult(
                success=False,
                error=f"Unsupported language: {language}. Only 'python' is supported.",
            )

        # Write code to a temp file and run it
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, dir="/tmp"
        ) as f:
            f.write(code)
            script_path = f.name

        try:
            proc = await asyncio.create_subprocess_exec(
                "python3",
                script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=settings.sandbox_timeout
            )

            success = proc.returncode == 0
            output = stdout.decode("utf-8", errors="replace")
            error = stderr.decode("utf-8", errors="replace") if stderr else None

            return ToolResult(
                success=success,
                output=output,
                error=error,
                data={"exit_code": proc.returncode},
            )

        except asyncio.TimeoutError:
            return ToolResult(
                success=False,
                error=f"Code execution timed out after {settings.sandbox_timeout}s",
            )
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))
        finally:
            Path(script_path).unlink(missing_ok=True)
