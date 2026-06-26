<div align="center">

# 5⃣ Sequence Diagram

### Zarix AgentOS - Customer Order / Task Execution Sequence

</div>

---

## 1. Overview

This document illustrates the **end-to-end sequence of interactions** when a user submits a task (e.g., *"Build me an ecommerce SaaS platform"*) and the AI workforce collaborates to deliver it. It shows the temporal ordering of messages between all participating components.

---

## 2. Primary Scenario - Full Task Execution

```mermaid
sequenceDiagram
  autonumber
  actor U as  User
  participant FE as Frontend
  participant API as FastAPI Gateway
  participant DB as PostgreSQL
  participant ORCH as Orchestrator
  participant PLN as Task Planner
  participant CTO as  CTO Agent
  participant PM as  Product Agent
  participant DES as  Designer Agent
  participant DEV as  Developer Agent
  participant QA as  QA Agent
  participant OPS as  DevOps Agent
  participant LLM as LLM Gateway
  participant TOOLS as Tool Framework
  participant MEM as Memory System

  U->>FE: Submit task: "Build ecommerce SaaS"
  FE->>API: POST /tasks (WebSocket upgrade)
  API->>DB: Create Task (status: pending)
  API->>ORCH: Trigger orchestration
  ORCH->>PLN: Decompose task
  PLN->>LLM: Generate task plan
  LLM-->>PLN: Return 6-step plan
  PLN-->>ORCH: Return plan

  Note over ORCH,OPS: Sequential Agent Execution

  rect rgb(219, 234, 254)
  Note right of CTO: Step 1 - Architecture
  ORCH->>CTO: Assign: design architecture
  CTO->>MEM: Retrieve relevant memory
  MEM-->>CTO: Return context
  CTO->>LLM: Generate architecture
  LLM-->>CTO: Stream architecture spec
  CTO-->>ORCH: Return architecture
  ORCH->>API: Stream progress (WS)
  API-->>FE: Push log
  FE-->>U: Display: "Architecture complete"
  end

  rect rgb(237, 233, 254)
  Note right of PM: Step 2 - Roadmap
  ORCH->>PM: Assign: create roadmap
  PM->>LLM: Generate product roadmap
  LLM-->>PM: Return roadmap
  PM-->>ORCH: Return roadmap
  ORCH->>API: Stream progress (WS)
  API-->>FE: Push log
  FE-->>U: Display: "Roadmap complete"
  end

  rect rgb(220, 252, 231)
  Note right of DES: Step 3 - UI/UX Plan
  ORCH->>DES: Assign: design UI/UX
  DES->>LLM: Generate design plan
  LLM-->>DES: Return design system
  DES-->>ORCH: Return UI plan
  ORCH->>API: Stream progress (WS)
  API-->>FE: Push log
  FE-->>U: Display: "UI plan complete"
  end

  rect rgb(254, 243, 199)
  Note right of DEV: Step 4 - Code
  ORCH->>DEV: Assign: write application code
  DEV->>TOOLS: Execute code_tool
  TOOLS-->>DEV: Return code output
  DEV->>LLM: Generate/refine code
  LLM-->>DEV: Return code
  DEV-->>ORCH: Return codebase
  ORCH->>API: Stream progress (WS)
  API-->>FE: Push log
  FE-->>U: Display: "Code complete"
  end

  rect rgb(252, 231, 243)
  Note right of QA: Step 5 - Testing
  ORCH->>QA: Assign: test the system
  QA->>TOOLS: Execute shell_tool (run tests)
  TOOLS-->>QA: Return test results
  QA->>LLM: Analyze test output
  LLM-->>QA: Return test report
  QA-->>ORCH: Return validation
  ORCH->>API: Stream progress (WS)
  API-->>FE: Push log
  FE-->>U: Display: "Tests passed"
  end

  rect rgb(254, 226, 226)
  Note right of OPS: Step 6 - Deployment
  ORCH->>OPS: Assign: deploy application
  OPS->>TOOLS: Execute shell_tool (deploy)
  TOOLS-->>OPS: Return deployment status
  OPS-->>ORCH: Return deployment URL
  ORCH->>API: Stream progress (WS)
  API-->>FE: Push log
  FE-->>U: Display: "Deployed "
  end

  ORCH->>DB: Update Task (status: completed, result)
  API-->>FE: Send final result
  FE-->>U: Display complete result
  U->>U:  Ecommerce SaaS deployed
```

---

## 3. Alternative Scenario - Human Approval Required

When an agent attempts a **critical action** (e.g., production deployment, destructive operation), the system pauses for human approval.

