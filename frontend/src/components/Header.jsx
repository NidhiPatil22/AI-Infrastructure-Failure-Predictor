import { useEffect, useState } from 'react';
import { getHealth } from '../services/api.js';

export default function Header({ title, description, onMenuClick }) {
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    let active = true;
    const checkHealth = async () => {
      try {
        const health = await getHealth();
        if (active) setConnected(health?.status === 'ok');
      } catch {
        if (active) setConnected(false);
      }
    };
    checkHealth();
    const timer = window.setInterval(checkHealth, 30000);
    return () => {
      active = false;
      window.clearInterval(timer);
    };
  }, []);

  return (
    <header className="topbar">
      <button className="menu-button" type="button" onClick={onMenuClick} aria-label="Toggle navigation">
        <span />
        <span />
        <span />
      </button>
      <div className="page-heading">
        <span className="eyebrow">SMART CITY / INFRASTRUCTURE INTELLIGENCE</span>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>
      <div className="topbar-status">
        <span className={`api-dot ${connected ? 'is-connected' : 'is-offline'}`} />
        <span>{connected ? 'API Connected' : 'API Offline'}</span>
        <span className="status-divider" />
        <span className="system-label">AI Prediction System</span>
      </div>
    </header>
  );
}
