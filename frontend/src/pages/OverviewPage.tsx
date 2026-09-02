import { ArrowUpRight, Ban, CheckCircle2, CircleAlert, RefreshCw } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useApp } from '@/app/providers';
import { Card } from '@/components/ui/Card';
import { SectionHeader } from '@/components/ui/SectionHeader';
import { Stat } from '@/components/ui/Stat';
import { IntentSummary } from '@/components/intent/IntentSummary';
import { AgentTimeline } from '@/components/activity/AgentTimeline';
import { DriftMeter } from '@/components/security/DriftMeter';
import { DecisionBadge } from '@/components/security/DecisionBadge';
import { RiskIndicator } from '@/components/security/RiskIndicator';

export function OverviewPage(){
 const {intent,calls,approvals,agents,backendOnline,refresh}=useApp();
 const allowed=calls.filter(c=>c.decision==='ALLOW').length; const blocked=calls.filter(c=>c.decision==='DENY').length; const pending=approvals.filter(a=>a.status==='PENDING').length; const avg=calls.length?calls.reduce((a,c)=>a+c.drift_score,0)/calls.length:0;
 return <div><SectionHeader eyebrow="CONTROL PLANE" title="Overview" description="Human intent, agent activity and authorization state in one place." action={<button className="icon-button" onClick={()=>void refresh()} title="Refresh"><RefreshCw size={16}/></button>}/>
 <div className="status-strip"><span className={backendOnline?'dot live':'dot'}></span><span>{backendOnline?'Backend connected':'Running in local demo mode'}</span><span className="separator"/> <span>{agents.length||1} agent{(agents.length||1)!==1?'s':''}</span><span className="separator"/><span>{pending} pending approval{pending!==1?'s':''}</span></div>
 <div className="overview-grid"><div className="overview-main"><IntentSummary intent={intent}/><Card><div className="eyebrow">CURRENT POSTURE</div><div className="stats-grid"><Stat label="Actions evaluated" value={calls.length}/><Stat label="Allowed" value={allowed}/><Stat label="Blocked" value={blocked}/><Stat label="Approval queue" value={pending}/></div><div className="posture-foot"><div><div className="small-label">Average drift</div><DriftMeter score={avg}/></div><Link className="text-link" to="/activity">View activity <ArrowUpRight size={14}/></Link></div></Card></div><aside className="overview-side"><Card><div className="eyebrow">DECISION SNAPSHOT</div>{calls.length?calls.slice(0,4).map(c=><div className="decision-line" key={c.id}><div className="decision-icon">{c.decision==='ALLOW'?<CheckCircle2 size={15}/>:c.decision==='DENY'?<Ban size={15}/>:<CircleAlert size={15}/>}</div><div><strong>{c.tool_name}</strong><span>{c.agent_name}</span></div><DecisionBadge decision={c.decision}/></div>):<div className="empty-state"><strong>No recent decisions</strong><p>Start a demo scenario to populate the control plane.</p></div>}</Card><Card><div className="eyebrow">SYSTEM INTEGRITY</div><div className="integrity-item"><span>Policy engine</span><RiskIndicator risk="LOW"/></div><div className="integrity-item"><span>Agent authority</span><RiskIndicator risk="LOW"/></div><div className="integrity-item"><span>WebMCP</span><span className="mono">{backendOnline?'ready':'standby'}</span></div></Card></aside></div><Card><div className="card-header"><div><div className="eyebrow">LIVE ACTIVITY</div><h2>Recent agent actions</h2></div><Link className="text-link" to="/activity">View all <ArrowUpRight size={14}/></Link></div><AgentTimeline calls={calls}/></Card></div>;
}
