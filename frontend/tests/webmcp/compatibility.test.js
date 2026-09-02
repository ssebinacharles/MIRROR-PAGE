import { describe, expect, it } from 'vitest';
import { webmcpSupported } from '@/webmcp/compatibility';
describe('webmcpSupported', () => {
    it('returns false when modelContext is unavailable', () => {
        expect(webmcpSupported()).toBe(false);
    });
    it('returns true when modelContext exists', () => {
        const documentWithModelContext = document;
        documentWithModelContext.modelContext = {};
        expect(webmcpSupported()).toBe(true);
        delete documentWithModelContext.modelContext;
    });
});
