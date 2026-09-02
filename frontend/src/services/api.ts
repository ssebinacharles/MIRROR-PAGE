import axios from 'axios';
import type { Agent, Approval, AuditEvent, EvaluationResponse, IntentContract, Tool, ToolCall } from '@/types/models';
import type { Paginated } from '@/types/api';

const baseURL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';
export const http = axios.create({ baseURL, timeout: 8000, headers: { 'Content-Type': 'application/json' } });

export const api = {
  health: async () => (await http.get<{ status: string }>('/health/')).data,
  listIntents: async () => (await http.get<Paginated<IntentContract>>('/intents/')).data,
  createIntent: async (payload: Partial<IntentContract>) => (await http.post<IntentContract>('/intents/', payload)).data,
  activateIntent: async (id: string) => (await http.post<IntentContract>(`/intents/${id}/activate/`)).data,
  revokeIntent: async (id: string) => (await http.post<IntentContract>(`/intents/${id}/revoke/`)).data,
  listTools: async () => (await http.get<Paginated<Tool>>('/tools/')).data,
  listAgents: async () => (await http.get<Paginated<Agent>>('/agents/')).data,
  listToolCalls: async () => (await http.get<Paginated<ToolCall>>('/tool-calls/')).data,
  listApprovals: async () => (await http.get<Paginated<Approval>>('/approvals/')).data,
  decideApproval: async (id: string, action: 'approve' | 'deny') => (await http.post<Approval>(`/approvals/${id}/decide/`, { action })).data,
  listAudit: async () => (await http.get<Paginated<AuditEvent>>('/audit/')).data,
  evaluateAction: async (payload: { intent_contract_id: string; tool_name: string; agent_id: string; input_payload?: Record<string, unknown>; execute?: boolean }) =>
    (await http.post<EvaluationResponse>('/policies/evaluate/', payload)).data,
};
