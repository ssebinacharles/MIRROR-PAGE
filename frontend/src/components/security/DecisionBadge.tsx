import { Badge } from '@/components/ui/Badge'; import type { Decision } from '@/types/models';
export function DecisionBadge({ decision }: { decision: Decision }) { const tone = decision==='ALLOW'?'success':decision==='DENY'?'danger':'warning'; return <Badge tone={tone}>{decision.replace('_',' ')}</Badge>; }
