from dataclasses import dataclass
from mirror.models import Agent, IntentContract, Tool
from mirror.services.delegation_engine import effective_authority
from mirror.services.drift_detector import calculate_drift

@dataclass(frozen=True)
class Decision:
    decision: str
    risk_level: str
    drift_score: float
    reason_codes: list[str]
    explanation: str
    required_approval: bool


def evaluate_action(intent: IntentContract, tool: Tool, input_data: dict, agent: Agent) -> Decision:
    if not intent.is_active():
        return Decision('DENY', 'CRITICAL', 1.0, ['EXPIRED_OR_INACTIVE_INTENT'], 'The intent contract is not active.', False)
    if agent.status != 'ACTIVE':
        return Decision('DENY', 'CRITICAL', 1.0, ['AGENT_NOT_AUTHORIZED'], 'The agent is not active.', False)

    authority = effective_authority(agent)
    if authority and tool.name not in authority:
        return Decision('DENY', 'HIGH', 0.8, ['PRIVILEGE_ESCALATION'], 'The agent does not have authority for this tool.', False)

    if tool.name in set(intent.denied_actions):
        drift = calculate_drift(intent, tool, input_data, agent)
        return Decision('DENY', tool.risk_level, max(drift.score, 0.75), sorted(set(drift.reasons + ['EXPLICITLY_DENIED'])), 'The action is explicitly denied by the active intent contract.', False)

    drift = calculate_drift(intent, tool, input_data, agent)
    allowed = set(intent.allowed_actions)
    approval_actions = set(intent.approval_required_actions)

    if allowed and tool.name not in allowed and tool.name not in approval_actions:
        return Decision('DENY', tool.risk_level, max(drift.score, 0.70), sorted(set(drift.reasons + ['OUTSIDE_SCOPE'])), 'The action is outside the active contract scope.', False)

    if tool.requires_approval or tool.name in approval_actions:
        return Decision('APPROVAL_REQUIRED', tool.risk_level, drift.score, drift.reasons, 'This action has consequential side effects and requires explicit human approval.', True)

    if drift.score >= 0.76:
        return Decision('DENY', tool.risk_level, drift.score, drift.reasons, 'Intent drift is too high for automatic execution.', False)

    return Decision('ALLOW', tool.risk_level, drift.score, drift.reasons, 'The action is consistent with the active intent contract.', False)
