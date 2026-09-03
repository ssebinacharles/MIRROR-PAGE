import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import type { ReactNode } from "react";

import { api } from "@/services/api";
import {
  registerMirrorTools,
} from "@/webmcp/registry";

import {
  setExecutionContext,
} from "@/webmcp/authorize";

import type {
  Agent,
  Approval,
  AuditEvent,
  IntentContract,
  Tool,
  ToolCall,
} from "@/types/models";

type AppState = {
  intent: IntentContract | null;
  tools: Tool[];
  agents: Agent[];
  calls: ToolCall[];
  approvals: Approval[];
  audit: AuditEvent[];
  loading: boolean;
  backendOnline: boolean;
  error: string | null;
  refresh: () => Promise<void>;
};

const AppContext = createContext<AppState | null>(null);

function extractResults<T>(response: unknown): T[] {
  if (Array.isArray(response)) {
    return response as T[];
  }

  if (
    response &&
    typeof response === "object" &&
    "results" in response
  ) {
    const results = (response as { results?: unknown }).results;

    return Array.isArray(results) ? (results as T[]) : [];
  }

  return [];
}

export function AppProvider({
  children,
}: {
  children: ReactNode;
}) {
  const [intent, setIntent] =
    useState<IntentContract | null>(null);

  const [tools, setTools] = useState<Tool[]>([]);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [calls, setCalls] = useState<ToolCall[]>([]);
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [audit, setAudit] = useState<AuditEvent[]>([]);

  const [loading, setLoading] = useState(true);
  const [backendOnline, setBackendOnline] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      await api.health();

      setBackendOnline(true);

      const [
        intentsResponse,
        toolsResponse,
        agentsResponse,
        callsResponse,
        approvalsResponse,
        auditResponse,
      ] = await Promise.all([
        api.listIntents(),
        api.listTools(),
        api.listAgents(),
        api.listToolCalls(),
        api.listApprovals(),
        api.listAudit(),
      ]);

      const intentResults =
        extractResults<IntentContract>(intentsResponse);

      const toolResults =
        extractResults<Tool>(toolsResponse);

      const agentResults =
        extractResults<Agent>(agentsResponse);

      const callResults =
        extractResults<ToolCall>(callsResponse);

      const approvalResults =
        extractResults<Approval>(approvalsResponse);

      const auditResults =
        extractResults<AuditEvent>(auditResponse);

      const activeIntent =
        intentResults.find(
          (item) => item.status === "ACTIVE",
        ) ??
        intentResults[0] ??
        null;

      const activeAgent =
        agentResults.find(
          (item) => item.status === "ACTIVE",
        ) ??
        agentResults[0] ??
        null;

      if (activeIntent && activeAgent) {
        setExecutionContext({
          intentId: activeIntent.id,
          agentId: activeAgent.id,
        });
      }

      setIntent(activeIntent);
      setTools(toolResults);
      setAgents(agentResults);
      setCalls(callResults);
      setApprovals(approvalResults);
      setAudit(auditResults);
    } catch (err) {
      console.error(
        "MIRROR backend connection failed:",
        err,
      );

      setBackendOnline(false);

      setError(
        "MIRROR backend is unavailable. Start Django on port 8000.",
      );

      setIntent(null);
      setTools([]);
      setAgents([]);
      setCalls([]);
      setApprovals([]);
      setAudit([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);
  
  useEffect(() => {
  const handleDecision = () => {
    void refresh();
  };

  window.addEventListener(
    "mirror:decision",
    handleDecision,
  );

  return () => {
    window.removeEventListener(
      "mirror:decision",
      handleDecision,
    );
  };
}, [refresh]);

  useEffect(() => {
    void registerMirrorTools().catch((err) => {
      console.error(
        "MIRROR WebMCP registration failed:",
        err,
      );
    });
  }, []);

  const value = useMemo<AppState>(
    () => ({
      intent,
      tools,
      agents,
      calls,
      approvals,
      audit,
      loading,
      backendOnline,
      error,
      refresh,
    }),
    [
      intent,
      tools,
      agents,
      calls,
      approvals,
      audit,
      loading,
      backendOnline,
      error,
      refresh,
    ],
  );

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp(): AppState {
  const value = useContext(AppContext);

  if (!value) {
    throw new Error(
      "useApp must be used inside AppProvider",
    );
  }

  return value;
}