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
  '/dashboard': ['City overview', 'A live snapshot of infrastructure health and prediction activity.'],
  '/predict': ['Predict risk', 'Assess an asset using the model trained by your backend.'],
  '/analytics': ['Analytics', 'Explore the metrics and clustering insights currently exposed by the API.'],
  '/model-performance': ['Model performance', 'Review the training metrics available from backend artifacts.'],
  '/priority': ['Infrastructure priority', 'Review saved prediction history and maintenance guidance.'],
  '/about': ['About the project', 'A student project exploring predictive maintenance for urban assets.'],
};

function NotFound() {
  return <section className="panel not-found"><span className="eyebrow">404 / NOT FOUND</span><h2>This page is not on the map.</h2><p>Use the navigation to return to the infrastructure workspace.</p></section>;
}

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const path = location.pathname === '/' ? '/dashboard' : location.pathname;
  const [title, description] = pageInfo[path] || ['Page not found', ''];

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
          <footer className="page-footer"><span>AI Urban Infrastructure Failure Predictor</span><span>Predict. Analyze. Prevent.</span></footer>
        </div>
      </main>
    </div>
  );
}
