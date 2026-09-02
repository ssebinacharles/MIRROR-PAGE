from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class DriftResult:
    score: float
    reasons: list[str]

WEIGHTS = {
    'goal_mismatch': 0.20,
    'scope_mismatch': 0.25,
    'data_sensitivity': 0.15,
    'financial_risk': 0.15,
    'side_effect_risk': 0.10,
    'irreversibility': 0.10,
    'privilege_escalation': 0.05,
}

def calculate_drift(intent, tool, input_data: dict[str, Any], agent) -> DriftResult:
    reasons = []
    score = 0.0
    allowed = set(intent.allowed_actions)
    denied = set(intent.denied_actions)
    approval = set(intent.approval_required_actions)

    if tool.name in denied:
        score += WEIGHTS['scope_mismatch']
        reasons.append('EXPLICITLY_DENIED')
    elif allowed and tool.name not in allowed and tool.name not in approval:
        score += WEIGHTS['scope_mismatch']
        reasons.append('OUTSIDE_SCOPE')

    if tool.financial:
        score += WEIGHTS['financial_risk']
        reasons.append('FINANCIAL_SIDE_EFFECT')
    if tool.side_effect:
        score += WEIGHTS['side_effect_risk']
        reasons.append('SIDE_EFFECT')
    if not tool.reversible:
        score += WEIGHTS['irreversibility']
        reasons.append('IRREVERSIBLE_ACTION')

    scope = set(intent.data_scope)
    required = set((tool.annotations or {}).get('dataScope', []))
    if required and not required.issubset(scope):
        score += WEIGHTS['data_sensitivity']
        reasons.append('SENSITIVE_DATA')

    authority = set(agent.authority_scope)
    if authority and tool.name not in authority:
        score += WEIGHTS['privilege_escalation']
        reasons.append('PRIVILEGE_ESCALATION')

    # A simple semantic keyword check for the demo. This is deliberately heuristic.
    goal_text = intent.goal.lower()
    action_text = tool.name.lower().replace('_', ' ')
    if 'research' in goal_text and any(x in action_text for x in ('purchase', 'submit', 'send', 'book')):
        score += WEIGHTS['goal_mismatch']
        reasons.append('GOAL_MISMATCH')

    return DriftResult(min(round(score, 2), 1.0), sorted(set(reasons)))
