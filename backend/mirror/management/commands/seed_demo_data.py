from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from mirror.models import IntentContract, Agent, Policy
from mirror.services.tool_catalog import ensure_builtin_tools

class Command(BaseCommand):
    help = 'Seed deterministic MIRROR demo data.'

    def handle(self, *args, **options):
        User = get_user_model()
        user, _ = User.objects.get_or_create(username='demo', defaults={'email':'demo@mirror.local'})
        if not user.has_usable_password():
            user.set_unusable_password(); user.save()
        ensure_builtin_tools()
        contract, _ = IntentContract.objects.get_or_create(
            user=user,
            goal='Research development laptops under $1,200. Compare them. Do not purchase anything.',
            defaults={
                'constraints': {'max_price': 1200, 'currency':'USD'},
                'allowed_actions': ['search_products','get_product_details','compare_products'],
                'approval_required_actions': ['add_to_cart'],
                'denied_actions': ['purchase_product'],
                'data_scope': ['public_product_information'],
                'status': 'ACTIVE',
                'expires_at': timezone.now() + timedelta(hours=2),
            },
        )
        Agent.objects.get_or_create(
            owner=user,
            name='ResearchAgent',
            defaults={'authority_scope':['search_products','get_product_details','compare_products','add_to_cart']},
        )
        for action, decision, risk in [
            ('search_products','ALLOW','LOW'),
            ('get_product_details','ALLOW','LOW'),
            ('compare_products','ALLOW','LOW'),
            ('add_to_cart','APPROVAL_REQUIRED','MEDIUM'),
            ('purchase_product','DENY','CRITICAL'),
        ]:
            Policy.objects.update_or_create(
                intent_contract=contract,
                action=action,
                defaults={'decision':decision,'risk_level':risk,'data_scope':['public_product_information']},
            )
        self.stdout.write(self.style.SUCCESS('MIRROR demo data seeded.'))
