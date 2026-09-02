# Generated manually for the MIRROR MVP.
from django.conf import settings
import django.db.models.deletion
import uuid
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('authority_scope', models.JSONField(blank=True, default=list)),
                ('status', models.CharField(choices=[('ACTIVE','Active'),('PAUSED','Paused'),('STOPPED','Stopped'),('REVOKED','Revoked')], default='ACTIVE', max_length=16)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agents', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='mirror.agent')),
            ],
        ),
        migrations.CreateModel(
            name='IntentContract',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('version', models.PositiveIntegerField(default=1)),
                ('goal', models.TextField()),
                ('constraints', models.JSONField(blank=True, default=dict)),
                ('allowed_actions', models.JSONField(blank=True, default=list)),
                ('approval_required_actions', models.JSONField(blank=True, default=list)),
                ('denied_actions', models.JSONField(blank=True, default=list)),
                ('data_scope', models.JSONField(blank=True, default=list)),
                ('status', models.CharField(choices=[('DRAFT','Draft'),('ACTIVE','Active'),('PAUSED','Paused'),('REVOKED','Revoked'),('EXPIRED','Expired')], default='DRAFT', max_length=16)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intent_contracts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField()),
                ('origin', models.URLField(blank=True, max_length=500)),
                ('risk_level', models.CharField(choices=[('LOW','Low'),('MEDIUM','Medium'),('HIGH','High'),('CRITICAL','Critical')], default='LOW', max_length=16)),
                ('read_only', models.BooleanField(default=True)),
                ('side_effect', models.BooleanField(default=False)),
                ('financial', models.BooleanField(default=False)),
                ('reversible', models.BooleanField(default=True)),
                ('requires_approval', models.BooleanField(default=False)),
                ('input_schema', models.JSONField(blank=True, default=dict)),
                ('annotations', models.JSONField(blank=True, default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(max_length=128)),
                ('decision', models.CharField(choices=[('ALLOW','Allow'),('APPROVAL_REQUIRED','Approval required'),('DENY','Deny')], max_length=32)),
                ('risk_level', models.CharField(default='LOW', max_length=16)),
                ('data_scope', models.JSONField(blank=True, default=list)),
                ('conditions', models.JSONField(blank=True, default=dict)),
                ('intent_contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='policies', to='mirror.intentcontract')),
            ],
        ),
        migrations.CreateModel(
            name='ToolCall',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('decision', models.CharField(choices=[('ALLOW','Allow'),('APPROVAL_REQUIRED','Approval required'),('DENY','Deny')], max_length=32)),
                ('risk_level', models.CharField(default='LOW', max_length=16)),
                ('drift_score', models.FloatField(default=0.0)),
                ('reason_codes', models.JSONField(blank=True, default=list)),
                ('explanation', models.TextField(blank=True)),
                ('result_status', models.CharField(choices=[('PENDING','Pending'),('SUCCESS','Success'),('FAILED','Failed'),('BLOCKED','Blocked')], default='PENDING', max_length=16)),
                ('result_summary', models.JSONField(blank=True, default=dict)),
                ('input_payload', models.JSONField(blank=True, default=dict)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tool_calls', to='mirror.agent')),
                ('intent_contract', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tool_calls', to='mirror.intentcontract')),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tool_calls', to='mirror.tool')),
            ],
        ),
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('PENDING','Pending'),('APPROVED','Approved'),('DENIED','Denied'),('EXPIRED','Expired'),('USED','Used')], default='PENDING', max_length=16)),
                ('scope', models.JSONField(blank=True, default=dict)),
                ('one_time', models.BooleanField(default=True)),
                ('expires_at', models.DateTimeField()),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('used_at', models.DateTimeField(blank=True, null=True)),
                ('tool_call', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='approval', to='mirror.toolcall')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approvals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event_type', models.CharField(max_length=64)),
                ('actor_type', models.CharField(default='SYSTEM', max_length=32)),
                ('actor_id', models.CharField(blank=True, max_length=128)),
                ('details', models.JSONField(blank=True, default=dict)),
                ('tool_call', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit_events', to='mirror.toolcall')),
            ],
        ),
        migrations.AddConstraint(
            model_name='policy',
            constraint=models.UniqueConstraint(fields=('intent_contract','action'), name='uniq_contract_action'),
        ),
        migrations.AddIndex(model_name='intentcontract', index=models.Index(fields=['user','status'], name='mirror_inten_user_id_9e3fe9_idx')),
        migrations.AddIndex(model_name='intentcontract', index=models.Index(fields=['expires_at'], name='mirror_inten_expires_5d69dc_idx')),
        migrations.AddIndex(model_name='toolcall', index=models.Index(fields=['created_at'], name='mirror_tool_created_7d6b89_idx')),
        migrations.AddIndex(model_name='toolcall', index=models.Index(fields=['decision'], name='mirror_tool_decisio_445af8_idx')),
        migrations.AddIndex(model_name='toolcall', index=models.Index(fields=['agent','created_at'], name='mirror_tool_agent_i_f189f5_idx')),
        migrations.AddIndex(model_name='auditlog', index=models.Index(fields=['created_at'], name='mirror_audi_created_d4f0cf_idx')),
        migrations.AddIndex(model_name='auditlog', index=models.Index(fields=['event_type'], name='mirror_audi_event_t_7c0c66_idx')),
    ]
