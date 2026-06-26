"use client";

import { useState, useEffect } from "react";
import {
  Radar,
  Bot,
  BrainCircuit,
  Wrench,
  Building2,
  Rocket,
  Radio,
  CheckCircle2,
  XCircle,
  Cpu,
  Briefcase,
  Palette,
  Compass,
  Code2,
  Cloud,
  Bug,
  BarChart3,
  Map,
  Megaphone,
  Users,
  PenTool,
  TrendingUp,
  ShieldCheck,
  type LucideIcon,
} from "lucide-react";
import {
  getAgents,
  getLLMProviders,
  getTools,
  createTask,
  connectOrchestration,
  type Agent,
  type LLMProvider,
  type Tool,
} from "@/lib/api";

// ── Department config ──────────────────────────────────────────
const DEPT_COLORS: Record<string, string> = {
  engineering: "border-blue-500/30 bg-blue-500/5",
  business: "border-green-500/30 bg-green-500/5",
  creative: "border-purple-500/30 bg-purple-500/5",
  enterprise: "border-orange-500/30 bg-orange-500/5",
};

const DEPT_ICONS: Record<string, LucideIcon> = {
  engineering: Wrench,
  business: Briefcase,
  creative: Palette,
  enterprise: Building2,
};

const DEPT_LABELS: Record<string, string> = {
  engineering: "Engineering",
  business: "Business",
  creative: "Creative",
  enterprise: "Enterprise",
};

// ── Agent icon mapping (slug → lucide icon) ───────────────────
const AGENT_ICONS: Record<string, LucideIcon> = {
  cto_agent: Compass,
  fullstack_engineer_agent: Code2,
  devops_agent: Cloud,
  qa_engineer_agent: Bug,
  business_analyst_agent: BarChart3,
  product_manager_agent: Map,
  marketing_agent: Megaphone,
  sales_agent: Users,
  ui_designer_agent: Palette,
  content_creator_agent: PenTool,
  erp_consultant_agent: Building2,
  data_analyst_agent: TrendingUp,
  cyber_security_agent: ShieldCheck,
};

function getAgentIcon(slug: string): LucideIcon {
  return AGENT_ICONS[slug] ?? Bot;
}

