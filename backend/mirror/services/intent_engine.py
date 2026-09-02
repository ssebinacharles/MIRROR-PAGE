from django.utils import timezone
from mirror.models import IntentContract


def activate_contract(contract: IntentContract) -> IntentContract:
    if contract.expires_at and contract.expires_at <= timezone.now():
        raise ValueError('Cannot activate an expired intent contract.')
    contract.status = 'ACTIVE'
    contract.save(update_fields=['status', 'updated_at'])
    return contract


def revoke_contract(contract: IntentContract) -> IntentContract:
    contract.status = 'REVOKED'
    contract.save(update_fields=['status', 'updated_at'])
    return contract


def expire_if_needed(contract: IntentContract) -> bool:
    if contract.status == 'ACTIVE' and contract.expires_at and contract.expires_at <= timezone.now():
        contract.status = 'EXPIRED'
        contract.save(update_fields=['status', 'updated_at'])
        return True
    return False
