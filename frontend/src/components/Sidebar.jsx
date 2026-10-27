import { NavLink } from 'react-router-dom';

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: '🛣' },
  { to: '/map', label: 'Infrastructure Map', icon: '🗺', tag: 'PUNE' },
  { to: '/damage-reports', label: 'Damage Reports', icon: '📸', tag: 'NEW' },
  { to: '/predict', label: 'Predict Risk', icon: '⚠️', isAi: true },
  { to: '/priority', label: 'Priority Queue', icon: '🚦' },
  { to: '/audit', label: 'Dataset Audit', icon: '📋' },
  { to: '/about', label: 'Project Info', icon: 'ℹ' },
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
          <div className="brand-mark-road" aria-hidden="true">
            <span className="brand-traffic-dots">
              <i className="dot-green" />
              <i className="dot-yellow" />
              <i className="dot-red" />
            </span>
          </div>
          <div>
            <strong className="brand-title">PUNE<span>INFRA</span></strong>
            <small className="brand-tagline">100K+ MONITORED ASSETS</small>
          </div>
        </div>

        <div className="sidebar-caption">CIVIL MONITORING WORKSPACE</div>
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
              {link.isAi && <span className="nav-new">AI ML</span>}
              {link.tag && !link.isAi && <span className="nav-tag-pune">{link.tag}</span>}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-traffic-status">
            <div className="mini-signal-indicator">
              <span className="signal-lamp green active" />
              <span className="signal-lamp yellow" />
              <span className="signal-lamp red" />
            </div>
            <div>
              <strong>PUNE METROPOLITAN</strong>
              <small>PMC & PCMC · 100K Active</small>
            </div>
          </div>
          <p className="sidebar-footer-motto">Planning · Construction · Progress · Impact</p>
        </div>
      </aside>
    </>
  );
}
