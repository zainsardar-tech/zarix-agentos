<div align="center">

<img src="https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/radar.svg" width="56" height="56" alt="Zarix AgentOS" />

# Zarix AgentOS

### The Autonomous AI Workforce Operating System for Modern Enterprises

**Open-source AI Workforce OS** — Deploy intelligent AI employees that collaborate, build, automate and operate your digital business.

[![License: MIT](https://img.shields.io/badge/License-MIT-0a0a0a?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](https://opensource.org/licenses/MIT)
[![GitHub Repo](https://img.shields.io/badge/GitHub-zarix--agentos-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/zainsardar-tech/zarix-agentos)
[![Made with Python](https://img.shields.io/badge/Python-FastAPI-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-00C896?style=for-the-badge)](https://github.com/zainsardar-tech/zarix-agentos/pulls)

<p>
  <a href="#vision">Vision</a> •
  <a href="#ai-digital-workforce">AI Workforce</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#platform-features">Features</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#system-design-documentation">System Design</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#contributing">Contributing</a>
</p>

</div>

---

> **Zarix AgentOS** is an open-source Agentic AI platform that replaces traditional agency workflows by providing a complete AI workforce — capable of handling software development, business operations, automation, analysis, and enterprise tasks.

---

## Vision

Build an **open-source Agentic AI platform** that can replace traditional agency workflows by providing a complete AI workforce capable of handling software development, business operations, automation, analysis, and enterprise tasks.

### Mission

- Create a **universal AI agent ecosystem** where companies can deploy specialized AI employees.
- **Automate workflows** currently handled by large technology agencies and outsourced teams.
- Enable **humans to manage AI teams** instead of managing repetitive operational tasks.

---

## Product Positioning

| | |
|---|---|
| **Category** | Agentic AI Operating System |
| **Target Users** | Startups · Enterprise Companies · Software Agencies · Developers · Product Teams · Business Owners |
| **Core Message** | A complete AI workforce platform that combines AI employees, automation, engineering, business intelligence, and enterprise operations. |

---

## AI Digital Workforce

A **multi-agent system** where every agent behaves like an expert employee — with memory, skills, tools, and collaboration ability.

### Engineering Department

| Agent | Skills |
|-------|--------|
| **AI CTO Agent** | System Architecture · Technology Decisions · Scalability Planning · Code Review |
| **Full Stack Engineer Agent** | React · Next.js · Node.js · Python · FastAPI · Django · APIs |
| **DevOps Agent** | AWS · Docker · Kubernetes · CI/CD · Cloud Deployment |
| **QA Engineer Agent** | Testing · Automation Testing · Bug Detection · Security Testing |

### Business Department

| Agent | Skills |
|-------|--------|
| **Business Analyst Agent** | Requirements Gathering · Process Analysis · Business Optimization |
| **Product Manager Agent** | Roadmaps · Feature Planning · User Research |
| **Marketing Agent** | Content · SEO · Campaigns · Growth Strategy |
| **Sales Agent** | Lead Generation · CRM · Personalized Outreach |

### Creative Department

| Agent | Skills |
|-------|--------|
| **UI/UX Designer Agent** | Design Systems · Wireframes · User Experience |
| **Content Creator Agent** | Blogs · Documentation · Social Media |

### Enterprise Department

| Agent | Skills |
|-------|--------|
| **ERP Consultant Agent** | Odoo · SAP · Dynamics · Business Automation |
| **Data Analyst Agent** | Dashboards · Analytics · Business Intelligence |
| **Cyber Security Agent** | Threat Analysis · Security Audit · Compliance |

---

## Supported LLM Providers

Zarix AgentOS includes a **unified LLM Gateway** that connects to 6 major LLM providers through a single interface. Every agent can be configured to use any provider and model.

| Provider | Models | Use Case |
|----------|--------|----------|
| **OpenAI** | GPT-5.5 · GPT-4.1 · Codex models | General intelligence · Code generation |
| **Anthropic** | Claude Opus · Claude Sonnet · Claude Code | Deep reasoning · Long-context analysis |
| **Google** | Gemini (Pro / Flash) | Multimodal · Fast inference |
| **Meta** | Llama (70B / 405B / 8B) | Open-source · Self-hostable |
| **Mistral** | Mistral Large · Codestral | European compliance · Code |
| **DeepSeek** | DeepSeek Coder · DeepSeek Reasoner | Coding · Mathematical reasoning |

### LLM Gateway Features

- **Unified API** — one interface for all 6 providers
- **Provider fallback** — automatically fall back to alternate providers on failure
- **Streaming support** — token-by-token streaming for all providers
- **Model aliasing** — use friendly names like `claude-sonnet` or `deepseek-coder`
- **Per-agent configuration** — each agent can use a different provider/model
- **Usage tracking** — token usage reported for every call

```python
from app.llm import get_gateway, LLMMessage

gateway = get_gateway()

# Chat with any provider
response = await gateway.chat(
    messages=[LLMMessage(role="user", content="Hello!")],
    provider="anthropic",
    model="claude-sonnet",
    fallback=["openai", "mistral"],  # auto-fallback
)

# Stream tokens
async for token in gateway.stream(
    messages=[LLMMessage(role="user", content="Write a poem")],
    provider="openai",
    model="gpt-4.1",
):
    print(token, end="")
```

---

## Platform Features

```
┌─────────────────────────────────────────────────────────────┐
│                    ZARIX AGENTOS PLATFORM                   │
├──────────────────┬──────────────────┬────────────────────────┤
│  Multi-Agent     │  Agent Memory    │  Long-Term Knowledge   │
│  Orchestration   │  System          │  Storage               │
├──────────────────┼──────────────────┼────────────────────────┤
│  Tool Calling    │  Human Approval  │  Agent Collaboration   │
│  Framework       │  Workflows       │                        │
├──────────────────┼──────────────────┼────────────────────────┤
│  Task Planning   │  Real-Time       │  AI Employee           │
│  Engine          │  Execution Logs  │  Marketplace           │
├──────────────────┼──────────────────┼────────────────────────┤
│  Plugin          │  Enterprise RBAC │  Multi-Tenant SaaS      │
│  Architecture    │                  │                        │
└──────────────────┴──────────────────┴────────────────────────┘
```

- **Multi-agent orchestration** — coordinate teams of specialized AI employees
- **Agent memory system** — short-term context and long-term recall
- **Long-term knowledge storage** — persistent organizational intelligence
- **Tool calling framework** — agents invoke real APIs, services, and code
- **Human approval workflows** — keep humans in the loop for critical decisions
- **Agent collaboration** — agents delegate, review, and build on each other's work
- **Task planning engine** — decompose complex goals into executable steps
- **Real-time execution logs** — full transparency into agent actions
- **AI employee marketplace** — discover and deploy pre-built agents
- **Plugin architecture** — extend the platform with custom capabilities
- **Enterprise RBAC** — role-based access control for teams and tenants
- **Multi-tenant SaaS** — isolated workspaces for every organization

---

## Architecture

Zarix AgentOS is built on a modern, scalable, cloud-native stack.

### Frontend
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat&logo=tailwindcss&logoColor=white)
![shadcn/ui](https://img.shields.io/badge/shadcn/ui-000000?style=flat&logo=shadcnui&logoColor=white)

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat&logo=nodedotjs&logoColor=white)

### AI Layer
![LLM Gateway](https://img.shields.io/badge/LLM_Gateway-8B5CF6?style=flat)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat)
![Agent Memory](https://img.shields.io/badge/Agent_Memory-F59E0B?style=flat)
![RAG Pipeline](https://img.shields.io/badge/RAG_Pipeline-10B981?style=flat)
![Vector DB](https://img.shields.io/badge/Vector_DB-EF4444?style=flat)

### Database
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)
![Vector DB](https://img.shields.io/badge/Vector_DB-7C3AED?style=flat)

### Infrastructure
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat&logo=kubernetes&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-FF9900?style=flat&logo=amazonaws&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI/CD-2088FF?style=flat&logo=githubactions&logoColor=white)

```
┌──────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js + React)                    │
│                  Tailwind CSS · shadcn/ui · Real-time Logs            │
└───────────────────────────────┬──────────────────────────────────────┘
                                │  REST / WebSocket
┌───────────────────────────────▼──────────────────────────────────────┐
│                    BACKEND (FastAPI + Node.js)                       │
│            Orchestration · RBAC · Task Planning · Workflows          │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                          AI LAYER                                     │
│   LLM Gateway · LangGraph · Agent Memory · RAG Pipeline · Vector DB  │
└───────────────────────────────┬──────────────────────────────────────┘
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                       DATA & INFRASTRUCTURE                          │
│        PostgreSQL · Redis · Vector DB · Docker · Kubernetes · AWS    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## How It Works

A single natural-language request triggers an entire AI workforce to collaborate end-to-end.

### Workflow Example

> **User Request:** *"Build me an ecommerce SaaS platform"*

| Step | Agent | Action |
|------|-------|--------|
| 1 | **CTO Agent** | Creates the system architecture |
| 2 | **Product Agent** | Creates the product roadmap |
| 3 | **Designer Agent** | Creates the UI/UX plan |
| 4 | **Developer Agent** | Writes the application code |
| 5 | **QA Agent** | Tests the complete system |
| 6 | **DevOps Agent** | Deploys the application |

```
                         ┌─────────────────────────────────────────┐
                         │            👤  USER REQUEST              │
                         │   "Build me an ecommerce SaaS platform" │
                         └────────────────────┬────────────────────┘
                                              │
                                              ▼
   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
   │  🏛️  CTO     │─────▶│  📋 PRODUCT  │─────▶│  🎨 DESIGNER │─────▶│  💻 DEVELOPER│
   │              │      │              │      │              │      │              │
   │   System     │      │   Product    │      │   UI/UX      │      │ Application   │
   │ Architecture │      │   Roadmap    │      │    Plan      │      │    Code       │
   └──────────────┘      └──────────────┘      └──────────────┘      └──────┬───────┘
                                                                          │
                                                                          ▼
   ┌──────────────┐      ┌──────────────┐                                 │
   │  🚀 DEVOPS   │◀─────│   🧪 QA      │◀────────────────────────────────┘
   │              │      │              │
   │  Deployment  │      │    Tests &   │
   │              │      │  Validation  │
   └──────┬───────┘      └──────────────┘
          │
          ▼
                         ┌─────────────────────────────────────────┐
                         │              ✅  DEPLOYED                │
                         │   Ecommerce SaaS Platform — Live in     │
                         │              Production                 │
                         └─────────────────────────────────────────┘
```

---

## System Design Documentation

Zarix AgentOS includes a complete, professional **system design documentation set** with interactive diagrams (rendered natively on GitHub via Mermaid). Explore the full technical blueprint:

| Document | Description |
|----------|-------------|
| 📐 [System Analysis & Design](./docs/system-analysis-and-design.md) | Requirements, stakeholders, design methodology, system boundaries |
| 🏗️ [System Architecture](./docs/system-architecture.md) | Layered architecture, component & deployment diagrams |
| 🎯 [Use Case Diagram](./docs/use-case-diagram.md) | Actors, use cases, and system interactions |
| 🗄️ [Entity Relationship Diagram](./docs/entity-relationship-diagram.md) | Database schema, entities, and relationships |
| 🔄 [Sequence Diagram](./docs/sequence-diagram.md) | Task execution & approval flow sequences |
| 📊 [Data Flow Diagram](./docs/data-flow-diagram.md) | Data movement across processes (DFD Level 0 & 1) |
| 🧩 [Module Diagram](./docs/module-diagram.md) | Code module structure and dependencies |
| 📅 [Gantt Chart](./docs/gantt-chart.md) | Project roadmap, milestones, and timeline |

> 📑 **[View Full Documentation Index →](./docs/README.md)**

---

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) `>= 18`
- [Python](https://www.python.org/) `>= 3.11`
- [Docker](https://www.docker.com/) & Docker Compose
- [PostgreSQL](https://www.postgresql.org/) `>= 15`
- [Redis](https://redis.io/)

### 1. Clone the Repository

```bash
git clone https://github.com/zainsardar-tech/zarix-agentos.git
cd zarix-agentos
```

### 2. Environment Setup

```bash
cp .env.example .env
# Configure your LLM API keys, database URLs, and secrets
```

### 3. Run with Docker (Recommended)

```bash
docker-compose up -d
```

### 4. Run the Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 5. Run the Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` to access the Zarix AgentOS dashboard.

---

## Project Structure

```
zarix-agentos/
├── frontend/                  # Next.js 15 + React + Tailwind CSS
│   ├── app/                   #   Pages & layout
│   │   ├── layout.tsx
│   │   ├── page.tsx           #   Dashboard UI
│   │   └── globals.css
│   ├── lib/
│   │   └── api.ts             #   API client + WebSocket
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.js
│   └── tsconfig.json
├── backend/                   # FastAPI + Celery
│   ├── app/
│   │   ├── main.py            #   FastAPI entry point
│   │   ├── cli.py             #   zarix CLI tool
│   │   ├── core/              #   Config · Database · Celery
│   │   ├── models/            #   SQLAlchemy ORM models
│   │   ├── llm/               #   LLM Gateway (6 providers)
│   │   │   ├── base.py        #     Base provider interface
│   │   │   ├── gateway.py     #     Unified gateway + fallback
│   │   │   ├── openai_provider.py
│   │   │   ├── anthropic_provider.py
│   │   │   ├── google_provider.py
│   │   │   ├── meta_provider.py
│   │   │   ├── mistral_provider.py
│   │   │   └── deepseek_provider.py
│   │   ├── agents/            #   14 AI employee definitions
│   │   │   ├── base.py        #     BaseAgent class
│   │   │   ├── engineering.py #     CTO · Full Stack · DevOps · QA
│   │   │   ├── business.py    #     Analyst · Product · Marketing · Sales
│   │   │   ├── creative.py    #     UI/UX · Content Creator
│   │   │   ├── enterprise.py  #     ERP · Data Analyst · Cyber Security
│   │   │   └── registry.py    #     Agent registry
│   │   ├── orchestration/     #   Multi-agent orchestration
│   │   │   ├── planner.py     #     Task decomposition
│   │   │   ├── orchestrator.py#     Step execution + collaboration
│   │   │   └── tasks.py       #     Celery background tasks
│   │   ├── memory/            #   Agent memory system
│   │   │   ├── short_term.py  #     Volatile conversation buffer
│   │   │   ├── long_term.py   #     ChromaDB vector store
│   │   │   └── manager.py     #     Unified memory manager
│   │   ├── tools/             #   Tool calling framework
│   │   │   ├── base.py        #     BaseTool interface
│   │   │   ├── code_tool.py   #     Python code execution
│   │   │   ├── web_tool.py    #     Web search + fetch
│   │   │   ├── file_tool.py   #     File read/write/list
│   │   │   ├── shell_tool.py  #     Shell execution
│   │   │   └── registry.py    #     Tool registry
│   │   └── api/routes/        #   REST + WebSocket endpoints
│   │       ├── agents.py
│   │       ├── tasks.py
│   │       ├── llm.py
│   │       ├── tools.py
│   │       └── ws.py
│   ├── Dockerfile
│   ├── setup.py               #   CLI entry point (zarix)
│   └── requirements.txt
├── infra/
│   └── k8s/                   #   Kubernetes manifests
│       └── deployment.yaml
├── .github/workflows/
│   └── ci-cd.yml              #   GitHub Actions CI/CD
├── .env.example
├── .gitignore
├── docker-compose.yml         #   Full stack: postgres · redis · chroma · backend · worker · frontend
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## Open Source Strategy

| | |
|---|---|
| **License** | MIT — fully open source |
| **Community Focus** | Developers · AI Researchers · Companies building AI workers |
| **Future Roadmap** | Agent Marketplace · Enterprise Edition · Hosted Cloud Version |

Zarix AgentOS is committed to building in the open. We welcome contributors, AI researchers, and companies who want to shape the future of autonomous enterprise software.

---

## Contributing

We welcome contributions! Whether it's a bug fix, a new agent, a feature, or documentation — every contribution makes Zarix AgentOS better.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a PR.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Connect & Follow

<div align="center">

**Built by [Zain Sardar](https://github.com/zainsardar-tech)**

**GitHub Repository:** [zainsardar-tech/zarix-agentos](https://github.com/zainsardar-tech/zarix-agentos)

If this project helps you, please consider giving it a **star** on GitHub — it helps others discover it!

</div>

---

<div align="center">

### The Future of Work is Autonomous

> *Zarix AgentOS — where AI employees don't just assist, they **operate** your business.*

**[Back to Top](#zarix-agentos)**

</div>
