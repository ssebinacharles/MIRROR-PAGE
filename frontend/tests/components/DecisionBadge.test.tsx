import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import { DecisionBadge } from '@/components/security/DecisionBadge';

describe('DecisionBadge', () => {
  it('renders ALLOW', () => {
    render(<DecisionBadge decision="ALLOW" />);
    expect(screen.getByText('ALLOW')).toBeInTheDocument();
  });

  it('renders readable APPROVAL_REQUIRED text', () => {
    render(<DecisionBadge decision="APPROVAL_REQUIRED" />);
    expect(screen.getByText('APPROVAL REQUIRED')).toBeInTheDocument();
  });

  it('renders DENY', () => {
    render(<DecisionBadge decision="DENY" />);
    expect(screen.getByText('DENY')).toBeInTheDocument();
  });
});
