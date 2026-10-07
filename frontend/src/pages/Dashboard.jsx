import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import ErrorMessage from '../components/ErrorMessage.jsx';
import InfrastructureTable from '../components/InfrastructureTable.jsx';
import Loading from '../components/Loading.jsx';
import StatCard from '../components/StatCard.jsx';
import RoadInfrastructureHero from '../components/RoadInfrastructureHero.jsx';
import ProjectOverviewCard from '../components/ProjectOverviewCard.jsx';
import ProgressPerformanceCard from '../components/ProgressPerformanceCard.jsx';
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

  if (state.loading) return <Loading label="Loading road infrastructure overview..." />;
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
      {/* 1. Road Infrastructure Project Hero Banner (Image 1) */}
      <RoadInfrastructureHero />

      {/* Operational Alerts Strip */}
      {data.alerts?.length > 0 && (
        <div className="alert-strip">
          <span className="alert-icon">⚠️</span>
          <div>
            <strong>Operational Roadway Signals</strong>
            <p>{data.alerts.join(' · ')}</p>
          </div>
        </div>
      )}

      {/* Road Infrastructure KPIs & Stat Cards */}
      <div className="stats-grid">
        <StatCard
          label="Total Monitored Corridors"
          value={formatNumber(data.total_assets)}
          note="Live inventory count"
          icon="🛣"
        />
        <StatCard
          label="Critical Hazard Assets"
          value={formatNumber(data.high_risk_assets)}
          note="Immediate inspection needed"
          icon="🔴"
          tone="red"
        />
        <StatCard
          label="Warning / Medium Risk"
          value={formatNumber(data.medium_risk_assets)}
          note="Scheduled maintenance"
          icon="🟡"
          tone="amber"
        />
        <StatCard
          label="Stable / Low Risk"
          value={formatNumber(low)}
          note="Clear operational health"
          icon="🟢"
          tone="green"
        />
        <StatCard
          label="Failure Probability"
          value={formatPercent(data.average_failure_probability)}
          note="Predictive ML model average"
          icon="⚡"
          tone="blue"
        />
      </div>

      {/* 2. Project Overview Component (Image 2) */}
      <ProjectOverviewCard
        title="Project Overview"
        description="The Road Infrastructure Project establishes an intelligent continuous assessment system for highways, bridges, transit corridors, and civil structures. By integrating sensor metrics, structural scores, environmental stress factors, and deep learning failure predictors, the platform empowers highway agencies to forecast degradation and schedule preventive interventions before safety compromises occur."
        metrics={[
          { label: 'Active Highway Sectors', value: '42' },
          { label: 'Bridge Safety Index', value: '88%' },
          { label: 'ML Prediction Reliability', value: '94.6%' },
        ]}
      />

      {/* 3. Progress & Performance Component (Image 3) */}
      <ProgressPerformanceCard
        title="Progress & Performance"
        description="Lifecycle milestone benchmarking across all road infrastructure development phases. Structural engineering diagnostics and predictive models continually validate foundation groundwork, structural piers, and asphalt wear friction layers to maximize asset longevity."
      />

      {/* Asset Health Distribution & Analytics Charts */}
      <div className="content-grid dashboard-charts">
        <section className="panel chart-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">HIGHWAY HEALTH STATUS</span>
              <h2>Risk Distribution</h2>
            </div>
            <span className="small-tag">Live Sensor Feed</span>
          </div>
          <RiskDistribution data={riskData} />
        </section>

        <section className="panel chart-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">ASSET CLASSIFICATION</span>
              <h2>Infrastructure Type</h2>
            </div>
          </div>
          <InfrastructureTypeChart data={[]} />
        </section>

        <section className="panel chart-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">TRANSIT CORRIDORS</span>
              <h2>Zone Risk Analysis</h2>
            </div>
          </div>
          <ZoneRiskChart data={[]} />
        </section>
      </div>

      {/* Recent Infrastructure Predictions */}
      <section className="panel">
        <div className="section-heading">
          <div>
            <span className="eyebrow">RECENT INSPECTION ASSESSMENTS</span>
            <h2>Recent Road & Bridge Predictions</h2>
            <p>Saved condition evaluations processed by the AI prediction engine.</p>
          </div>
          <Link className="subtle-link" to="/priority">
            View Maintenance Queue <span>→</span>
          </Link>
        </div>
        <InfrastructureTable assets={recent} compact />
      </section>

      <div className="info-footnote">
        Average remaining useful road life: <strong>{data.average_remaining_life == null ? 'Under calculation' : `${data.average_remaining_life} years`}</strong>
        {data.priority_focus && <> · Critical focus area: <strong>{data.priority_focus}</strong></>}
      </div>
    </div>
  );
}
