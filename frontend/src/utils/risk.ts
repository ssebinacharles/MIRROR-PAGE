import type { Risk } from '@/types/models';
export const riskWeight: Record<Risk, number> = { LOW: 0.15, MEDIUM: 0.35, HIGH: 0.65, CRITICAL: 0.9 };
export function driftLabel(score: number) { if (score < 0.21) return 'LOW'; if (score < 0.51) return 'MODERATE'; if (score < 0.76) return 'HIGH'; return 'CRITICAL'; }
