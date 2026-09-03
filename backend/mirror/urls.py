from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AgentViewSet,
    ApprovalViewSet,
    AuditLogViewSet,
    IntentContractViewSet,
    PolicyViewSet,
    ToolCallViewSet,
    ToolViewSet,
    health,
    evaluate_action_api,
)
from .product_views import (
    ProductSearchView,
    ProductDetailView,
)

router = DefaultRouter()
router.register("intents", IntentContractViewSet, basename="intentcontract")
router.register("policies", PolicyViewSet, basename="policy")
router.register("tools", ToolViewSet, basename="tool")
router.register("agents", AgentViewSet, basename="agent")
router.register("tool-calls", ToolCallViewSet, basename="toolcall")
router.register("approvals", ApprovalViewSet, basename="approval")
router.register("audit", AuditLogViewSet, basename="auditlog")

urlpatterns = [
    # Explicit custom endpoints MUST sit above router.urls
    path("health/", health, name="health"),
    path("policies/evaluate/", evaluate_action_api, name="evaluate-action"),
    path("products/search/", ProductSearchView.as_view(), name="product-search"),
    path("products/<uuid:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("", include(router.urls)),
]