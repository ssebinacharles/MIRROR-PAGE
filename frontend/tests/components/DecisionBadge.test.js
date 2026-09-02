import { jsx as _jsx } from "react/jsx-runtime";
import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { DecisionBadge } from '@/components/security/DecisionBadge';
describe('DecisionBadge', () => {
    it('renders ALLOW', () => {
        render(_jsx(DecisionBadge, { decision: "ALLOW" }));
        expect(screen.getByText('ALLOW')).toBeInTheDocument();
    });
    it('renders readable APPROVAL_REQUIRED text', () => {
        render(_jsx(DecisionBadge, { decision: "APPROVAL_REQUIRED" }));
        expect(screen.getByText('APPROVAL REQUIRED')).toBeInTheDocument();
    });
    it('renders DENY', () => {
        render(_jsx(DecisionBadge, { decision: "DENY" }));
        expect(screen.getByText('DENY')).toBeInTheDocument();
    });
});
