import { useState } from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import Header from './components/Header.jsx';
import Sidebar from './components/Sidebar.jsx';
import About from './pages/About.jsx';
import Analytics from './pages/Analytics.jsx';
import Dashboard from './pages/Dashboard.jsx';
import InfrastructurePriority from './pages/InfrastructurePriority.jsx';
import ModelPerformance from './pages/ModelPerformance.jsx';
import PredictRisk from './pages/PredictRisk.jsx';

const pageInfo = {
  '/dashboard': ['Road Infrastructure Project', 'Continuous monitoring of highway corridors, bridges, and municipal assets.'],
  '/predict': ['Predict Corridor Risk', 'Assess structural deterioration and failure probability using trained ML models.'],
  '/analytics': ['Infrastructure Analytics', 'Explore clustering insights, silhouette scores, and condition metrics.'],
  '/model-performance': ['Model Performance', 'Review classification accuracy, regression errors, and model benchmarks.'],
  '/priority': ['Maintenance Priority Queue', 'Review prioritized infrastructure assets and recommended interventions.'],
  '/about': ['Project Overview', 'Planning, construction lifecycle, machine learning architecture, and future scope.'],
};

function NotFound() {
  return (
    <section className="panel not-found">
      <span className="eyebrow">ROAD HAZARD / ROUTE NOT FOUND</span>
      <h2>This road is currently closed.</h2>
      <p>Use the navigation menu to return to the active infrastructure project corridors.</p>
    </section>
  );
}

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const path = location.pathname === '/' ? '/dashboard' : location.pathname;
  const [title, description] = pageInfo[path] || ['Road Infrastructure Project', ''];

  return (
    <div className="app-shell">
      <Sidebar open={sidebarOpen} onNavigate={() => setSidebarOpen(false)} />
      <main className="main-area">
        <Header title={title} description={description} onMenuClick={() => setSidebarOpen((open) => !open)} />
        <div className="page-content">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/predict" element={<PredictRisk />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/model-performance" element={<ModelPerformance />} />
            <Route path="/priority" element={<InfrastructurePriority />} />
            <Route path="/about" element={<About />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
          <footer className="page-footer">
            <div className="footer-brand">
              <span className="footer-dot-signal green" />
              <strong>ROAD INFRASTRUCTURE PROJECT</strong>
            </div>
            <div className="footer-tagline">
              <span>Planning</span> · <span>Construction</span> · <span>Progress</span> · <span>Impact</span>
            </div>
          </footer>
        </div>
      </main>
    </div>
  );
}
