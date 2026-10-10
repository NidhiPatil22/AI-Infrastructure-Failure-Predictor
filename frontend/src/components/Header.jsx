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

  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'dark');

  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    localStorage.setItem('theme', nextTheme);
    document.documentElement.setAttribute('data-theme', nextTheme);
  };

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <header className="topbar">
      <button className="menu-button" type="button" onClick={onMenuClick} aria-label="Toggle navigation">
        <span />
        <span />
        <span />
      </button>

      <div className="page-heading">
        <div className="eyebrow-container">
          <span className="road-hazard-strip" />
          <span className="eyebrow">ROAD INFRASTRUCTURE PROJECT · CIVIL HEALTH</span>
        </div>
        <h1>{title}</h1>
        <p>{description}</p>
      </div>

      <div className="topbar-status">
        <button
          type="button"
          className="theme-toggle-btn"
          onClick={toggleTheme}
          title={theme === 'dark' ? 'Switch to Sunlit Road (Day Mode)' : 'Switch to Dark Highway (Night Mode)'}
        >
          {theme === 'dark' ? '☀️ Day' : '🌙 Night'}
        </button>

        <div className="header-traffic-signal" title={connected ? 'System Status: Active & Connected' : 'System Status: Backend Offline'}>
          <span className={`signal-dot red ${!connected ? 'lit' : ''}`} />
          <span className="signal-dot yellow" />
          <span className={`signal-dot green ${connected ? 'lit' : ''}`} />
        </div>
        <div className="signal-label-group">
          <strong>{connected ? 'HIGHWAY SENSORS LIVE' : 'SIGNAL DISCONNECTED'}</strong>
          <small>{connected ? 'FastAPI Gateway Active' : 'Check Local Server'}</small>
        </div>
        <span className="status-divider" />
        <div className="project-badge-pill">
          <span>PROJECT 2026</span>
        </div>
      </div>
    </header>
  );
}
