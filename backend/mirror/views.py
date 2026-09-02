from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import (
    IntentContract,
    Policy,
    Tool,
    Agent,
    ToolCall,
    Approval,
    AuditLog,
)

from .serializers import (
    IntentContractSerializer,
    PolicySerializer,
    ToolSerializer,
    AgentSerializer,
    ToolCallSerializer,
    ApprovalSerializer,
    AuditLogSerializer,
    EvaluateActionSerializer,
    ApprovalDecisionSerializer,
)

from .services.approval_engine import (
    create_approval,
    approve as approve_approval,
    deny as deny_approval,
)

from .services.audit_service import record_event
from .services.decision_engine import evaluate_action
from .services.intent_engine import (
    activate_contract,
    revoke_contract,
)
from .services.tool_catalog import ensure_builtin_tools

User = get_user_model()


# ============================================================
# HEALTH
# ============================================================

@api_view(["GET"])
def health(request):
    """
    Lightweight backend health check used by the frontend.
    """
    return Response(
        {
            "status": "ok",
            "service": "mirror-backend",
            "time": timezone.now().isoformat(),
        }
    )


# ============================================================
# INTENT CONTRACTS
# ============================================================

class IntentContractViewSet(viewsets.ModelViewSet):
    queryset = (
        IntentContract.objects
        .select_related("user")
        .all()
        .order_by("-created_at")
    )

    serializer_class = IntentContractSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = User.objects.order_by("id").first()

        if user is None:
            user = User.objects.create_user(
                username="demo",
                email="demo@mirror.local",
            )

        serializer.save(user=user)

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        contract = self.get_object()

        try:
            activate_contract(contract)
        except ValueError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        record_event(
            "INTENT_ACTIVATED",
            actor_type="USER",
            actor_id=str(contract.user_id),
            details={
                "intent_id": str(contract.id),
            },
        )

        return Response(
            self.get_serializer(contract).data
        )

    @action(detail=True, methods=["post"])
    def revoke(self, request, pk=None):
        contract = revoke_contract(
            self.get_object()
        )

        record_event(
            "INTENT_REVOKED",
            actor_type="USER",
            actor_id=str(contract.user_id),
            details={
                "intent_id": str(contract.id),
            },
        )

        return Response(
            self.get_serializer(contract).data
        )


# ============================================================
# POLICIES
# ============================================================

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = (
        Policy.objects
        .select_related("intent_contract")
        .all()
        .order_by("-created_at")
    )

    serializer_class = PolicySerializer
    permission_classes = [AllowAny]


# ============================================================
# TOOLS
# ============================================================

class ToolViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tool.objects.all().order_by("name")

    serializer_class = ToolSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        ensure_builtin_tools()

        return super().list(
            request,
            *args,
            **kwargs,
        )


# ============================================================
# AGENTS
# ============================================================

class AgentViewSet(viewsets.ModelViewSet):
    queryset = (
        Agent.objects
        .select_related("owner", "parent")
        .all()
        .order_by("-created_at")
    )

    serializer_class = AgentSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = User.objects.order_by("id").first()

        if user is None:
            user = User.objects.create_user(
                username="demo",
                email="demo@mirror.local",
            )

        serializer.save(owner=user)


# ============================================================
# TOOL CALLS
# ============================================================

class ToolCallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        ToolCall.objects
        .select_related(
            "tool",
            "agent",
            "intent_contract",
        )
        .all()
        .order_by("-created_at")
    )

    serializer_class = ToolCallSerializer
    permission_classes = [AllowAny]


# ============================================================
# APPROVALS
# ============================================================

class ApprovalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Approval.objects
        .select_related(
            "tool_call__tool",
            "user",
        )
        .all()
        .order_by("-created_at")
    )

    serializer_class = ApprovalSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=["post"])
    def decide(self, request, pk=None):
        approval = self.get_object()

        serializer = ApprovalDecisionSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:
            if (
                serializer.validated_data["action"]
                == "approve"
            ):
                approve_approval(approval)
            else:
                deny_approval(approval)

        except ValueError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            self.get_serializer(approval).data
        )


# ============================================================
# AUDIT LOG
# ============================================================

class AuditLogViewSet(
    viewsets.ReadOnlyModelViewSet
):
    queryset = (
        AuditLog.objects
        .all()
        .order_by("-created_at")
    )

    serializer_class = AuditLogSerializer
    permission_classes = [AllowAny]


# ============================================================
# POLICY EVALUATION
# ============================================================

@api_view(["POST"])
def evaluate_action_api(request):
    """
    Evaluate a WebMCP/agent action against
    the active MIRROR intent and policy.

    This endpoint is the core authorization boundary.
    """

    serializer = EvaluateActionSerializer(
        data=request.data
    )

    serializer.is_valid(
        raise_exception=True
    )

    ensure_builtin_tools()

    try:
        intent = IntentContract.objects.get(
            id=serializer.validated_data[
                "intent_contract_id"
            ]
        )

        tool = Tool.objects.get(
            name=serializer.validated_data[
                "tool_name"
            ]
        )

        agent = Agent.objects.get(
            id=serializer.validated_data[
                "agent_id"
            ]
        )

    except (
        IntentContract.DoesNotExist,
        Tool.DoesNotExist,
        Agent.DoesNotExist,
    ) as exc:

        return Response(
            {
                "error": (
                    f"Not found: "
                    f"{exc.__class__.__name__}"
                )
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    decision = evaluate_action(
        intent,
        tool,
        serializer.validated_data[
            "input_payload"
        ],
        agent,
    )

    with transaction.atomic():

        call = ToolCall.objects.create(
            tool=tool,
            agent=agent,
            intent_contract=intent,
            input_payload=serializer.validated_data[
                "input_payload"
            ],
            decision=decision.decision,
            risk_level=decision.risk_level,
            drift_score=decision.drift_score,
            reason_codes=decision.reason_codes,
            explanation=decision.explanation,
            result_status=(
                "PENDING"
                if decision.decision != "DENY"
                else "BLOCKED"
            ),
        )

        record_event(
            "TOOL_CALL_EVALUATED",
            actor_type="AGENT",
            actor_id=str(agent.id),
            tool_call=call,
            details={
                "decision": decision.decision,
                "drift_score": decision.drift_score,
                "reason_codes": (
                    decision.reason_codes
                ),
            },
        )

        approval = None

        if (
            decision.decision
            == "APPROVAL_REQUIRED"
        ):
            approval = create_approval(
                call,
                intent.user,
            )

        if (
            decision.decision == "ALLOW"
            and serializer.validated_data[
                "execute"
            ]
        ):
            call.result_status = "SUCCESS"

            call.result_summary = {
                "executed": True,
                "demo": True,
            }

            call.save(
                update_fields=[
                    "result_status",
                    "result_summary",
                    "updated_at",
                ]
            )

            record_event(
                "TOOL_CALL_EXECUTED",
                actor_type="AGENT",
                actor_id=str(agent.id),
                tool_call=call,
                details=call.result_summary,
            )

    return Response(
        {
            "tool_call": ToolCallSerializer(
                call
            ).data,

            "decision": {
                "decision": decision.decision,
                "risk_level": decision.risk_level,
                "drift_score": decision.drift_score,
                "reason_codes": (
                    decision.reason_codes
                ),
                "explanation": decision.explanation,
                "required_approval": (
                    decision.required_approval
                ),
            },

            "approval": (
                ApprovalSerializer(
                    approval
                ).data
                if approval
                else None
            ),
        },
        status=status.HTTP_200_OK,
    )