import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()

class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class IntentContract(TimeStampedModel):
    STATUS_CHOICES = [('DRAFT','Draft'),('ACTIVE','Active'),('PAUSED','Paused'),('REVOKED','Revoked'),('EXPIRED','Expired')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='intent_contracts')
    version = models.PositiveIntegerField(default=1)
    goal = models.TextField()
    constraints = models.JSONField(default=dict, blank=True)
    allowed_actions = models.JSONField(default=list, blank=True)
    approval_required_actions = models.JSONField(default=list, blank=True)
    denied_actions = models.JSONField(default=list, blank=True)
    data_scope = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='DRAFT')
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=['user','status']), models.Index(fields=['expires_at'])]

    def is_active(self):
        if self.status != 'ACTIVE':
            return False
        if self.expires_at and self.expires_at <= timezone.now():
            return False
        return True

class Policy(TimeStampedModel):
    DECISIONS = [('ALLOW','Allow'),('APPROVAL_REQUIRED','Approval required'),('DENY','Deny')]
    intent_contract = models.ForeignKey(IntentContract, on_delete=models.CASCADE, related_name='policies')
    action = models.CharField(max_length=128)
    decision = models.CharField(max_length=32, choices=DECISIONS)
    risk_level = models.CharField(max_length=16, default='LOW')
    data_scope = models.JSONField(default=list, blank=True)
    conditions = models.JSONField(default=dict, blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['intent_contract','action'], name='uniq_contract_action')]

class Tool(TimeStampedModel):
    RISK = [('LOW','Low'),('MEDIUM','Medium'),('HIGH','High'),('CRITICAL','Critical')]
    name = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    origin = models.URLField(max_length=500, blank=True)
    risk_level = models.CharField(max_length=16, choices=RISK, default='LOW')
    read_only = models.BooleanField(default=True)
    side_effect = models.BooleanField(default=False)
    financial = models.BooleanField(default=False)
    reversible = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    input_schema = models.JSONField(default=dict, blank=True)
    annotations = models.JSONField(default=dict, blank=True)

class Agent(TimeStampedModel):
    STATUS = [('ACTIVE','Active'),('PAUSED','Paused'),('STOPPED','Stopped'),('REVOKED','Revoked')]
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agents')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    authority_scope = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=16, choices=STATUS, default='ACTIVE')

class ToolCall(TimeStampedModel):
    DECISIONS = [('ALLOW','Allow'),('APPROVAL_REQUIRED','Approval required'),('DENY','Deny')]
    RESULT = [('PENDING','Pending'),('SUCCESS','Success'),('FAILED','Failed'),('BLOCKED','Blocked')]
    tool = models.ForeignKey(Tool, on_delete=models.PROTECT, related_name='tool_calls')
    agent = models.ForeignKey(Agent, on_delete=models.PROTECT, related_name='tool_calls')
    intent_contract = models.ForeignKey(IntentContract, on_delete=models.PROTECT, related_name='tool_calls')
    input_payload = models.JSONField(default=dict, blank=True)
    decision = models.CharField(max_length=32, choices=DECISIONS)
    risk_level = models.CharField(max_length=16, default='LOW')
    drift_score = models.FloatField(default=0.0)
    reason_codes = models.JSONField(default=list, blank=True)
    explanation = models.TextField(blank=True)
    result_status = models.CharField(max_length=16, choices=RESULT, default='PENDING')
    result_summary = models.JSONField(default=dict, blank=True)

    class Meta:
        indexes = [models.Index(fields=['created_at']), models.Index(fields=['decision']), models.Index(fields=['agent','created_at'])]

class Approval(TimeStampedModel):
    STATUS = [('PENDING','Pending'),('APPROVED','Approved'),('DENIED','Denied'),('EXPIRED','Expired'),('USED','Used')]
    tool_call = models.OneToOneField(ToolCall, on_delete=models.CASCADE, related_name='approval')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approvals')
    status = models.CharField(max_length=16, choices=STATUS, default='PENDING')
    scope = models.JSONField(default=dict, blank=True)
    one_time = models.BooleanField(default=True)
    expires_at = models.DateTimeField()
    approved_at = models.DateTimeField(null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)

class AuditLog(TimeStampedModel):
    event_type = models.CharField(max_length=64)
    actor_type = models.CharField(max_length=32, default='SYSTEM')
    actor_id = models.CharField(max_length=128, blank=True)
    tool_call = models.ForeignKey(ToolCall, null=True, blank=True, on_delete=models.SET_NULL, related_name='audit_events')
    details = models.JSONField(default=dict, blank=True)
    class Meta:
        indexes = [models.Index(fields=['created_at']), models.Index(fields=['event_type'])]
