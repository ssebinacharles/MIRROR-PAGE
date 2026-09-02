import { Navigate, Route, Routes } from "react-router-dom";

import { AppShell } from "@/components/layout/AppShell";
import { OverviewPage } from "@/pages/OverviewPage";
import { IntentPage } from "@/pages/IntentPage";
import { ActivityPage } from "@/pages/ActivityPage";
import { ToolsPage } from "@/pages/ToolsPage";
import { ApprovalsPage } from "@/pages/ApprovalsPage";
import { AgentsPage } from "@/pages/AgentsPage";
import { AuditPage } from "@/pages/AuditPage";
import { SecurityPage } from "@/pages/SecurityPage";
import { DemoPage } from "@/pages/DemoPage";

function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<OverviewPage />} />
        <Route path="/intent" element={<IntentPage />} />
        <Route path="/activity" element={<ActivityPage />} />
        <Route path="/tools" element={<ToolsPage />} />
        <Route path="/approvals" element={<ApprovalsPage />} />
        <Route path="/agents" element={<AgentsPage />} />
        <Route path="/audit" element={<AuditPage />} />
        <Route path="/security" element={<SecurityPage />} />
        <Route path="/demo" element={<DemoPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AppShell>
  );
}

export default App;