import { api } from "@/services/api";

import type {
  MirrorAuthorizationResult,
  MirrorToolInput,
} from "./types";

function getExecutionContext() {
  const params = new URLSearchParams(
    window.location.search,
  );

  return {
    intentId: params.get("intent"),
    agentId: params.get("agent"),
  };
}

export async function authorizeTool(
  toolName: string,
  input: MirrorToolInput,
): Promise<MirrorAuthorizationResult> {
  const { intentId, agentId } =
    getExecutionContext();

  if (!intentId || !agentId) {
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

  const result = await api.evaluateAction({
    intent_contract_id: intentId,
    tool_name: toolName,
    agent_id: agentId,
    input_payload: input,
    execute: false,
  });

  return result.decision;
}