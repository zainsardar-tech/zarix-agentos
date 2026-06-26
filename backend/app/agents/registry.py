# ============================================================
#  Zarix AgentOS — Agent Registry
# ============================================================
#  Central registry of all 14 AI employees across 4 departments.
#  Provides lookup, listing, and instantiation.
# ============================================================
from __future__ import annotations

from typing import Optional

from app.agents.base import AgentContext, AgentResult, BaseAgent
from app.agents.business import (
    BusinessAnalystAgent,
    MarketingAgent,
    ProductManagerAgent,
    SalesAgent,
)
from app.agents.creative import ContentCreatorAgent, UIDesignerAgent
from app.agents.engineering import (
    CTOAgent,
    DevOpsAgent,
    FullStackEngineerAgent,
    QAEngineerAgent,
)
from app.agents.enterprise import (
    CyberSecurityAgent,
    DataAnalystAgent,
    ERPConsultantAgent,
)

# ── Registry: slug → class ────────────────────────────────────
AGENT_REGISTRY: dict[str, type[BaseAgent]] = {
    # Engineering
    "cto_agent": CTOAgent,
    "fullstack_engineer_agent": FullStackEngineerAgent,
    "devops_agent": DevOpsAgent,
    "qa_engineer_agent": QAEngineerAgent,
    # Business
    "business_analyst_agent": BusinessAnalystAgent,
    "product_manager_agent": ProductManagerAgent,
    "marketing_agent": MarketingAgent,
    "sales_agent": SalesAgent,
    # Creative
    "ui_designer_agent": UIDesignerAgent,
    "content_creator_agent": ContentCreatorAgent,
    # Enterprise
    "erp_consultant_agent": ERPConsultantAgent,
    "data_analyst_agent": DataAnalystAgent,
    "cyber_security_agent": CyberSecurityAgent,
}

# ── Department grouping ──────────────────────────────────────
DEPARTMENTS: dict[str, list[str]] = {
    "engineering": [
        "cto_agent",
        "fullstack_engineer_agent",
        "devops_agent",
        "qa_engineer_agent",
    ],
    "business": [
        "business_analyst_agent",
        "product_manager_agent",
        "marketing_agent",
        "sales_agent",
    ],
    "creative": [
        "ui_designer_agent",
        "content_creator_agent",
    ],
    "enterprise": [
        "erp_consultant_agent",
        "data_analyst_agent",
        "cyber_security_agent",
    ],
}


def get_agent(slug: str) -> Optional[BaseAgent]:
    """Instantiate and return an agent by slug, or None if not found."""
    cls = AGENT_REGISTRY.get(slug)
    if cls is None:
        return None
    return cls()


def list_agents() -> list[dict]:
    """Return metadata for all registered agents."""
    return [cls().to_dict() for cls in AGENT_REGISTRY.values()]


def list_agents_by_department() -> dict[str, list[dict]]:
    """Return agents grouped by department."""
    result: dict[str, list[dict]] = {}
    for dept, slugs in DEPARTMENTS.items():
        result[dept] = []
        for slug in slugs:
            cls = AGENT_REGISTRY.get(slug)
            if cls:
                result[dept].append(cls().to_dict())
    return result


def get_department_agents(department: str) -> list[BaseAgent]:
    """Return instantiated agents for a department."""
    slugs = DEPARTMENTS.get(department, [])
    agents = []
    for slug in slugs:
        agent = get_agent(slug)
        if agent:
            agents.append(agent)
    return agents
