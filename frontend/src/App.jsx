import { useState } from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import Header from './components/Header.jsx';
import Sidebar from './components/Sidebar.jsx';
import About from './pages/About.jsx';
import Dashboard from './pages/Dashboard.jsx';
import InfrastructureMapPage from './pages/InfrastructureMapPage.jsx';
import DamageReportingPage from './pages/DamageReportingPage.jsx';
import InfrastructurePriority from './pages/InfrastructurePriority.jsx';
import PredictRisk from './pages/PredictRisk.jsx';
import DatasetAudit from './pages/DatasetAudit.jsx';

const pageInfo = {
  '/dashboard': ['Pune Infrastructure Dashboard', 'Continuous telemetry monitoring of 50,000 road segments and civil assets across Pune.'],
  '/map': ['Pune Infrastructure GIS Map', 'Live spatial monitoring and condition inspection restricted to Pune city boundary.'],
  '/damage-reports': ['Report Infrastructure Damage', 'Citizen & contractor damage upload with automatic boundary check, CV detection, and asset linking.'],
  '/predict': ['Predict Corridor Risk', 'Assess structural deterioration and failure probability using trained ML models.'],
  '/priority': ['Maintenance Priority Queue', 'Review prioritized infrastructure assets, reported defect escalations, and Knapsack scheduling.'],
  '/audit': ['Dataset Quality & Schema Audit', 'Inspect real-time 50,000-record dataset health, domain integrity, and target distribution.'],
  '/about': ['Project Provenance & Architecture', 'Documentation, dataset provenance, ML pipeline, and GIS boundary scope.'],
};

function NotFound() {
  return (
    <section className="panel not-found">
      <span className="eyebrow">ROAD HAZARD / ROUTE NOT FOUND</span>
      <h2>This road is currently closed.</h2>
      <p>Use the navigation menu to return to the active Pune infrastructure monitoring corridors.</p>
    </section>
  );
}

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const path = location.pathname === '/' ? '/dashboard' : location.pathname;
  const [title, description] = pageInfo[path] || ['Pune Infrastructure Monitor', ''];

  return (
    <div className="app-shell">
      <Sidebar open={sidebarOpen} onNavigate={() => setSidebarOpen(false)} />
      <main className="main-area">
        <Header title={title} description={description} onMenuClick={() => setSidebarOpen((open) => !open)} />
        <div className="page-content">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/map" element={<InfrastructureMapPage />} />
            <Route path="/damage-reports" element={<DamageReportingPage />} />
            <Route path="/predict" element={<PredictRisk />} />
            <Route path="/priority" element={<InfrastructurePriority />} />
            <Route path="/audit" element={<DatasetAudit />} />
            <Route path="/about" element={<About />} />
            {/* Legacy redirect safeguards without restoring removed tabs */}
            <Route path="/analytics" element={<Navigate to="/dashboard" replace />} />
            <Route path="/model-performance" element={<Navigate to="/dashboard" replace />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
          <footer className="page-footer">
            <div className="footer-brand">
              <span className="footer-dot-signal green" />
              <strong>PUNE URBAN INFRASTRUCTURE MONITOR</strong>
            </div>
            <div className="footer-tagline">
              <span>PMC & PCMC Boundary</span> · <span>100K+ Monitored Assets</span> · <span>AI Predictive Maintenance</span>
            </div>
          </footer>
        </div>
      </main>
    </div>
  );
}
