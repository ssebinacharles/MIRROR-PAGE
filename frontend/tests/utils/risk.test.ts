import { describe, expect, it } from 'vitest';
import { driftLabel, riskWeight } from '@/utils/risk';

describe('driftLabel', () => {
  it('classifies boundary values correctly', () => {
    expect(driftLabel(0)).toBe('LOW');
    expect(driftLabel(0.2)).toBe('LOW');
    expect(driftLabel(0.21)).toBe('MODERATE');
    expect(driftLabel(0.5)).toBe('MODERATE');
    expect(driftLabel(0.51)).toBe('HIGH');
    expect(driftLabel(0.75)).toBe('HIGH');
    expect(driftLabel(0.76)).toBe('CRITICAL');
    expect(driftLabel(1)).toBe('CRITICAL');
  });
});

describe('riskWeight', () => {
  it('keeps risk weights monotonically increasing', () => {
    expect(riskWeight.LOW).toBeLessThan(riskWeight.MEDIUM);
    expect(riskWeight.MEDIUM).toBeLessThan(riskWeight.HIGH);
    expect(riskWeight.HIGH).toBeLessThan(riskWeight.CRITICAL);
  });
});
