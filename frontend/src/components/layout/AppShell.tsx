import type { ReactNode } from 'react';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';
export function AppShell({ children }: { children: ReactNode }) { return <div className="app-shell"><Sidebar/><div className="main"><TopBar/><main className="content">{children}</main></div></div>; }
