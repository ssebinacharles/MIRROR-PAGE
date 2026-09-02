export type Decision = 'ALLOW' | 'APPROVAL_REQUIRED' | 'DENY';
export type Risk = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export type IntentContract = {
  id: string;
  version: number;
  goal: string;
  constraints: Record<string, unknown>;
  allowed_actions: string[];
  approval_required_actions: string[];
  denied_actions: string[];
  data_scope: string[];
  status: 'DRAFT' | 'ACTIVE' | 'PAUSED' | 'REVOKED' | 'EXPIRED';
  expires_at: string | null;
  created_at: string;
  updated_at: string;
};

export type Tool = {
  id: string;
  name: string;
  title: string;
  description: string;
  origin: string;
  risk_level: Risk;
  read_only: boolean;
  side_effect: boolean;
  financial: boolean;
  reversible: boolean;
  requires_approval: boolean;
  input_schema: Record<string, unknown>;
  annotations: Record<string, unknown>;
};

export type Agent = {
  id: string;
  name: string;
  parent: string | null;
  authority_scope: string[];
  status: 'ACTIVE' | 'PAUSED' | 'STOPPED' | 'REVOKED';
  created_at: string;
  updated_at: string;
};

export type ToolCall = {
  id: string;
  tool: string;
  tool_name: string;
  agent: string;
  agent_name: string;
  intent_contract: string;
  input_payload: Record<string, unknown>;
  decision: Decision;
  risk_level: Risk;
  drift_score: number;
  reason_codes: string[];
  explanation: string;
  result_status: 'PENDING' | 'SUCCESS' | 'FAILED' | 'BLOCKED';
  result_summary: Record<string, unknown>;
  created_at: string;
  updated_at: string;
};

export type Approval = {
  id: string;
  tool_call: string;
  tool_name: string;
  user: number;
  status: 'PENDING' | 'APPROVED' | 'DENIED' | 'EXPIRED' | 'USED';
  scope: Record<string, unknown>;
  one_time: boolean;
  expires_at: string;
  approved_at: string | null;
  used_at: string | null;
};

export type AuditEvent = {
  id: string;
  event_type: string;
  actor_type: string;
  actor_id: string;
  tool_call: string | null;
  details: Record<string, unknown>;
  created_at: string;
};

export type EvaluationResponse = {
  decision: {
    decision: Decision;
    risk_level: Risk;
    drift_score: number;
    reason_codes: string[];
    explanation: string;
    required_approval: boolean;
  };
  tool_call: ToolCall;
  approval: Approval | null;
};
