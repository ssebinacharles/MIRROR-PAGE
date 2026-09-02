from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    IntentContractViewSet, PolicyViewSet, ToolViewSet, AgentViewSet,
    ToolCallViewSet, ApprovalViewSet, AuditLogViewSet, health, evaluate_action_api,
)

router = DefaultRouter()
router.register('intents', IntentContractViewSet)
router.register('policies', PolicyViewSet)
router.register('tools', ToolViewSet)
router.register('agents', AgentViewSet)
router.register('tool-calls', ToolCallViewSet)
router.register('approvals', ApprovalViewSet)
router.register('audit', AuditLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health),
    path('policies/evaluate/', evaluate_action_api),
]
