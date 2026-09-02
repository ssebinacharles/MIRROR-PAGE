import { describe, expect, it, vi } from 'vitest';
import { pct, timeAgo } from '@/utils/formatting';

describe('pct', () => {
  it('formats drift scores as percentages', () => {
    expect(pct(0)).toBe('0%');
    expect(pct(0.856)).toBe('86%');
    expect(pct(1)).toBe('100%');
  });
});

describe('timeAgo', () => {
  it('formats recent timestamps', () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-09-02T10:00:00Z'));

    expect(timeAgo('2026-09-02T09:59:45Z')).toBe('just now');
    expect(timeAgo('2026-09-02T09:58:00Z')).toBe('2m ago');
    expect(timeAgo('2026-09-02T09:00:00Z')).toBe('1h ago');
    expect(timeAgo('2026-09-01T10:00:00Z')).toBe('1d ago');

    vi.useRealTimers();
  });
});
