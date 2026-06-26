# ============================================================
#  Zarix AgentOS — FastAPI Application Entry Point
# ============================================================
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    # Startup
    if settings.app_debug:
        await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title=settings.app_name,
    description=(
        "The Autonomous AI Workforce Operating System — deploy intelligent AI "
        "employees that collaborate, build, automate and operate your business."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Routers ──────────────────────────────────────────────────
from app.api.routes import agents, llm, tasks, tools, ws  # noqa: E402

app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(llm.router, prefix="/api/llm", tags=["LLM Gateway"])
app.include_router(tools.router, prefix="/api/tools", tags=["Tools"])
app.include_router(ws.router, prefix="/ws", tags=["WebSocket"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy", "env": settings.app_env}
