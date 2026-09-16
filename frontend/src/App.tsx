import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { DashboardPage } from './pages/DashboardPage';
import { MockBankSandboxPage } from './pages/MockBankSandboxPage';
import { SimulationLabPage } from './pages/SimulationLabPage';
import { IncidentsPage } from './pages/IncidentsPage';
import { AlertsPage } from './pages/AlertsPage';
import { ApiInventoryPage } from './pages/ApiInventoryPage';
import { TestExecutionPage } from './pages/TestExecutionPage';
import { SecurityRulesPage } from './pages/SecurityRulesPage';
import { PosturePage } from './pages/PosturePage';
import { ReportsPage } from './pages/ReportsPage';

export const App: React.FC = () => {
  return (
    <Router>
      <div className="flex min-h-screen bg-[#0B0F17] text-slate-100 font-sans">
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <Header />
          <main className="flex-1 overflow-y-auto">
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/banking" element={<MockBankSandboxPage />} />
              <Route path="/sandbox" element={<MockBankSandboxPage />} />
              <Route path="/simulation" element={<SimulationLabPage />} />
              <Route path="/incidents" element={<IncidentsPage />} />
              <Route path="/alerts" element={<AlertsPage />} />
              <Route path="/apis" element={<ApiInventoryPage />} />
              <Route path="/tests" element={<TestExecutionPage />} />
              <Route path="/test-execution" element={<TestExecutionPage />} />
              <Route path="/rules" element={<SecurityRulesPage />} />
              <Route path="/posture" element={<PosturePage />} />
              <Route path="/reports" element={<ReportsPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
};

export default App;
