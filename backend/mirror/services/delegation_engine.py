from mirror.models import Agent

def can_delegate(parent: Agent, requested: list[str]) -> tuple[bool, list[str]]:
    parent_scope = set(parent.authority_scope)
    requested_set = set(requested)
    allowed = sorted(requested_set & parent_scope)
    return requested_set.issubset(parent_scope), allowed

def effective_authority(agent: Agent) -> set[str]:
    scope = set(agent.authority_scope)
    current = agent.parent
    while current is not None:
        scope &= set(current.authority_scope)
        current = current.parent
    return scope
