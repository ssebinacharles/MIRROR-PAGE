import { describe, expect, it } from 'vitest';
import { setDemoIntent, useIntentStore } from '@/state/intentStore';

const original = useIntentStore((state) => state.intent);

describe('intentStore', () => {
  it('exposes the active intent', () => {
    expect(useIntentStore((state) => state.intent).status).toBe('ACTIVE');
  });

  it('allows replacing the demo intent', () => {
    const updated = { ...original, goal: 'Test intent' };
    setDemoIntent(updated);
    expect(useIntentStore((state) => state.intent).goal).toBe('Test intent');
    setDemoIntent(original);
  });
});
