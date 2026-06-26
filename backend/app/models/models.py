# ============================================================
#  Zarix AgentOS — ORM Models
# ============================================================
import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _uuid() -> str:
    return str(uuid.uuid4())


# ── Enums ────────────────────────────────────────────────────
class AgentDepartment(str, enum.Enum):
    ENGINEERING = "engineering"
    BUSINESS = "business"
    CREATIVE = "creative"
    ENTERPRISE = "enterprise"


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class LLMProvider(str, enum.Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    META = "meta"
    MISTRAL = "mistral"
    DEEPSEEK = "deepseek"


# ── Models ────────────────────────────────────────────────────
class Tenant(Base):
    """Multi-tenant organisation."""

    __tablename__ = "tenants"

    id = Column(String, primary_key=True, default=_uuid)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    plan = Column(String(50), default="free")  # free | pro | enterprise
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utcnow)

    users = relationship("User", back_populates="tenant")
    agents = relationship("Agent", back_populates="tenant")
    tasks = relationship("Task", back_populates="tenant")


class User(Base):
    """Platform user (human operator)."""

    __tablename__ = "users"

    id = Column(String, primary_key=True, default=_uuid)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="member")  # admin | manager | member
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utcnow)

    tenant = relationship("Tenant", back_populates="users")
    tasks = relationship("Task", back_populates="user")


class Agent(Base):
    """An AI employee definition."""

    __tablename__ = "agents"

    id = Column(String, primary_key=True, default=_uuid)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False)
    department = Column(Enum(AgentDepartment), nullable=False)
    role = Column(String(255), nullable=False)
    description = Column(Text, default="")
    system_prompt = Column(Text, default="")
    skills = Column(JSON, default=list)  # ["React", "FastAPI", ...]
    tools = Column(JSON, default=list)  # ["code_exec", "web_search", ...]
    llm_provider = Column(Enum(LLMProvider), default=LLMProvider.ANTHROPIC)
    llm_model = Column(String(100), default="claude-sonnet")
    temperature = Column(Float, default=0.2)
    max_tokens = Column(Integer, default=4096)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utcnow)

    tenant = relationship("Tenant", back_populates="agents")
    tasks = relationship("Task", back_populates="agent")


class Task(Base):
    """A unit of work assigned to one or more agents."""

    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=_uuid)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, default="")
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    plan = Column(JSON, default=list)  # decomposed steps
    result = Column(Text, nullable=True)
    requires_approval = Column(Boolean, default=False)
    approved = Column(Boolean, nullable=True)
    parent_task_id = Column(String, ForeignKey("tasks.id"), nullable=True)
    created_at = Column(DateTime, default=_utcnow)
    updated_at = Column(DateTime, default=_utcnow, onupdate=_utcnow)
    completed_at = Column(DateTime, nullable=True)

    tenant = relationship("Tenant", back_populates="tasks")
    user = relationship("User", back_populates="tasks")
    agent = relationship("Agent", back_populates="tasks")
    steps = relationship(
        "TaskStep",
        back_populates="task",
        cascade="all, delete-orphan",
        foreign_keys="TaskStep.task_id",
    )
    logs = relationship(
        "ExecutionLog",
        back_populates="task",
        cascade="all, delete-orphan",
    )


class TaskStep(Base):
    """A single step inside a task plan."""

    __tablename__ = "task_steps"

    id = Column(String, primary_key=True, default=_uuid)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    order = Column(Integer, nullable=False)
    agent_slug = Column(String(100), nullable=False)
    instruction = Column(Text, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_utcnow)
    completed_at = Column(DateTime, nullable=True)

    task = relationship("Task", back_populates="steps", foreign_keys=[task_id])


class ExecutionLog(Base):
    """Real-time execution log entry."""

    __tablename__ = "execution_logs"

    id = Column(String, primary_key=True, default=_uuid)
    task_id = Column(String, ForeignKey("tasks.id"), nullable=False)
    agent_slug = Column(String(100), nullable=True)
    level = Column(String(20), default="INFO")  # INFO | DEBUG | WARN | ERROR
    message = Column(Text, nullable=False)
    data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=_utcnow)

    task = relationship("Task", back_populates="logs")


class Memory(Base):
    """Long-term knowledge / memory store (metadata; vectors in Chroma)."""

    __tablename__ = "memories"

    id = Column(String, primary_key=True, default=_uuid)
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=True)
    agent_slug = Column(String(100), nullable=True)
    memory_type = Column(String(50), default="long_term")  # short_term | long_term
    content = Column(Text, nullable=False)
    metadata_json = Column(JSON, default=dict)
    vector_id = Column(String(255), nullable=True)  # Chroma document id
    created_at = Column(DateTime, default=_utcnow)


class Tool(Base):
    """Registered tool / plugin."""

    __tablename__ = "tools"

    id = Column(String, primary_key=True, default=_uuid)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, default="")
    category = Column(String(50), default="general")  # code | web | file | shell
    config = Column(JSON, default=dict)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utcnow)
