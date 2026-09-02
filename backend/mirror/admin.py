from django.contrib import admin
from .models import IntentContract, Policy, Tool, Agent, ToolCall, Approval, AuditLog

for model in [IntentContract, Policy, Tool, Agent, ToolCall, Approval, AuditLog]:
    admin.site.register(model)
