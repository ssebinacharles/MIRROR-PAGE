import type { ReactNode } from 'react';
export function Badge({ children, tone = 'neutral' }: { children: ReactNode; tone?: 'neutral'|'success'|'warning'|'danger'|'info' }) { return <span className={`badge badge-${tone}`}>{children}</span>; }
