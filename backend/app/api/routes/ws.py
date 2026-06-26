# ============================================================
#  Zarix AgentOS — WebSocket Routes
# ============================================================
#  Real-time communication for:
#    - Streaming agent output token-by-token
#    - Live orchestration progress updates
# ============================================================
import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.agents import AgentContext, get_agent
from app.orchestration import Orchestrator

router = APIRouter()
logger = logging.getLogger(__name__)


@router.websocket("/stream")
async def ws_stream_agent(websocket: WebSocket):
    """
    Stream a single agent's output token-by-token.

    Client sends JSON: {"agent_slug": "...", "instruction": "..."}
    Server streams back tokens, then a final {"done": true} message.
    """
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        request = json.loads(data)
        agent_slug = request.get("agent_slug", "")
        instruction = request.get("instruction", "")

        agent = get_agent(agent_slug)
        if agent is None:
            await websocket.send_json(
                {"error": f"Agent '{agent_slug}' not found"}
            )
            await websocket.close()
            return

        context = AgentContext(
            task_id="ws_stream",
            task_title=instruction,
            instruction=instruction,
        )

        async for token in agent.stream_run(context):
            await websocket.send_json({"type": "token", "content": token})

        await websocket.send_json({"type": "done", "agent": agent_slug})

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected (stream)")
    except Exception as exc:
        logger.error("WebSocket stream error: %s", exc)
        await websocket.send_json({"error": str(exc)})
    finally:
        await websocket.close()


@router.websocket("/orchestrate")
async def ws_orchestrate(websocket: WebSocket):
    """
    Orchestrate a multi-agent task with live progress updates.

    Client sends JSON: {"goal": "..."}
    Server streams back progress events and the final result.
    """
    await websocket.accept()
    try:
        data = await websocket.receive_text()
        request = json.loads(data)
        goal = request.get("goal", "")

        orchestrator = Orchestrator()

        async def on_progress(event: dict):
            await websocket.send_json({"type": "progress", **event})

        result = await orchestrator.execute(goal=goal, on_progress=on_progress)
        await websocket.send_json(
            {"type": "complete", "result": result.to_dict()}
        )

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected (orchestrate)")
    except Exception as exc:
        logger.error("WebSocket orchestrate error: %s", exc)
        await websocket.send_json({"error": str(exc)})
    finally:
        await websocket.close()
