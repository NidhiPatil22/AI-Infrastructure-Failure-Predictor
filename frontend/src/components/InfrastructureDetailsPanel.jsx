import { useState } from 'react';

export default function InfrastructureDetailsPanel({ asset, onClose, onSelectReport }) {
  const [activeTab, setActiveTab] = useState('overview');

  if (!asset) return null;

  const risk = String(asset.risk_level || 'LOW').toUpperCase();
  const riskClass =
    risk === 'CRITICAL'
      ? 'risk-critical'
      : risk === 'HIGH'
      ? 'risk-high'
      : risk === 'MEDIUM'
      ? 'risk-medium'
      : 'risk-low';

  const prob = Number(asset.failure_probability || 0);
  const condition = Number(
    asset.condition_score ?? (asset.structural_score ? asset.structural_score * 0.8 : 75)
  );
  const roadClass = asset.road_class ? asset.road_class.charAt(0).toUpperCase() + asset.road_class.slice(1) : '';
  const typeName = (asset.asset_type || 'Road Segment').replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  const displayTitle = roadClass ? `${roadClass} ${typeName}` : (typeName || 'Road Infrastructure');
  const rulDays = asset.remaining_useful_life_days != null
    ? asset.remaining_useful_life_days
    : Math.round(Number(asset.remaining_useful_life || 0) * 365);
  const damageReports = Array.isArray(asset.damage_reports) ? asset.damage_reports : [];

  return (
    <div
      className="asset-drawer-root"
      role="dialog"
      aria-modal="true"
      aria-label="Infrastructure Details"
    >
      {/* Dimmed backdrop to close on outside click */}
      <div className="asset-drawer-backdrop" onClick={onClose} />

      {/* Slide-in Drawer Panel */}
      <aside className="asset-drawer-panel">
        {/* Drawer Header */}
        <div className="asset-drawer-header">
          <div className="asset-drawer-title-group">
            <span className="asset-drawer-eyebrow">MONITORED INFRASTRUCTURE</span>
            <div className="asset-drawer-id-row">
              <h2 className="asset-drawer-id">{displayTitle}</h2>
              <span className={`asset-tag-risk ${riskClass}`}>{risk} RISK</span>
            </div>
            <div className="asset-drawer-badges">
              <span className="asset-tag-type">{typeName}</span>
              <span className="asset-tag-locality">
                📍 {asset.locality || asset.pune_ward || 'Pune'}
              </span>
              {damageReports.length > 0 && (
                <span className="asset-tag-damage">
                  ⚠️ {damageReports.length} Active Damage {damageReports.length > 1 ? 'Reports' : 'Report'}
                </span>
              )}
            </div>
          </div>
          <button
            className="asset-drawer-close-btn"
            type="button"
            onClick={onClose}
            aria-label="Close details"
          >
            ✕
          </button>
        </div>

        {/* Tab Navigation */}
        <nav className="asset-drawer-nav">
          <button
            type="button"
            className={`asset-nav-tab ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button
            type="button"
            className={`asset-nav-tab ${activeTab === 'maintenance' ? 'active' : ''}`}
            onClick={() => setActiveTab('maintenance')}
          >
            Maintenance
          </button>
          <button
            type="button"
            className={`asset-nav-tab ${activeTab === 'damage' ? 'active' : ''}`}
            onClick={() => setActiveTab('damage')}
          >
            Damage ({damageReports.length})
          </button>
          <button
            type="button"
            className={`asset-nav-tab ${activeTab === 'ai' ? 'active' : ''}`}
            onClick={() => setActiveTab('ai')}
          >
            AI Models
          </button>
        </nav>

        {/* Scrollable Content Body */}
        <div className="asset-drawer-body">
          {activeTab === 'overview' && (
            <div className="asset-tab-pane">
              {/* Overall Structural Condition Meter */}
              <div className="asset-card condition-card">
                <div className="condition-card-top">
                  <span className="card-label">Overall Structural Condition</span>
                  <span className="condition-score-display">{condition.toFixed(1)} / 100</span>
                </div>
                <div className="asset-progress-bar-track">
                  <div
                    className={`asset-progress-bar-fill ${
                      condition < 45 ? 'fill-red' : condition < 70 ? 'fill-amber' : 'fill-green'
                    }`}
                    style={{ width: `${Math.min(100, Math.max(5, condition))}%` }}
                  />
                </div>
                <div className="condition-status-note">
                  {condition < 45
                    ? '🔴 Severe structural degradation detected — overhaul required'
                    : condition < 70
                    ? '🟡 Moderate wear — routine preventive maintenance recommended'
                    : '🟢 Sound structural integrity operating within normal safety limits'}
                </div>
              </div>

              {/* 4 Key Performance Indicators */}
              <div className="asset-kpi-grid">
                <div className="asset-kpi-item">
                  <span className="kpi-label">Predicted RUL</span>
                  <strong className="kpi-val highlight-amber">{rulDays} days</strong>
                  <span className="kpi-sub">Remaining Useful Life</span>
                </div>
                <div className="asset-kpi-item">
                  <span className="kpi-label">Failure Probability</span>
                  <strong
                    className={`kpi-val ${
                      prob > 0.6 ? 'text-red' : prob > 0.3 ? 'text-amber' : 'text-green'
                    }`}
                  >
                    {(prob * 100).toFixed(1)}%
                  </strong>
                  <span className="kpi-sub">ML Classifier Score</span>
                </div>
                <div className="asset-kpi-item">
                  <span className="kpi-label">Asset Age</span>
                  <strong className="kpi-val">{asset.age_years || '—'} yrs</strong>
                  <span className="kpi-sub">Service duration</span>
                </div>
                <div className="asset-kpi-item">
                  <span className="kpi-label">Previous Failures</span>
                  <strong className="kpi-val">{asset.previous_failures || 0}</strong>
                  <span className="kpi-sub">Recorded incidents</span>
                </div>
              </div>

              {/* Geographic & Structural Properties */}
              <div className="asset-card">
                <h4 className="asset-card-title">Geographic & Engineering Metadata</h4>
                <div className="asset-prop-table">
                  <div className="asset-prop-row">
                    <span className="prop-name">City / Sector</span>
                    <span className="prop-val">Pune Metropolitan (PMC / PCMC)</span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Pune Ward</span>
                    <span className="prop-val">{asset.pune_ward || 'Pune Municipal Ward'}</span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Locality / Area</span>
                    <span className="prop-val">{asset.locality || 'Pune Municipal Sector'}</span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Municipal Zone</span>
                    <span className="prop-val">{asset.zone || 'Central'}</span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">GPS Coordinates</span>
                    <span className="prop-val mono">
                      {Number(asset.latitude).toFixed(6)}, {Number(asset.longitude).toFixed(6)}
                    </span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Material</span>
                    <span className="prop-val">
                      {asset.material || 'Reinforced Concrete / Steel'}
                    </span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Traffic Density</span>
                    <span className="prop-val">
                      {asset.traffic_density ? `${asset.traffic_density} / 100` : 'Moderate'}
                    </span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Corrosion Index</span>
                    <span className="prop-val">
                      {asset.corrosion_level ? `${asset.corrosion_level}%` : 'Standard'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'maintenance' && (
            <div className="asset-tab-pane">
              {/* Engineering Action Card */}
              <div className="asset-card action-card">
                <div className="action-tag">RECOMMENDED ENGINEERING ACTION</div>
                <p className="action-text">
                  {asset.recommended_action ||
                    'Maintain regular IoT and citizen damage monitoring. Schedule structural inspection during upcoming municipal sweep.'}
                </p>
                <div className="action-priority-row">
                  <span>Priority Rating:</span>
                  <span className={`asset-tag-risk ${riskClass}`}>
                    {asset.priority_label || risk}
                  </span>
                </div>
              </div>

              {/* Maintenance History Log */}
              <div className="asset-card">
                <h4 className="asset-card-title">Intervention & Maintenance Schedule</h4>
                <div className="asset-prop-table">
                  <div className="asset-prop-row">
                    <span className="prop-name">Current Status</span>
                    <span className="prop-val status-operational">
                      {asset.status || 'Active Monitoring'}
                    </span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Interventions Recorded</span>
                    <span className="prop-val">{asset.maintenance_count ?? 3} completed</span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Last Maintenance</span>
                    <span className="prop-val">
                      {asset.days_since_maintenance
                        ? `${Math.round(asset.days_since_maintenance)} days ago`
                        : 'Within 90 days'}
                    </span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Last Physical Inspection</span>
                    <span className="prop-val">
                      {asset.days_since_inspection
                        ? `${Math.round(asset.days_since_inspection)} days ago`
                        : 'Within 30 days'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'damage' && (
            <div className="asset-tab-pane">
              {damageReports.length === 0 ? (
                <div className="asset-empty-box">
                  <div className="empty-check-icon">✓</div>
                  <h4>No Active Damage Reports</h4>
                  <p>
                    No citizen or field engineer damage reports are currently pending for this asset.
                  </p>
                </div>
              ) : (
                <div className="damage-reports-stack">
                  {damageReports.map((rep) => (
                    <div key={rep.report_id} className="damage-feed-item">
                      <div className="damage-item-top">
                        <strong className="rep-id">{rep.report_id}</strong>
                        <span
                          className={`rep-status-badge ${String(rep.status)
                            .toLowerCase()
                            .replace(/\s+/g, '-')}`}
                        >
                          {rep.status}
                        </span>
                      </div>
                      <div className="damage-item-type">
                        Defect: <strong>{rep.damage_type}</strong>
                      </div>
                      {rep.cv_detected && (
                        <div className="damage-item-cv">
                          CV Detected: <strong>{rep.cv_detected}</strong>
                          {rep.cv_confidence && (
                            <small> ({(rep.cv_confidence * 100).toFixed(0)}% conf)</small>
                          )}
                        </div>
                      )}
                      {rep.description && <p className="damage-item-desc">{rep.description}</p>}
                      {rep.image_url && (
                        <div className="damage-img-wrapper">
                          <img
                            src={rep.image_url}
                            alt={`Inspection for ${rep.report_id}`}
                            className="damage-report-thumb"
                            onError={(e) => {
                              e.currentTarget.style.display = 'none';
                            }}
                          />
                        </div>
                      )}
                      <div className="damage-item-date">
                        Reported: {rep.created_at ? new Date(rep.created_at).toLocaleDateString() : 'Recent'}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'ai' && (
            <div className="asset-tab-pane">
              <div className="asset-card">
                <h4 className="asset-card-title">ML Pipeline Diagnostics & Attribution</h4>
                <div className="asset-prop-table">
                  <div className="asset-prop-row">
                    <span className="prop-name">Failure Risk Tier</span>
                    <span className={`asset-tag-risk ${riskClass}`}>{risk}</span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Failure Probability</span>
                    <span className="prop-val">{(prob * 100).toFixed(2)}%</span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Predicted Useful Life (RUL)</span>
                    <span className="prop-val highlight-amber">{rulDays} days</span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Underlying Model Ensemble</span>
                    <span className="prop-val">Random Forest + GBDT (FLAML Auto-Tuned)</span>
                  </div>
                  <div className="asset-prop-row">
                    <span className="prop-name">Training Protocol</span>
                    <span className="prop-val">Stratified Zero-Leakage Fit</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Drawer Footer */}
        <div className="asset-drawer-footer">
          <button className="asset-drawer-action-btn" type="button" onClick={onClose}>
            Done Reviewing Asset
          </button>
        </div>
      </aside>
    </div>
  );
}
