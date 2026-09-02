import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { RiskIndicator } from '@/components/security/RiskIndicator';

describe('RiskIndicator', () => {
  it('renders risk level', () => {
    render(<RiskIndicator risk="CRITICAL" />);
    expect(screen.getByText('CRITICAL')).toBeInTheDocument();
  });
});
