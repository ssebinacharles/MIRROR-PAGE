import { Activity, Bot, ClipboardCheck, FileText, LayoutDashboard, LockKeyhole, Shield, TerminalSquare, Wrench } from 'lucide-react';
import { NavLink } from 'react-router-dom';

const items = [
  ['/', 'Overview', LayoutDashboard], ['/intent', 'Intent', FileText], ['/activity', 'Activity', Activity], ['/tools', 'Tools', Wrench],
  ['/approvals', 'Approvals', ClipboardCheck], ['/agents', 'Agents', Bot], ['/audit', 'Audit', TerminalSquare], ['/security', 'Security', Shield], ['/demo', 'Demo Lab', LockKeyhole],
] as const;

export function Sidebar() { return <aside className="sidebar"><div className="brand"><div className="brand-mark">M</div><div><div className="brand-name">MIRROR</div><div className="brand-sub">intent infrastructure</div></div></div><nav>{items.map(([to,label,Icon]) => <NavLink key={to} to={to} className={({isActive}) => `nav-item ${isActive ? 'active' : ''}`}><Icon size={16}/><span>{label}</span></NavLink>)}</nav><div className="sidebar-footer"><div className="mini-label">CONTROL PLANE</div><div className="mono">v0.1 · demo</div></div></aside>; }
