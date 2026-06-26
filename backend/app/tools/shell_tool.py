# ============================================================
#  Zarix AgentOS — Shell Execution Tool
# ============================================================
#  Executes shell commands in a subprocess with a timeout.
#  Disabled by default — must be explicitly enabled via settings.
# ============================================================
from __future__ import annotations

import asyncio
import shlex

from app.core.config import settings
from app.tools.base import BaseTool, ToolResult

# Commands that are never allowed
BLOCKED_COMMANDS = {
    "rm -rf /",
    "mkfs",
    "dd if=",
    ":(){:|:&};:",
    "shutdown",
    "reboot",
    "halt",
    "init 0",
}


class ShellExecutionTool(BaseTool):
    """Execute shell commands in a sandboxed subprocess."""

    name = "shell_exec"
    description = (
        "Execute a shell command and return stdout/stderr. "
        "Use for running builds, tests, git, and system commands. "
        "Disabled by default for security."
    )
    category = "shell"

    async def execute(self, command: str, timeout: int = 0, **kwargs) -> ToolResult:
        if not settings.enable_shell_access:
            return ToolResult(
                success=False,
                error="Shell execution is disabled. Set ENABLE_SHELL_ACCESS=true to enable.",
            )

        # Safety check
        cmd_lower = command.lower().strip()
        for blocked in BLOCKED_COMMANDS:
            if blocked in cmd_lower:
                return ToolResult(
                    success=False,
                    error=f"Blocked command detected: '{blocked}'",
                )

        actual_timeout = timeout or settings.sandbox_timeout

        try:
            args = shlex.split(command)
            proc = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), timeout=actual_timeout
            )

            success = proc.returncode == 0
            output = stdout.decode("utf-8", errors="replace")
            error = stderr.decode("utf-8", errors="replace") if stderr else None

            return ToolResult(
                success=success,
                output=output,
                error=error,
                data={"exit_code": proc.returncode, "command": command},
            )

        except asyncio.TimeoutError:
            return ToolResult(
                success=False,
                error=f"Command timed out after {actual_timeout}s",
            )
        except Exception as exc:
            return ToolResult(success=False, error=str(exc))
