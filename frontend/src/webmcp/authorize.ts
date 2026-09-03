import { api } from "@/services/api";

import type {
  MirrorAuthorizationResult,
  MirrorToolInput,
} from "./types";

const EXECUTION_CONTEXT_KEY = "mirror.executionContext";

type ExecutionContext = {
  intentId: string;
  agentId: string;
};

export function setExecutionContext(
  context: ExecutionContext,
): void {
  sessionStorage.setItem(
    EXECUTION_CONTEXT_KEY,
    JSON.stringify(context),
  );
}

export function clearExecutionContext(): void {
  sessionStorage.removeItem(EXECUTION_CONTEXT_KEY);
}

function getExecutionContext(): ExecutionContext | null {
  const params = new URLSearchParams(
    window.location.search,
  );

  const urlIntent = params.get("intent");
  const urlAgent = params.get("agent");

  // URL values remain useful for debugging and override
  // the automatically discovered context.
  if (urlIntent && urlAgent) {
    return {
      intentId: urlIntent,
      agentId: urlAgent,
    };
  }

  const stored = sessionStorage.getItem(
    EXECUTION_CONTEXT_KEY,
  );

  if (!stored) {
    return null;
  }

  try {
    const parsed = JSON.parse(stored) as Partial<ExecutionContext>;

    if (
      typeof parsed.intentId === "string" &&
      typeof parsed.agentId === "string"
    ) {
      return {
        intentId: parsed.intentId,
        agentId: parsed.agentId,
      };
    }
  } catch {
    sessionStorage.removeItem(EXECUTION_CONTEXT_KEY);
  }

  return null;
}

export async function authorizeTool(
  toolName: string,
  input: MirrorToolInput,
): Promise<MirrorAuthorizationResult> {
  const context = getExecutionContext();

  if (!context) {
    return {
      decision: "DENY",
      risk_level: "CRITICAL",
      drift_score: 1,
      reason_codes: [
        "MISSING_EXECUTION_CONTEXT",
      ],
      explanation:
        "No active MIRROR intent or agent context was provided.",
    };
  }

  try {
    const result = await api.evaluateAction({
      intent_contract_id: context.intentId,
      tool_name: toolName,
      agent_id: context.agentId,
      input_payload: input,
      execute: false,
    });

    // Tell the UI that the authorization state changed.
    window.dispatchEvent(
      new CustomEvent("mirror:decision"),
    );

    return result.decision;
  } catch (error) {
    console.error(
      "[MIRROR] Authorization request failed:",
      error,
    );

    return {
      decision: "DENY",
      risk_level: "CRITICAL",
      drift_score: 1,
      reason_codes: [
        "AUTHORIZATION_SERVICE_ERROR",
      ],
      explanation:
        "MIRROR could not reach the authorization service.",
    };
  }
}