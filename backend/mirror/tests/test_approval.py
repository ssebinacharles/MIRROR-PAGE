from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from mirror.models import IntentContract, Agent, Tool, ToolCall, Approval
from mirror.services.approval_engine import create_approval, approve, consume
from mirror.services.tool_catalog import ensure_builtin_tools

class ApprovalTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='approval')
        ensure_builtin_tools()
        intent = IntentContract.objects.create(user=user, goal='Research', status='ACTIVE', expires_at=timezone.now()+timedelta(hours=1))
        agent = Agent.objects.create(owner=user,name='A',authority_scope=['add_to_cart'])
        tool = Tool.objects.get(name='add_to_cart')
        self.call = ToolCall.objects.create(tool=tool,agent=agent,intent_contract=intent,decision='APPROVAL_REQUIRED',risk_level='MEDIUM')
        self.approval = create_approval(self.call,user,ttl_minutes=10)

    def test_one_time_approval_consumes(self):
        approve(self.approval)
        consume(self.approval)
        self.approval.refresh_from_db()
        self.assertEqual(self.approval.status,'USED')
