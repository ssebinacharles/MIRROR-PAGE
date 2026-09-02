from typing import Any
from mirror.models import AuditLog

def record_event(event_type: str, actor_type='SYSTEM', actor_id='', tool_call=None, details: dict[str, Any] | None = None):
    return AuditLog.objects.create(
        event_type=event_type,
        actor_type=actor_type,
        actor_id=str(actor_id),
        tool_call=tool_call,
        details=details or {},
    )
