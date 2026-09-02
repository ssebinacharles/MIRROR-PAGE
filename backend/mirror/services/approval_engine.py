from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from mirror.models import Approval, ToolCall
from mirror.services.audit_service import record_event

@transaction.atomic
def create_approval(tool_call: ToolCall, user, ttl_minutes=10):
    approval, _ = Approval.objects.get_or_create(
        tool_call=tool_call,
        defaults={
            'user': user,
            'scope': {
                'tool': tool_call.tool.name,
                'input_hash_basis': tool_call.input_payload,
                'intent_contract': str(tool_call.intent_contract_id),
            },
            'one_time': True,
            'expires_at': timezone.now() + timedelta(minutes=ttl_minutes),
        },
    )
    record_event('APPROVAL_REQUESTED', actor_type='SYSTEM', tool_call=tool_call, details={'approval_id': str(approval.id)})
    return approval

def approve(approval: Approval):
    if approval.status != 'PENDING':
        raise ValueError('Approval is no longer pending.')
    if approval.expires_at <= timezone.now():
        approval.status = 'EXPIRED'
        approval.save(update_fields=['status','updated_at'])
        raise ValueError('Approval has expired.')
    approval.status = 'APPROVED'
    approval.approved_at = timezone.now()
    approval.save(update_fields=['status','approved_at','updated_at'])
    record_event('APPROVAL_GRANTED', actor_type='USER', actor_id=str(approval.user_id), tool_call=approval.tool_call, details={'approval_id': str(approval.id)})
    return approval

def deny(approval: Approval):
    if approval.status != 'PENDING':
        raise ValueError('Approval is no longer pending.')
    approval.status = 'DENIED'
    approval.save(update_fields=['status','updated_at'])
    record_event('APPROVAL_DENIED', actor_type='USER', actor_id=str(approval.user_id), tool_call=approval.tool_call, details={'approval_id': str(approval.id)})
    return approval

def consume(approval: Approval):
    if approval.status != 'APPROVED':
        raise ValueError('Approval is not usable.')
    if approval.expires_at <= timezone.now():
        approval.status = 'EXPIRED'
        approval.save(update_fields=['status','updated_at'])
        raise ValueError('Approval has expired.')
    if approval.one_time:
        approval.status = 'USED'
        approval.used_at = timezone.now()
        approval.save(update_fields=['status','used_at','updated_at'])
    return approval
