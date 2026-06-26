// ============================================================
//  Zarix AgentOS — API Client
// ============================================================

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws";

// ── Types ──────────────────────────────────────────────────
export interface Agent {
  slug: string;
  name: string;
  department: string;
  role: string;
  description: string;
  icon: string;
  skills: string[];
  tools: string[];
  llm_provider: string;
  llm_model: string;
  temperature: number;
  max_tokens: number;
}

export interface LLMProvider {
  provider: string;
  default_model: string;
  models: string[];
  available: boolean;
}

export interface Tool {
  name: string;
  description: string;
  category: string;
  enabled: boolean;
}

export interface TaskResult {
  goal: string;
  success: boolean;
  final_output: string;
  error: string | null;
  steps: StepResult[];
}

export interface StepResult {
  order: number;
  agent_slug: string;
  success: boolean;
  content: string;
  error: string | null;
}

// ── API helpers ─────────────────────────────────────────────
async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const error = await res.text();
    throw new Error(`API Error ${res.status}: ${error}`);
  }
  return res.json();
}

// ── Agents ──────────────────────────────────────────────────
export async function getAgents(): Promise<{ agents: Agent[]; total: number }> {
  return apiFetch("/api/agents/");
}

export async function getAgentDepartments(): Promise<{
  departments: Record<string, Agent[]>;
}> {
  return apiFetch("/api/agents/departments");
}

export async function runAgent(
  agentSlug: string,
  instruction: string
): Promise<{ success: boolean; content: string; error: string | null }> {
  return apiFetch("/api/agents/run", {
    method: "POST",
    body: JSON.stringify({ agent_slug: agentSlug, instruction }),
  });
}

// ── Tasks ──────────────────────────────────────────────────
export async function createTask(
  goal: string,
  runAsync = false
): Promise<TaskResult | { task_id: string; status: string }> {
  return apiFetch("/api/tasks/", {
    method: "POST",
    body: JSON.stringify({ goal, run_async: runAsync }),
  });
}

export async function planTask(goal: string): Promise<{
  goal: string;
  requires_approval: boolean;
  steps: { order: number; agent_slug: string; instruction: string }[];
}> {
  return apiFetch("/api/tasks/plan", {
    method: "POST",
    body: JSON.stringify({ goal }),
  });
}

// ── LLM ────────────────────────────────────────────────────
export async function getLLMProviders(): Promise<{ providers: LLMProvider[] }> {
  return apiFetch("/api/llm/providers");
}

export async function getLLMModels(): Promise<{ models: Record<string, string[]> }> {
  return apiFetch("/api/llm/models");
}

export async function llmChat(
  message: string,
  provider?: string,
  model?: string
): Promise<{ content: string; provider: string; model: string; usage: any }> {
  return apiFetch("/api/llm/chat", {
    method: "POST",
    body: JSON.stringify({ message, provider: provider || "", model: model || "" }),
  });
}

// ── Tools ──────────────────────────────────────────────────
export async function getTools(): Promise<{ tools: Tool[] }> {
  return apiFetch("/api/tools/");
}

export async function executeTool(
  toolName: string,
  args: Record<string, any>
): Promise<{ success: boolean; output: string; error: string | null }> {
  return apiFetch("/api/tools/execute", {
    method: "POST",
    body: JSON.stringify({ tool_name: toolName, arguments: args }),
  });
}

// ── WebSocket ──────────────────────────────────────────────
export function connectOrchestration(
  goal: string,
  onProgress: (data: any) => void,
  onComplete: (result: any) => void,
  onError: (error: string) => void
): WebSocket {
  const ws = new WebSocket(`${WS_URL}/orchestrate`);

  ws.onopen = () => {
    ws.send(JSON.stringify({ goal }));
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "progress") {
      onProgress(data);
    } else if (data.type === "complete") {
      onComplete(data.result);
      ws.close();
    } else if (data.error) {
      onError(data.error);
      ws.close();
    }
  };

  ws.onerror = () => {
    onError("WebSocket connection error");
    ws.close();
  };

  return ws;
}

export function streamAgent(
  agentSlug: string,
  instruction: string,
  onToken: (token: string) => void,
  onDone: () => void,
  onError: (error: string) => void
): WebSocket {
  const ws = new WebSocket(`${WS_URL}/stream`);

  ws.onopen = () => {
    ws.send(JSON.stringify({ agent_slug: agentSlug, instruction }));
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "token") {
      onToken(data.content);
    } else if (data.type === "done") {
      onDone();
      ws.close();
    } else if (data.error) {
      onError(data.error);
      ws.close();
    }
  };

  ws.onerror = () => {
    onError("WebSocket connection error");
    ws.close();
  };

  return ws;
}
