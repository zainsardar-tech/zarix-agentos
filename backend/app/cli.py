# ============================================================
#  Zarix AgentOS — CLI Tool
# ============================================================
#  Command-line interface for the Zarix AgentOS platform.
#
#  Usage:
#    zarix agents                    List all AI employees
#    zarix agents --dept engineering Filter by department
#    zarix run <agent> <instruction> Run a single agent
#    zarix task <goal>               Orchestrate a multi-agent task
#    zarix llm providers             List LLM providers
#    zarix llm chat <message>        Chat directly with an LLM
#    zarix tools                     List available tools
#    zarix tools exec <tool> <json> Execute a tool
#    zarix serve                     Start the API server
# ============================================================
import asyncio
import json
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Banner
BANNER = r"""
[bold cyan]
   ███████╗███████╗ █████╗ ██╗  ██╗██╗███████╗
   ╚══███╔╝██╔════╝██╔══██╗██║ ██╔╝██║██╔════╝
     ███╔╝ █████╗  ███████║█████╔╝ ██║███████╗
    ███╔╝  ██╔══╝  ██╔══██║██╔═██╗ ██║╚════██║
   ███████╗███████╗██║  ██║██║  ██╗██║███████║
   ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
[/bold cyan]
[bold]AgentOS — The Autonomous AI Workforce Operating System[/bold]
"""


@click.group()
@click.version_option(version="1.0.0", prog_name="zarix")
def cli():
    """🛰️ Zarix AgentOS — AI Workforce Operating System CLI."""
    pass


# ── Agents ────────────────────────────────────────────────────
@cli.group()
def agents():
    """Manage and list AI employees."""
    pass


@agents.command("list")
@click.option("--dept", "-d", default=None, help="Filter by department")
def agents_list(dept):
    """List all available AI agents."""
    from app.agents import list_agents, list_agents_by_department

    console.print(BANNER)

    if dept:
        grouped = list_agents_by_department()
        agents_data = grouped.get(dept, [])
        if not agents_data:
            console.print(f"[red]No agents found in department '{dept}'[/red]")
            return
        _print_agents_table(agents_data, dept)
    else:
        grouped = list_agents_by_department()
        for department, agents_data in grouped.items():
            _print_agents_table(agents_data, department)


def _print_agents_table(agents_data, department):
    """Print a rich table of agents."""
    table = Table(title=f"  {department.upper()} Department", show_header=True)
    table.add_column("Icon", style="cyan", width=4)
    table.add_column("Agent", style="bold white")
    table.add_column("Slug", style="dim")
    table.add_column("Role", style="green")
    table.add_column("LLM", style="yellow")
    table.add_column("Skills", style="blue")

    for a in agents_data:
        table.add_row(
            a["icon"],
            a["name"],
            a["slug"],
            a["role"],
            f"{a['llm_provider']}/{a['llm_model']}",
            ", ".join(a["skills"][:4]),
        )
    console.print(table)
    console.print()


@agents.command("run")
@click.argument("agent_slug")
@click.argument("instruction")
def agents_run(agent_slug, instruction):
    """Run a single agent on an instruction."""
    from app.agents import AgentContext, get_agent

    agent = get_agent(agent_slug)
    if agent is None:
        console.print(f"[red]Agent '{agent_slug}' not found.[/red]")
        console.print("[dim]Run 'zarix agents list' to see available agents.[/dim]")
        sys.exit(1)

    console.print(BANNER)
    console.print(
        Panel(
            f"[bold]{agent.icon} {agent.name}[/bold]\n"
            f"[dim]{agent.role}[/dim]\n\n"
            f"[cyan]Instruction:[/cyan] {instruction}",
            title="Agent Execution",
            border_style="cyan",
        )
    )

    context = AgentContext(
        task_id=f"cli_{agent_slug}",
        task_title=instruction,
        instruction=instruction,
    )

    with console.status(f"[bold cyan]{agent.icon} {agent.name} is working..."):
        result = asyncio.run(agent.run(context))

    if result.success:
        console.print()
        console.print(
            Panel(result.content, title=f"✅ {agent.name} Output", border_style="green")
        )
    else:
        console.print(f"\n[red]❌ Error: {result.error}[/red]")


# ── Tasks (Orchestration) ────────────────────────────────────
@cli.group()
def task():
    """Multi-agent task orchestration."""
    pass


@task.command("run")
@click.argument("goal")
def task_run(goal):
    """Orchestrate a multi-agent task from a goal."""
    from app.orchestration import Orchestrator

    console.print(BANNER)
    console.print(
        Panel(
            f"[bold cyan]Goal:[/bold cyan] {goal}",
            title="🚀 Multi-Agent Orchestration",
            border_style="cyan",
        )
    )

    orchestrator = Orchestrator()

    def on_progress(event):
        phase = event.get("phase", "")
        message = event.get("message", "")
        if phase == "step":
            console.print(f"  [yellow]→[/yellow] {message}")
        elif phase == "planning":
            console.print(f"  [blue]📋[/blue] {message}")
        elif phase == "complete":
            console.print(f"  [green]✅[/green] {message}")

    with console.status("[bold cyan]Orchestrating AI workforce..."):
        result = asyncio.run(orchestrator.execute(goal=goal, on_progress=on_progress))

    console.print()
    if result.success:
        console.print(
            Panel(
                result.final_output[:3000],
                title="✅ Task Complete",
                border_style="green",
            )
        )
        console.print(
            f"\n[green]Completed in {len(result.steps)} steps.[/green]"
        )
    else:
        console.print(f"[red]❌ Task failed: {result.error}[/red]")


