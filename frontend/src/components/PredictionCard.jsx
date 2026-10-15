import { formatNumber, formatPercent } from '../utils/formatters.js';
import RiskBadge from './RiskBadge.jsx';

export default function PredictionCard({ result }) {
  if (!result) return null;
  const loc = result.location || {};
  const addr = loc.address || result.geo_metadata?.address;
  const lat = loc.latitude || result.geo_metadata?.latitude;
  const lng = loc.longitude || result.geo_metadata?.longitude;

  return (
    <section className="prediction-result panel">
      <div className="result-heading">
        <div>
          <span className="eyebrow">ASSESSMENT COMPLETE · SUPERVISED ML</span>
          <h2>{result.asset_id || 'Infrastructure Assessment'}</h2>
          <p>
            <strong>{result.asset_type || 'Asset'}</strong>
            {addr ? ` · 📍 ${addr}` : result.zone ? ` · ${result.zone} Zone` : ''}
          </p>
        </div>
        <RiskBadge risk={result.risk_level} />
      </div>

      {addr && (
        <div className="result-location-pill">
          <span>📍 <strong>Assessed Corridor:</strong> {addr}</span>
          {lat && lng && (
            <span className="coord-chip">({Number(lat).toFixed(4)}°N, {Number(lng).toFixed(4)}°E)</span>
          )}
          <a
            href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(addr)}`}
            target="_blank"
            rel="noopener noreferrer"
            className="mini-maps-link"
          >
            Open in Google Maps ↗
          </a>
        </div>
      )}

      <div className="result-metrics">
        <div className="result-probability">
          <span>Failure Probability</span>
          <strong>{formatPercent(result.failure_probability)}</strong>
          <div className="probability-track">
            <i style={{ width: `${Math.max(0, Math.min(100, Number(result.failure_probability) * 100 || 0))}%` }} />
          </div>
        </div>
        <div className="result-metric">
          <span>Remaining Useful Life (RUL)</span>
          <strong>{formatNumber(result.remaining_useful_life, 1)} <small>years</small></strong>
        </div>
        <div className="result-metric">
          <span>Triage Priority</span>
          <strong className={`priority-tag ${result.priority?.toLowerCase() || ''}`}>{result.priority || 'Standard'}</strong>
        </div>
      </div>

      <div className="result-note">
        <span className="note-symbol">ℹ️</span>
        <span>
          {result.data_limitations ||
            'Trained Random Forest evaluation using physical civil condition indicators. Grounded in regional baseline telemetry.'}
        </span>
      </div>
    </section>
  );
}
