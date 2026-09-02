import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import type { ReactNode } from 'react';
import { api } from '@/services/api';
import { registerMirrorTools } from '@/webmcp/registry';
import type { Agent, Approval, AuditEvent, IntentContract, Tool, ToolCall } from '@/types/models';

type AppState = {
  intent: IntentContract | null;
  tools: Tool[];
  agents: Agent[];
  calls: ToolCall[];
  approvals: Approval[];
  audit: AuditEvent[];
  loading: boolean;
  backendOnline: boolean;
  refresh: () => Promise<void>;
};

const AppContext = createContext<AppState | null>(null);

export function AppProvider({ children }: { children: ReactNode }) {
  const [intent, setIntent] = useState<IntentContract | null>(null);
  const [tools, setTools] = useState<Tool[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [calls, setCalls] = useState<ToolCall[]>([]);
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [audit, setAudit] = useState<AuditEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [backendOnline, setBackendOnline] = useState(false);
  const demoIntent = null;

  const refresh = async () => {
    setLoading(true);
    const health = await api.health().catch(() => null);
    const online = Boolean(health);
    setBackendOnline(online);
    if (online) {
      const [intents, toolPage, agentPage, callPage, approvalPage, auditPage] = await Promise.all([
        api.listIntents(),
        api.listTools(),
        api.listAgents(),
        api.listToolCalls(),
        api.listApprovals(),
        api.listAudit(),
      ]);
      setIntent(intents.results.find((i) => i.status === 'ACTIVE') ?? intents.results[0] ?? null);
      setTools(toolPage.results);
      setAgents(agentPage.results);
      setCalls(callPage.results);
      setApprovals(approvalPage.results);
      setAudit(auditPage.results);
    } else {
      setIntent(demoIntent);
      setTools([]);
      setAgents([]);
      setCalls([]);
      setApprovals([]);
      setAudit([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    void refresh();
  }, []);

  useEffect(() => {
    void registerMirrorTools();
  }, []);

  const value = useMemo(() => ({
    intent, tools, agents, calls, approvals, audit, loading, backendOnline, refresh,
  }), [intent, tools, agents, calls, approvals, audit, loading, backendOnline]);

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}

export function useApp() {
  const value = useContext(AppContext);
  if (!value) throw new Error('useApp must be used inside AppProvider');
  return value;
}
