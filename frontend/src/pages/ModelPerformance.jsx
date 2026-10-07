import { useCallback, useEffect, useState } from 'react';
import ErrorMessage from '../components/ErrorMessage.jsx';
import Loading from '../components/Loading.jsx';
import FeatureImportanceChart from '../components/charts/FeatureImportanceChart.jsx';
import { getAnalytics, getApiErrorMessage } from '../services/api.js';
import { formatMetric, humanize } from '../utils/formatters.js';

function metricRecords(analytics) {
  const records = Object.entries(analytics || {}).flatMap(([source, value]) => {
    if (!value || Array.isArray(value) || typeof value !== 'object') return [];
    return Object.entries(value).filter(([, metrics]) => metrics && typeof metrics === 'object' && !Array.isArray(metrics))
      .map(([model, metrics]) => ({ source, model, metrics }));
  });
  return records;
}

function MetricsTable({ records, type }) {
  const keys = type === 'classification'
    ? ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
    : ['mae', 'rmse', 'r2'];
  const models = records.filter(({ metrics }) => keys.some((key) => metrics[key] != null));
  if (!models.length) return <div className="chart-empty">No {type} metrics were returned by the analytics endpoint.</div>;
  return <div className="table-scroll"><table className="data-table metric-table"><thead><tr><th>Model</th>{keys.map((key) => <th key={key}>{humanize(key)}</th>)}</tr></thead><tbody>{models.map(({ model, metrics, source }) => <tr key={`${source}-${model}`}><td><strong>{model}</strong></td>{keys.map((key) => <td key={key}>{metrics[key] == null ? 'Not available' : formatMetric(metrics[key], 4)}</td>)}</tr>)}</tbody></table></div>;
}

export default function ModelPerformance() {
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
  if (state.loading) return <Loading label="Loading model metrics..." />;
  if (state.error) return <ErrorMessage message={state.error} onRetry={load} />;

  const analytics = state.data || {};
  const records = metricRecords(analytics);
  const clusters = analytics.cluster_results || {};
  const classificationRecords = records.filter(({ metrics }) => ['accuracy', 'precision', 'recall', 'f1', 'roc_auc'].some((key) => metrics[key] != null));
  const regressionRecords = records.filter(({ metrics }) => ['mae', 'rmse', 'r2'].some((key) => metrics[key] != null));

  return (
    <div className="page-stack">
      <div className="page-intro-row"><div><span className="eyebrow">TRAINING EVALUATION</span><h2>Model performance</h2><p>Every displayed score is read from the backend analytics response. Missing scores remain unavailable.</p></div><span className="schema-pill">Backend metrics</span></div>
      <section className="panel">
        <div className="section-heading"><div><span className="eyebrow">SUPERVISED LEARNING</span><h2>Classification metrics</h2><p>Failure classification model evaluation.</p></div></div>
        <MetricsTable records={classificationRecords} type="classification" />
      </section>
      <section className="panel">
        <div className="section-heading"><div><span className="eyebrow">REMAINING USEFUL LIFE</span><h2>Regression metrics</h2><p>Regression errors and coefficient of determination.</p></div></div>
        <MetricsTable records={regressionRecords} type="regression" />
      </section>
      <section className="content-grid performance-grid">
        <div className="panel chart-panel">
          <div className="section-heading"><div><span className="eyebrow">MODEL INTERPRETABILITY</span><h2>Feature importance</h2><p>Random Forest feature weights, where available.</p></div></div>
          <FeatureImportanceChart data={Array.isArray(analytics.feature_importance) ? analytics.feature_importance : []} />
        </div>
        <div className="panel">
          <div className="section-heading"><div><span className="eyebrow">UNSUPERVISED LEARNING</span><h2>Clustering evaluation</h2></div></div>
          <div className="cluster-metric"><span>Algorithm</span><strong>{analytics.model_summary?.clustering || 'Not available'}</strong></div>
          <div className="cluster-metric"><span>Selected clusters</span><strong>{clusters.selected_k ?? 'Not available'}</strong></div>
          <div className="cluster-metric"><span>Silhouette scores</span><strong>{clusters.silhouette_values?.length ? `${clusters.silhouette_values.length} values returned` : 'Not available'}</strong></div>
          <div className="cluster-metric"><span>Confusion matrix / ROC curve / PR curve</span><strong>Not available as separate visualizations</strong></div>
        </div>
      </section>
      <div className="info-footnote">The available API includes model metrics and K-Means summaries. PCA points, ROC curve coordinates, precision-recall points, and feature importance are not returned.</div>
    </div>
  );
}
