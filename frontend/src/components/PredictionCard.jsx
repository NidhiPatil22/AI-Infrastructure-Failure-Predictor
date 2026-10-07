import { formatNumber, formatPercent } from '../utils/formatters.js';
import RiskBadge from './RiskBadge.jsx';

export default function PredictionCard({ result }) {
  if (!result) return null;
  return (
    <section className="prediction-result panel">
      <div className="result-heading">
        <div>
          <span className="eyebrow">PREDICTION COMPLETE</span>
          <h2>{result.asset_id || 'Infrastructure assessment'}</h2>
          <p>{result.asset_type || 'Asset'} · {result.zone || 'Zone not provided'}</p>
        </div>
        <RiskBadge risk={result.risk_level} />
      </div>
      <div className="result-metrics">
        <div className="result-probability">
          <span>Failure probability</span>
          <strong>{formatPercent(result.failure_probability)}</strong>
          <div className="probability-track"><i style={{ width: `${Math.max(0, Math.min(100, Number(result.failure_probability) * 100 || 0))}%` }} /></div>
        </div>
        <div className="result-metric"><span>Remaining useful life</span><strong>{formatNumber(result.remaining_useful_life, 1)} <small>years</small></strong></div>
        <div className="result-metric"><span>Priority</span><strong>{result.priority || 'Not available'}</strong></div>
      </div>
      <div className="result-note">
        <span className="note-symbol">i</span>
        <span>Failure label and a separate AI explanation are not returned by the current prediction API.</span>
      </div>
    </section>
  );
}
