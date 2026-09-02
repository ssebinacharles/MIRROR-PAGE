from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import (
    IntentContract,
    Policy,
    Tool,
    Agent,
    ToolCall,
    Approval,
    AuditLog,
    Product,
)
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name']

class IntentContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntentContract
        fields = '__all__'
        read_only_fields = ['id','version','created_at','updated_at']

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = '__all__'
        read_only_fields = ['id','created_at','updated_at']

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'
        read_only_fields = ['id','created_at','updated_at']

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'
        read_only_fields = ['id','created_at','updated_at']

class ToolCallSerializer(serializers.ModelSerializer):
    tool_name = serializers.CharField(source='tool.name', read_only=True)
    agent_name = serializers.CharField(source='agent.name', read_only=True)
    class Meta:
        model = ToolCall
        fields = '__all__'
        read_only_fields = ['id','created_at','updated_at']

class ApprovalSerializer(serializers.ModelSerializer):
    tool_name = serializers.CharField(source='tool_call.tool.name', read_only=True)
    class Meta:
        model = Approval
        fields = '__all__'
        read_only_fields = ['id','created_at','updated_at','approved_at','used_at']

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = ['id','created_at','updated_at']

class EvaluateActionSerializer(serializers.Serializer):
    intent_contract_id = serializers.UUIDField()
    tool_name = serializers.CharField(max_length=128)
    agent_id = serializers.UUIDField()
    input_payload = serializers.JSONField(required=False, default=dict)
    execute = serializers.BooleanField(required=False, default=False)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'category',
            'price',
            'currency',
            'specs',
            'available',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
        ]

class ApprovalDecisionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve','deny'])
