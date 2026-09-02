import { describe, expect, it } from 'vitest';

describe('MIRROR frontend smoke suite', () => {
  it('has a working test environment', () => {
    expect(document).toBeDefined();
    expect(typeof window).toBe('object');
  });
});
