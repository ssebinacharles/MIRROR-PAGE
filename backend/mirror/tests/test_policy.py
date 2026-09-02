from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from mirror.models import IntentContract, Agent, Tool
from mirror.services.decision_engine import evaluate_action
from mirror.services.tool_catalog import ensure_builtin_tools

class PolicyEngineTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user = User.objects.create_user(username='test')
        ensure_builtin_tools()
        cls.intent = IntentContract.objects.create(
            user=cls.user,
            goal='Research development laptops under $1,200. Do not purchase anything.',
            constraints={'max_price':1200},
            allowed_actions=['search_products','compare_products'],
            approval_required_actions=['add_to_cart'],
            denied_actions=['purchase_product'],
            data_scope=['public_product_information'],
            status='ACTIVE',
            expires_at=timezone.now()+timedelta(hours=1),
        )
        cls.agent = Agent.objects.create(owner=cls.user, name='ResearchAgent', authority_scope=['search_products','compare_products','add_to_cart'])

    def test_search_is_allowed(self):
        tool = Tool.objects.get(name='search_products')
        d = evaluate_action(self.intent, tool, {'query':'laptop'}, self.agent)
        self.assertEqual(d.decision,'ALLOW')

    def test_purchase_is_denied(self):
        tool = Tool.objects.get(name='purchase_product')
        d = evaluate_action(self.intent, tool, {'product_id':'p1'}, self.agent)
        self.assertEqual(d.decision,'DENY')
        self.assertIn('EXPLICITLY_DENIED', d.reason_codes)

    def test_cart_requires_approval(self):
        tool = Tool.objects.get(name='add_to_cart')
        d = evaluate_action(self.intent, tool, {'product_id':'p1'}, self.agent)
        self.assertEqual(d.decision,'APPROVAL_REQUIRED')

    def test_inactive_intent_denies(self):
        self.intent.status='REVOKED'; self.intent.save()
        tool = Tool.objects.get(name='search_products')
        d = evaluate_action(self.intent, tool, {'query':'laptop'}, self.agent)
        self.assertEqual(d.decision,'DENY')

    def test_child_cannot_escalate(self):
        child = Agent.objects.create(owner=self.user, name='Child', parent=self.agent, authority_scope=['purchase_product'])
        tool = Tool.objects.get(name='purchase_product')
        d = evaluate_action(self.intent, tool, {}, child)
        self.assertEqual(d.decision,'DENY')
