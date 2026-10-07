import { NavLink } from 'react-router-dom';

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: '⌂' },
  { to: '/predict', label: 'Predict Risk', icon: '⌁' },
  { to: '/analytics', label: 'Analytics', icon: '▥' },
  { to: '/model-performance', label: 'Model Performance', icon: '◈' },
  { to: '/priority', label: 'Infrastructure Priority', icon: '≡' },
  { to: '/about', label: 'About', icon: 'i' },
];

export default function Sidebar({ open, onNavigate }) {
  return (
    <>
      <button
        className={`sidebar-backdrop ${open ? 'visible' : ''}`}
        type="button"
        aria-label="Close navigation"
        onClick={onNavigate}
      />
      <aside className={`sidebar ${open ? 'sidebar-open' : ''}`}>
        <div className="brand">
          <div className="brand-mark" aria-hidden="true"><span>AI</span><i /></div>
          <div>
            <strong>URBAN<span>IQ</span></strong>
            <small>INFRASTRUCTURE INTELLIGENCE</small>
          </div>
        </div>
        <div className="sidebar-caption">WORKSPACE</div>
        <nav className="nav-list" aria-label="Main navigation">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => `nav-link${isActive ? ' nav-active' : ''}`}
              onClick={onNavigate}
            >
              <span className="nav-icon" aria-hidden="true">{link.icon}</span>
              <span>{link.label}</span>
              {link.label === 'Predict Risk' && <span className="nav-new">AI</span>}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="sidebar-status">
            <span className="status-orbit"><i /></span>
            <div><strong>AI Infrastructure Predictor</strong><small>AIML Mini Project</small></div>
          </div>
          <p>Predict. Analyze. Prevent.</p>
        </div>
      </aside>
    </>
  );
}
