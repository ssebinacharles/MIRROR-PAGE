import { Circle } from 'lucide-react';
import { useApp } from '@/app/providers';
import { useWebMCP } from '@/hooks/useWebMCP';
export function TopBar() { const { backendOnline }=useApp(); const {supported, registered}=useWebMCP(); return <header className="topbar"><div className="topbar-left"><span className="page-context">Control plane</span></div><div className="topbar-right"><span className="connection"><Circle size={7} fill="currentColor"/> {backendOnline ? 'Backend connected' : 'Demo mode'}</span><span className={`connection ${supported && registered ? 'good' : ''}`}><Circle size={7} fill="currentColor"/> {supported && registered ? 'WebMCP ready' : 'WebMCP unavailable'}</span></div></header>; }
