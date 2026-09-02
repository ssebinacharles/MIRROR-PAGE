import { Badge } from '@/components/ui/Badge'; import type { Risk } from '@/types/models';
export function RiskIndicator({ risk }: { risk: Risk }) { const tone = risk==='CRITICAL'||risk==='HIGH'?'danger':risk==='MEDIUM'?'warning':'neutral'; return <Badge tone={tone}>{risk}</Badge>; }