```mermaid
sequenceDiagram
  autonumber
  actor U as  User
  participant FE as Frontend
  participant API as FastAPI
  participant ORCH as Orchestrator
  participant OPS as  DevOps Agent
  participant TOOLS as Tool Framework

  ORCH->>OPS: Assign: deploy to production
  OPS->>TOOLS: Request: shell_tool (deploy prod)
  TOOLS->>API: Flag as critical action
  API->>DB: Create ApprovalRequest (status: pending)
  API-->>FE: Push approval request (WS)
  FE-->>U: Display: "Approval required: deploy to prod?"

  alt User Approves
  U->>FE: Click "Approve"
  FE->>API: POST /approvals/{id}/approve
  API->>DB: Update ApprovalRequest (status: approved)
  API->>ORCH: Resume execution
  ORCH->>OPS: Proceed with deployment
  OPS->>TOOLS: Execute deploy
  TOOLS-->>OPS: Return success
  OPS-->>ORCH: Return deployment URL
  else User Rejects
  U->>FE: Click "Reject"
  FE->>API: POST /approvals/{id}/reject
  API->>DB: Update ApprovalRequest (status: rejected)
  API->>ORCH: Halt execution
  ORCH->>ORCH: Mark step as blocked
  ORCH-->>API: Stream: "Deployment rejected"
  API-->>FE: Push notification
  FE-->>U: Display: "Deployment rejected by user"
  end
```

---

## 4. Alternative Scenario - LLM Provider Fallback

When the primary LLM provider fails, the gateway automatically falls back to alternate providers.

```mermaid
sequenceDiagram
  autonumber
  participant A as Agent
  participant GW as LLM Gateway
  participant P1 as OpenAI
  participant P2 as Anthropic
  participant P3 as Mistral

  A->>GW: chat(provider: openai, fallback: [anthropic, mistral])
  GW->>P1: Send request
  P1--xGW: Error: 503 Service Unavailable

  Note over GW: Primary failed - trying fallback 1
  GW->>P2: Send request (fallback)
  P2--xGW: Error: 429 Rate Limited

  Note over GW: Fallback 1 failed - trying fallback 2
  GW->>P3: Send request (fallback)
  P3-->>GW: Success: response tokens
  GW-->>A: Return response (from mistral)
  GW->>GW: Log: provider=openai failed, used=mistral
```

---

## 5. Message Flow Summary

| Step | From | To | Message | Purpose |
|------|------|----|---------|---------|
| 1 | User | Frontend | Submit task | Initiate workflow |
| 2 | Frontend | API | POST /tasks | Create task record |
| 3 | API | Orchestrator | Trigger | Begin orchestration |
| 4 | Orchestrator | Planner | Decompose | Break into steps |
| 5-10 | Orchestrator | Agents | Assign steps | Sequential execution |
| 11 | Agents | LLM Gateway | Generate | AI inference |
| 12 | Agents | Tools | Execute | Real-world actions |
| 13 | Agents | Memory | Store/Retrieve | Context persistence |
| 14 | Orchestrator | API | Stream logs | Real-time updates |
| 15 | API | Frontend | Push (WS) | Live dashboard |
| 16 | Orchestrator | DB | Update task | Persist final result |

---

## 6. Sequence Design Notes

| Concern | Handling |
|---------|----------|
| **Concurrency** | Steps execute sequentially by default; parallel execution supported for independent steps |
| **Failure** | Failed steps trigger retry with exponential backoff; persistent failures halt the task |
| **Timeouts** | Each LLM call has a configurable timeout; tool executions are sandboxed |
| **Idempotency** | Task IDs are UUIDs; re-submission creates new tasks |
| **Streaming** | WebSocket channels stream token-by-token output for live UX |

---

## 7. Related Documents

| Document | Link |
|----------|------|
| System Analysis & Design | [system-analysis-and-design.md](./system-analysis-and-design.md) |
| System Architecture | [system-architecture.md](./system-architecture.md) |
| Use Case Diagram | [use-case-diagram.md](./use-case-diagram.md) |
| Entity Relationship Diagram | [entity-relationship-diagram.md](./entity-relationship-diagram.md) |
| Data Flow Diagram | [data-flow-diagram.md](./data-flow-diagram.md) |
| Module Diagram | [module-diagram.md](./module-diagram.md) |
| Gantt Chart | [gantt-chart.md](./gantt-chart.md) |

---

<div align="center">

**[ Back to Docs Index](./README.md)** · **[ Back to Top](#)**

</div>
