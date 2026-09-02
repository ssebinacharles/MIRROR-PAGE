from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from mirror.models import IntentContract, Agent
from mirror.services.tool_catalog import ensure_builtin_tools
from django.utils import timezone
from datetime import timedelta

class ApiTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='api')
        ensure_builtin_tools()
        self.intent = IntentContract.objects.create(
            user=self.user, goal='Research laptops only', allowed_actions=['search_products'], denied_actions=['purchase_product'],
            status='ACTIVE', expires_at=timezone.now()+timedelta(hours=1), data_scope=['public_product_information']
        )
        self.agent = Agent.objects.create(owner=self.user, name='ApiAgent', authority_scope=['search_products'])

    def test_health(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'],'ok')

    def test_evaluate(self):
        response = self.client.post('/api/policies/evaluate/', {
            'intent_contract_id': str(self.intent.id),
            'tool_name':'search_products',
            'agent_id': str(self.agent.id),
            'input_payload': {'query':'laptop'},
            'execute': True,
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['decision']['decision'],'ALLOW')