export default function Home() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [providers, setProviders] = useState<LLMProvider[]>([]);
  const [tools, setTools] = useState<Tool[]>([]);
  const [goal, setGoal] = useState("");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState<any[]>([]);
  const [result, setResult] = useState<any>(null);
  const [activeTab, setActiveTab] = useState<"dashboard" | "agents" | "llm" | "tools">("dashboard");

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const [agentsRes, providersRes, toolsRes] = await Promise.all([
        getAgents(),
        getLLMProviders(),
        getTools(),
      ]);
      setAgents(agentsRes.agents);
      setProviders(providersRes.providers);
      setTools(toolsRes.tools);
    } catch (err) {
      console.error("Failed to load data:", err);
    }
  }

  async function handleRunTask() {
    if (!goal.trim()) return;
    setLoading(true);
    setProgress([]);
    setResult(null);

    connectOrchestration(
      goal,
      (data) => {
        setProgress((prev) => [...prev, data]);
      },
      (res) => {
        setResult(res);
        setLoading(false);
      },
      (err) => {
        setResult({ success: false, error: err });
        setLoading(false);
      }
    );
  }

  const stats = [
    { label: "AI Agents", value: agents.length, icon: Bot, color: "text-blue-400" },
    { label: "LLM Providers", value: providers.length, icon: BrainCircuit, color: "text-purple-400" },
    { label: "Tools", value: tools.length, icon: Wrench, color: "text-green-400" },
    { label: "Departments", value: 4, icon: Building2, color: "text-orange-400" },
  ];

  return (
    <div className="min-h-screen bg-neutral-950">
      {/* Header */}
      <header className="border-b border-neutral-800 bg-neutral-900/50 backdrop-blur sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Radar className="w-7 h-7 text-zarix-500" strokeWidth={2} />
            <div>
              <h1 className="text-xl font-bold text-white">Zarix AgentOS</h1>
              <p className="text-xs text-neutral-400">AI Workforce Operating System</p>
            </div>
          </div>
          <nav className="flex gap-1">
            {(["dashboard", "agents", "llm", "tools"] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 rounded-lg text-sm font-medium capitalize transition-colors ${
                  activeTab === tab
                    ? "bg-zarix-600 text-white"
                    : "text-neutral-400 hover:text-white hover:bg-neutral-800"
                }`}
              >
                {tab}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Dashboard Tab */}
        {activeTab === "dashboard" && (
          <div className="space-y-8">
            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {stats.map((s) => {
                const Icon = s.icon;
                return (
                  <div
                    key={s.label}
                    className="bg-neutral-900 border border-neutral-800 rounded-xl p-5"
                  >
                    <Icon className={`w-7 h-7 mb-3 ${s.color}`} strokeWidth={2} />
                    <div className={`text-3xl font-bold ${s.color}`}>{s.value}</div>
                    <div className="text-sm text-neutral-400">{s.label}</div>
                  </div>
                );
              })}
            </div>

            {/* Task Input */}
            <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
              <div className="flex items-center gap-2 mb-1">
                <Rocket className="w-5 h-5 text-zarix-500" strokeWidth={2} />
                <h2 className="text-lg font-bold text-white">Deploy AI Workforce</h2>
              </div>
              <p className="text-sm text-neutral-400 mb-4">
                Describe a goal and the AI workforce will collaborate to complete it.
              </p>
              <div className="flex gap-3">
                <input
                  type="text"
                  value={goal}
                  onChange={(e) => setGoal(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleRunTask()}
                  placeholder="e.g. Build me an ecommerce SaaS platform"
                  className="flex-1 bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-3 text-white placeholder-neutral-500 focus:outline-none focus:border-zarix-500"
                />
                <button
                  onClick={handleRunTask}
                  disabled={loading || !goal.trim()}
                  className="px-6 py-3 bg-zarix-600 hover:bg-zarix-500 disabled:bg-neutral-700 disabled:text-neutral-500 text-white font-medium rounded-lg transition-colors flex items-center gap-2"
                >
                  {loading ? "Working..." : "Deploy"}
                </button>
              </div>
            </div>

            {/* Progress */}
            {progress.length > 0 && (
              <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6">
                <div className="flex items-center gap-2 mb-3">
                  <Radio className="w-4 h-4 text-zarix-500 animate-pulse" strokeWidth={2} />
                  <h3 className="text-sm font-bold text-white">Live Progress</h3>
                </div>
                <div className="space-y-2">
                  {progress.map((p, i) => (
                    <div key={i} className="flex items-center gap-3 text-sm animate-slide-in">
                      <span className="text-neutral-500">{i + 1}.</span>
                      <span className="text-neutral-300">{p.message}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Result */}
            {result && (
              <div
                className={`bg-neutral-900 border rounded-xl p-6 ${
                  result.success ? "border-green-500/30" : "border-red-500/30"
                }`}
              >
                <div className="flex items-center gap-2 mb-3">
                  {result.success ? (
                    <CheckCircle2 className="w-5 h-5 text-green-400" strokeWidth={2} />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-400" strokeWidth={2} />
                  )}
                  <h3 className={`text-sm font-bold ${result.success ? "text-green-400" : "text-red-400"}`}>
                    {result.success ? "Task Complete" : "Task Failed"}
                  </h3>
                </div>
                {result.error ? (
                  <p className="text-red-400 text-sm">{result.error}</p>
                ) : (
                  <pre className="text-sm text-neutral-300 whitespace-pre-wrap max-h-96 overflow-auto">
                    {result.final_output}
                  </pre>
                )}
                {result.steps && (
                  <div className="mt-4 space-y-2">
                    {result.steps.map((step: any, i: number) => {
                      const StepIcon = step.success ? CheckCircle2 : XCircle;
                      return (
                        <div key={i} className="flex items-center gap-2 text-xs text-neutral-400">
                          <StepIcon
                            className={`w-3.5 h-3.5 ${step.success ? "text-green-400" : "text-red-400"}`}
                            strokeWidth={2}
                          />
                          <span className="font-mono">{step.agent_slug}</span>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Agents Tab */}
        {activeTab === "agents" && (
          <div className="space-y-6">
            <div className="flex items-center gap-2">
              <Bot className="w-6 h-6 text-zarix-500" strokeWidth={2} />
              <h2 className="text-xl font-bold text-white">AI Digital Workforce</h2>
            </div>
            {["engineering", "business", "creative", "enterprise"].map((dept) => {
              const deptAgents = agents.filter((a) => a.department === dept);
              if (deptAgents.length === 0) return null;
              const DeptIcon = DEPT_ICONS[dept] ?? Building2;
              return (
                <div key={dept}>
                  <div className="flex items-center gap-2 mb-3">
                    <DeptIcon className="w-4 h-4 text-neutral-400" strokeWidth={2} />
                    <h3 className="text-sm font-bold text-neutral-400 uppercase tracking-wide">
                      {DEPT_LABELS[dept]}
                    </h3>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {deptAgents.map((agent) => {
                      const AgentIcon = getAgentIcon(agent.slug);
                      return (
                        <div
                          key={agent.slug}
                          className={`border rounded-xl p-5 ${DEPT_COLORS[dept]}`}
                        >
                          <div className="flex items-start justify-between mb-2">
                            <AgentIcon className="w-7 h-7 text-neutral-300" strokeWidth={2} />
                            <span className="text-xs px-2 py-1 rounded bg-neutral-800 text-neutral-400">
                              {agent.llm_provider}
                            </span>
                          </div>
                          <h4 className="font-bold text-white">{agent.name}</h4>
                          <p className="text-xs text-neutral-400 mb-3">{agent.role}</p>
                          <p className="text-sm text-neutral-300 mb-3 line-clamp-2">
                            {agent.description}
                          </p>
                          <div className="flex flex-wrap gap-1">
                            {agent.skills.slice(0, 4).map((skill) => (
                              <span
                                key={skill}
                                className="text-xs px-2 py-0.5 rounded bg-neutral-800 text-neutral-300"
                              >
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* LLM Tab */}
        {activeTab === "llm" && (
          <div className="space-y-6">
            <div className="flex items-center gap-2">
              <BrainCircuit className="w-6 h-6 text-zarix-500" strokeWidth={2} />
              <h2 className="text-xl font-bold text-white">LLM Gateway</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {providers.map((p) => (
                <div
                  key={p.provider}
                  className="bg-neutral-900 border border-neutral-800 rounded-xl p-5"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <Cpu className="w-5 h-5 text-neutral-400" strokeWidth={2} />
                      <h4 className="font-bold text-white capitalize">{p.provider}</h4>
                    </div>
                    <span
                      className={`text-xs px-2 py-1 rounded ${
                        p.available ? "bg-green-500/20 text-green-400" : "bg-red-500/20 text-red-400"
                      }`}
                    >
                      {p.available ? "Active" : "No Key"}
                    </span>
                  </div>
                  <p className="text-xs text-neutral-400 mb-2">
                    Default: <span className="text-neutral-200">{p.default_model}</span>
                  </p>
                  <div className="flex flex-wrap gap-1">
                    {p.models.slice(0, 5).map((m) => (
                      <span
                        key={m}
                        className="text-xs px-2 py-0.5 rounded bg-neutral-800 text-neutral-300"
                      >
                        {m}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Tools Tab */}
        {activeTab === "tools" && (
          <div className="space-y-6">
            <div className="flex items-center gap-2">
              <Wrench className="w-6 h-6 text-zarix-500" strokeWidth={2} />
              <h2 className="text-xl font-bold text-white">Tool Calling Framework</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {tools.map((t) => (
                <div
                  key={t.name}
                  className="bg-neutral-900 border border-neutral-800 rounded-xl p-5"
                >
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-bold text-white font-mono text-sm">{t.name}</h4>
                    <span
                      className={`text-xs px-2 py-1 rounded ${
                        t.enabled ? "bg-green-500/20 text-green-400" : "bg-red-500/20 text-red-400"
                      }`}
                    >
                      {t.enabled ? "Enabled" : "Disabled"}
                    </span>
                  </div>
                  <span className="text-xs px-2 py-0.5 rounded bg-zarix-500/20 text-zarix-300 mb-2 inline-block">
                    {t.category}
                  </span>
                  <p className="text-sm text-neutral-400">{t.description}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      <footer className="border-t border-neutral-800 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-6 flex items-center justify-center gap-2 text-sm text-neutral-500">
          <Radar className="w-4 h-4" strokeWidth={2} />
          <span>Zarix AgentOS — The Future of Work is Autonomous</span>
        </div>
      </footer>
    </div>
  );
}
