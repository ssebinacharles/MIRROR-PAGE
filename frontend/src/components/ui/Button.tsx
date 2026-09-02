import type { ButtonHTMLAttributes, ReactNode } from 'react';
export function Button({ children, variant='default', ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'default'|'danger'|'ghost' }): ReactNode { return <button className={`button button-${variant}`} {...props}>{children}</button>; }
