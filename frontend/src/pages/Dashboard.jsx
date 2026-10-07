import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import ErrorMessage from '../components/ErrorMessage.jsx';
import InfrastructureTable from '../components/InfrastructureTable.jsx';
import Loading from '../components/Loading.jsx';
import StatCard from '../components/StatCard.jsx';
import InfrastructureTypeChart from '../components/charts/InfrastructureTypeChart.jsx';
import RiskDistribution from '../components/charts/RiskDistribution.jsx';
import ZoneRiskChart from '../components/charts/ZoneRiskChart.jsx';
import { getApiErrorMessage, getDashboard } from '../services/api.js';
import { formatNumber, formatPercent } from '../utils/formatters.js';

export default function Dashboard() {
  const [state, setState] = useState({ loading: true, error: '', data: null });
  const load = useCallback(async () => {
    setState({ loading: true, error: '', data: null });
    try {
      const data = await getDashboard();
      setState({ loading: false, error: '', data });
    } catch (error) {
      setState({ loading: false, error: getApiErrorMessage(error), data: null });
    }
  }, []);
  useEffect(() => { load(); }, [load]);

  if (state.loading) return <Loading label="Loading the city overview..." />;
  if (state.error) return <ErrorMessage message={state.error} onRetry={load} />;

  const data = state.data || {};
  const total = Number(data.total_assets);
  const high = Number(data.high_risk_assets);
  const medium = Number(data.medium_risk_assets);
  const low = Number.isFinite(total - high - medium) ? Math.max(0, total - high - medium) : NaN;
  const riskData = [
    { name: 'Low risk', value: low },
    { name: 'Medium risk', value: medium },
    { name: 'High risk', value: high },
  ].filter((item) => Number.isFinite(item.value));
  const recent = Array.isArray(data.recent_predictions) ? data.recent_predictions : [];

  return (
    <div className="page-stack">
      <div className="welcome-banner">
        <div><span className="eyebrow">CITY INFRASTRUCTURE / LIVE OVERVIEW</span><h2>{data.title || 'Infrastructure health overview'}</h2><p>Model-backed predictions and the latest health indicators from your local API.</p></div>
        <Link to="/predict" className="primary-button"><span>＋</span> Run a prediction</Link>
        <div className="banner-grid" aria-hidden="true" />
      </div>
      {data.alerts?.length > 0 && <div className="alert-strip"><span>!</span><div><strong>Operational signals</strong><p>{data.alerts.join(' · ')}</p></div></div>}
      <div className="stats-grid">
        <StatCard label="Total infrastructure assets" value={formatNumber(data.total_assets)} note="Reported by dashboard API" icon="▦" />
        <StatCard label="High risk assets" value={formatNumber(data.high_risk_assets)} note="Reported by dashboard API" icon="!" tone="red" />
        <StatCard label="Medium risk assets" value={formatNumber(data.medium_risk_assets)} note="Reported by dashboard API" icon="◷" tone="amber" />
        <StatCard label="Low risk assets" value={formatNumber(low)} note="Derived from total minus high and medium" icon="✓" tone="green" />
        <StatCard label="Average failure probability" value={formatPercent(data.average_failure_probability)} note="Not included in dashboard response" icon="⌁" tone="blue" />
      </div>
      <div className="content-grid dashboard-charts">
        <section className="panel chart-panel">
          <div className="section-heading"><div><span className="eyebrow">ASSET HEALTH</span><h2>Risk distribution</h2></div><span className="small-tag">API summary</span></div>
          <RiskDistribution data={riskData} />
        </section>
        <section className="panel chart-panel">
          <div className="section-heading"><div><span className="eyebrow">ASSET MIX</span><h2>Infrastructure type</h2></div></div>
          <InfrastructureTypeChart data={[]} />
        </section>
        <section className="panel chart-panel">
          <div className="section-heading"><div><span className="eyebrow">GEOGRAPHIC SIGNALS</span><h2>Zone risk</h2></div></div>
          <ZoneRiskChart data={[]} />
        </section>
      </div>
      <section className="panel">
        <div className="section-heading"><div><span className="eyebrow">RECENT ACTIVITY</span><h2>Recent predictions</h2><p>Most recent saved assessments returned by the dashboard API.</p></div><Link className="subtle-link" to="/priority">View priority history <span>→</span></Link></div>
        <InfrastructureTable assets={recent} compact />
      </section>
      <div className="info-footnote">Average remaining life in the current summary: <strong>{data.average_remaining_life == null ? 'Not available' : `${data.average_remaining_life} years`}</strong>{data.priority_focus && <> · Focus area: <strong>{data.priority_focus}</strong></>}</div>
    </div>
  );
}
