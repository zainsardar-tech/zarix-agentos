# ============================================================
#  Zarix AgentOS — Tasks API Routes
# ============================================================
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.orchestration import Orchestrator, TaskPlanner

router = APIRouter()


class TaskCreateRequest(BaseModel):
    """Request to create and execute a multi-agent task."""

    goal: str
    run_async: bool = False


class TaskPlanRequest(BaseModel):
    """Request to generate a plan without executing."""

    goal: str


@router.post("/")
async def create_task(request: TaskCreateRequest):
    """
    Create and execute a multi-agent task.

    If run_async is true, the task is dispatched to the Celery worker
    and a task id is returned immediately.
    """
    if request.run_async:
        from app.orchestration.tasks import run_task

        task = run_task.delay(request.goal)
        return {
            "task_id": task.id,
            "status": "queued",
            "goal": request.goal,
            "message": "Task dispatched to background worker",
        }

    # Synchronous execution
    orchestrator = Orchestrator()
    result = await orchestrator.execute(goal=request.goal)
    return result.to_dict()


@router.post("/plan")
async def plan_task(request: TaskPlanRequest):
    """Generate an execution plan without running it."""
    planner = TaskPlanner()
    plan = await planner.plan(request.goal)
    return plan.to_dict()


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """Check the status of an async background task."""
    from app.core.celery_app import celery_app

    result = celery_app.AsyncResult(task_id)
    response = {
        "task_id": task_id,
        "status": result.status,
    }
    if result.status == "SUCCESS":
        response["result"] = result.result
    elif result.status == "PROGRESS":
        response["progress"] = result.info
    elif result.status == "FAILURE":
        response["error"] = str(result.info)
    return response
