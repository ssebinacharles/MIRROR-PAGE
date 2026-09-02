import { jsx as _jsx } from "react/jsx-runtime";
import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { DriftMeter } from '@/components/security/DriftMeter';
describe('DriftMeter', () => {
    it('renders score and classification', () => {
        render(_jsx(DriftMeter, { score: 0.86 }));
        expect(screen.getByText('86%')).toBeInTheDocument();
        expect(screen.getByText('CRITICAL')).toBeInTheDocument();
    });
    it('sets a proportional meter width', () => {
        const { container } = render(_jsx(DriftMeter, { score: 0.42 }));
        const fill = container.querySelector('.meter-fill');
        expect(fill).toHaveStyle({ width: '42%' });
    });
});