@task.command("plan")
@click.argument("goal")
def task_plan(goal):
    """Generate an execution plan without running it."""
    from app.orchestration import TaskPlanner

    planner = TaskPlanner()
    with console.status("[bold blue]Planning..."):
        plan = asyncio.run(planner.plan(goal))

    console.print(BANNER)
    console.print(f"[bold cyan]Goal:[/bold cyan] {goal}\n")

    table = Table(title="Execution Plan", show_header=True)
    table.add_column("Step", style="bold", width=6)
    table.add_column("Agent", style="cyan")
    table.add_column("Instruction", style="white")

    for step in plan.steps:
        table.add_row(str(step.order), step.agent_slug, step.instruction[:80])
    console.print(table)

    if plan.requires_approval:
        console.print("\n[yellow]⚠ This task requires human approval.[/yellow]")


# ── LLM ──────────────────────────────────────────────────────
@cli.group()
def llm():
    """LLM Gateway operations."""
    pass


@llm.command("providers")
def llm_providers():
    """List all configured LLM providers."""
    from app.llm import get_gateway

    gateway = get_gateway()
    providers = gateway.list_providers()

    console.print(BANNER)
    table = Table(title="LLM Providers", show_header=True)
    table.add_column("Provider", style="bold cyan")
    table.add_column("Default Model", style="green")
    table.add_column("Available", style="yellow")
    table.add_column("Models", style="dim")

    for p in providers:
        table.add_row(
            p["provider"],
            p["default_model"],
            "✅" if p["available"] else "❌",
            ", ".join(p["models"][:4]),
        )
    console.print(table)


@llm.command("chat")
@click.argument("message")
@click.option("--provider", "-p", default="", help="LLM provider")
@click.option("--model", "-m", default="", help="Model name")
def llm_chat(message, provider, model):
    """Chat directly with an LLM."""
    from app.llm import LLMConfig, LLMMessage, get_gateway

    gateway = get_gateway()
    messages = [LLMMessage(role="user", content=message)]
    config = LLMConfig(model=model or None)

    with console.status("[bold cyan]Thinking..."):
        response = asyncio.run(
            gateway.chat(messages=messages, provider=provider or None, config=config)
        )

    console.print(
        Panel(
            response.content,
            title=f"💬 {response.provider}/{response.model}",
            border_style="cyan",
        )
    )
    if response.usage:
        console.print(
            f"[dim]Tokens: {response.usage.get('total_tokens', '?')}[/dim]"
        )


# ── Tools ────────────────────────────────────────────────────
@cli.group()
def tools():
    """Tool calling framework."""
    pass


@tools.command("list")
def tools_list():
    """List all available tools."""
    from app.tools import get_registry

    registry = get_registry()
    tools_data = registry.list_tools()

    console.print(BANNER)
    table = Table(title="Available Tools", show_header=True)
    table.add_column("Name", style="bold cyan")
    table.add_column("Category", style="green")
    table.add_column("Enabled", style="yellow")
    table.add_column("Description", style="white")

    for t in tools_data:
        table.add_row(
            t["name"],
            t["category"],
            "✅" if t["enabled"] else "❌",
            t["description"][:60],
        )
    console.print(table)


@tools.command("exec")
@click.argument("tool_name")
@click.argument("arguments", required=False, default="{}")
def tools_exec(tool_name, arguments):
    """Execute a tool. Arguments as JSON string."""
    from app.tools import get_registry

    try:
        args = json.loads(arguments)
    except json.JSONDecodeError:
        console.print(f"[red]Invalid JSON arguments: {arguments}[/red]")
        sys.exit(1)

    registry = get_registry()
    with console.status(f"[bold cyan]Executing {tool_name}..."):
        result = asyncio.run(registry.execute(tool_name, **args))

    if result.success:
        console.print(
            Panel(
                result.output[:3000],
                title=f"✅ {tool_name} Output",
                border_style="green",
            )
        )
    else:
        console.print(f"[red]❌ {result.error}[/red]")


# ── Server ───────────────────────────────────────────────────
@cli.command()
@click.option("--host", "-h", default="0.0.0.0", help="Host")
@click.option("--port", "-p", default=8000, help="Port")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def serve(host, port, reload):
    """Start the Zarix AgentOS API server."""
    console.print(BANNER)
    console.print(
        f"[bold green]🚀 Starting Zarix AgentOS API on {host}:{port}[/bold green]\n"
    )
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
    )


# ── Info ─────────────────────────────────────────────────────
@cli.command()
def info():
    """Show system information."""
    from app.core.config import settings
    from app.agents import AGENT_REGISTRY
    from app.llm import get_gateway
    from app.tools import get_registry

    console.print(BANNER)

    gateway = get_gateway()
    registry = get_registry()

    table = Table(title="System Information", show_header=True)
    table.add_column("Property", style="bold cyan")
    table.add_column("Value", style="white")
    table.add_row("Version", "1.0.0")
    table.add_row("Environment", settings.app_env)
    table.add_row("Agents", str(len(AGENT_REGISTRY)))
    table.add_row("LLM Providers", str(len(gateway.list_providers())))
    table.add_row("Tools", str(len(registry.list_tools())))
    table.add_row("Default LLM", f"{settings.default_llm_provider}/{settings.default_llm_model}")
    console.print(table)


if __name__ == "__main__":
    cli()
