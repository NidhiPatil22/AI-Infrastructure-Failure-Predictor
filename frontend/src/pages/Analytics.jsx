import { useCallback, useEffect, useState } from 'react';
import ErrorMessage from '../components/ErrorMessage.jsx';
import Loading from '../components/Loading.jsx';
import ClusterChart from '../components/charts/ClusterChart.jsx';
import { getAnalytics, getApiErrorMessage } from '../services/api.js';
import { formatNumber, formatMetric, humanize } from '../utils/formatters.js';

export default function Analytics() {
  const [state, setState] = useState({ loading: true, error: '', data: null });
  const load = useCallback(async () => {
    setState({ loading: true, error: '', data: null });
    try {
      setState({ loading: false, error: '', data: await getAnalytics() });
    } catch (error) {
      setState({ loading: false, error: getApiErrorMessage(error), data: null });
    }
  }, []);
  useEffect(() => { load(); }, [load]);
  if (state.loading) return <Loading label="Loading analytics..." />;
  if (state.error) return <ErrorMessage message={state.error} onRetry={load} />;

  const data = state.data || {};
  const clusterData = data.cluster_results || {};
  const clusters = Array.isArray(clusterData.cluster_summary) ? clusterData.cluster_summary : [];
  const silhouettes = Array.isArray(clusterData.silhouette_values) ? clusterData.silhouette_values : [];

  return (
    <div className="page-stack">
      <div className="page-intro-row"><div><span className="eyebrow">PATTERNS & INSIGHTS</span><h2>Infrastructure analytics</h2><p>Charts are limited to metrics and summaries provided by the analytics API.</p></div><span className="schema-pill">Live API data</span></div>
      <section className="panel">
        <div className="section-heading"><div><span className="eyebrow">MODEL OBSERVATIONS</span><h2>Current insights</h2></div></div>
        {Array.isArray(data.insights) && data.insights.length ? <div className="insight-grid">{data.insights.map((insight, index) => <article className="insight-card" key={insight}><span className="insight-index">0{index + 1}</span><p>{insight}</p></article>)}</div> : <p className="muted">No insights were returned.</p>}
      </section>
      <section className="content-grid analytics-grid">
        <div className="panel chart-panel">
          <div className="section-heading"><div><span className="eyebrow">UNSUPERVISED LEARNING</span><h2>Cluster distribution</h2><p>Asset count by cluster from the trained K-Means model.</p></div></div>
          <ClusterChart clusters={clusters} />
        </div>
        <div className="panel">
          <div className="section-heading"><div><span className="eyebrow">CLUSTER QUALITY</span><h2>Silhouette scores</h2></div></div>
          {silhouettes.length ? <div className="score-list">{silhouettes.map((item) => <div className="score-row" key={item.k}><span>k = {item.k}</span><div className="score-track"><i style={{ width: `${Math.max(0, Math.min(100, Number(item.silhouette_score) * 100))}%` }} /></div><strong>{formatMetric(item.silhouette_score, 4)}</strong></div>)}</div> : <div className="chart-empty">Silhouette scores are not available.</div>}
          {clusterData.selected_k != null && <div className="selected-k">Selected cluster count <strong>{formatNumber(clusterData.selected_k)}</strong></div>}
        </div>
      </section>
      <section className="panel">
        <div className="section-heading"><div><span className="eyebrow">CLUSTER PROFILES</span><h2>Cluster characteristics</h2></div></div>
        {clusters.length ? <div className="cluster-cards">{clusters.map((cluster) => <article className="cluster-card" key={cluster.cluster_id}><div className="cluster-top"><span>CLUSTER {cluster.cluster_id}</span><strong>{formatNumber(cluster.size)} <small>assets</small></strong></div><h3>{humanize(cluster.description)}</h3><dl><div><dt>Average age</dt><dd>{formatNumber(cluster.average_age_years, 1)} yr</dd></div><div><dt>Structural score</dt><dd>{formatNumber(cluster.average_structural_score, 1)}</dd></div><div><dt>Days since maintenance</dt><dd>{formatNumber(cluster.average_days_since_maintenance, 1)}</dd></div><div><dt>Prior failures</dt><dd>{formatNumber(cluster.average_previous_failures, 1)}</dd></div></dl></article>)}</div> : <p className="muted">Cluster characteristics are not available in this response.</p>}
      </section>
      <section className="content-grid">
        <div className="panel chart-panel"><div className="section-heading"><div><span className="eyebrow">FAILURE ANALYSIS</span><h2>Type and zone breakdown</h2></div></div><div className="unavailable-grid"><p>Failure distribution by type and zone requires raw grouped counts, which the analytics API does not return.</p><p>Age, structural score, maintenance gap, traffic/load relationships and correlation data are also not provided.</p></div></div>
        <div className="panel chart-panel"><div className="section-heading"><div><span className="eyebrow">PCA</span><h2>2D cluster projection</h2></div></div><div className="chart-empty">PCA coordinates are not returned by the backend analytics endpoint.</div></div>
      </section>
    </div>
  );
}
