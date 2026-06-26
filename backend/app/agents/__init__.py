# ============================================================
#  Zarix AgentOS — Agents Package
# ============================================================
#  14 AI employees across 4 departments:
#    Engineering · Business · Creative · Enterprise
# ============================================================
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
from app.agents.registry import (
    AGENT_REGISTRY,
    DEPARTMENTS,
    get_agent,
    get_department_agents,
    list_agents,
    list_agents_by_department,
)

__all__ = [
    "BaseAgent",
    "AgentContext",
    "AgentResult",
    # Engineering
    "CTOAgent",
    "FullStackEngineerAgent",
    "DevOpsAgent",
    "QAEngineerAgent",
    # Business
    "BusinessAnalystAgent",
    "ProductManagerAgent",
    "MarketingAgent",
    "SalesAgent",
    # Creative
    "UIDesignerAgent",
    "ContentCreatorAgent",
    # Enterprise
    "ERPConsultantAgent",
    "DataAnalystAgent",
    "CyberSecurityAgent",
    # Registry
    "AGENT_REGISTRY",
    "DEPARTMENTS",
    "get_agent",
    "get_department_agents",
    "list_agents",
    "list_agents_by_department",
]
