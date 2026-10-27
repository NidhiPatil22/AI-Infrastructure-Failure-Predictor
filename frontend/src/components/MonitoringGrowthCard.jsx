export default function MonitoringGrowthCard({ trend }) {
  if (!trend) return null;

  const total = Number(trend.total || trend.total_assets || 0);
  const previousTotal = Number(trend.previous_total || 0);
  const change = Number(trend.change || 0);
  const changePercent = Number(trend.change_percent || 0);
  const newAssets = Number(trend.new_assets || 0);
  const updatedAssets = Number(trend.updated_assets || 0);
  const reportedDamaged = Number(trend.newly_reported_damaged_assets || 0);

  const isPositive = change >= 0;

  return (
    <div className="panel monitoring-growth-card">
      <div className="section-heading">
        <div>
          <span className="eyebrow">MONITORING GROWTH & EXPANSION</span>
          <h2>Infrastructure Monitoring Trend</h2>
          <p>
            Audit tracking of civil assets under continuous sensory and GIS monitoring across Pune Metropolitan sectors.
          </p>
        </div>
        <span className="small-tag live-tag">
          <span className="pulsing-dot green" /> Version Snapshot
        </span>
      </div>

      <div className="trend-metrics-grid">
        <div className="trend-metric-box highlight-box">
          <span className="trend-label">Current Total Assets</span>
          <div className="trend-value-row">
            <strong className="trend-big-number">{total.toLocaleString()}</strong>
            <span className={`trend-badge ${isPositive ? 'trend-up' : 'trend-down'}`}>
              {isPositive ? '▲ +' : '▼ -'}
              {Math.abs(change).toLocaleString()} ({Math.abs(changePercent)}%)
            </span>
          </div>
          <small className="trend-subtext">Active Pune municipal inventory</small>
        </div>

        <div className="trend-metric-box">
          <span className="trend-label">Previous Baseline Total</span>
          <strong className="trend-number">{previousTotal.toLocaleString()}</strong>
          <small className="trend-subtext">Prior monthly benchmark audit</small>
        </div>

        <div className="trend-metric-box">
          <span className="trend-label">Newly Onboarded Assets</span>
          <strong className="trend-number text-accent">+{newAssets.toLocaleString()}</strong>
          <small className="trend-subtext">New corridors & structures</small>
        </div>

        <div className="trend-metric-box">
          <span className="trend-label">Telemetry Updated Assets</span>
          <strong className="trend-number text-cyan">{updatedAssets.toLocaleString()}</strong>
          <small className="trend-subtext">Inspections & sensor recertification</small>
        </div>

        <div className="trend-metric-box">
          <span className="trend-label">Newly Reported Damaged</span>
          <strong className="trend-number text-amber">{reportedDamaged.toLocaleString()}</strong>
          <small className="trend-subtext">Active citizen / field defect reports</small>
        </div>
      </div>

      <div className="trend-provenance-footer">
        <span className="provenance-badge">BASELINE PROVENANCE</span>
        <span>
          {trend.baseline_note ||
            'Calculated against previous monthly municipal audit snapshot. Telemetry represents verified synthetic benchmark records for Pune city.'}
        </span>
      </div>
    </div>
  );
}
