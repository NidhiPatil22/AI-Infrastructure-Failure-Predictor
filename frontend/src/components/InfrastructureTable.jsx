import { formatNumber, formatPercent, humanize } from '../utils/formatters.js';
import RiskBadge from './RiskBadge.jsx';

export default function InfrastructureTable({ assets = [], compact = false }) {
  const rows = assets || [];
  if (!rows.length) {
    return <div className="empty-state"><span className="empty-icon">⌁</span><strong>No prediction history yet</strong><p>Completed predictions will appear here when the backend has saved history.</p></div>;
  }

  return (
    <div className="table-scroll">
      <table className="data-table">
        <thead><tr>
          <th>Rank</th><th>Infrastructure Segment</th><th>Type</th><th>Locality / Ward</th><th>Failure probability</th><th>Risk</th><th>Estimated RUL</th><th>Priority</th>
          {!compact && <th>Recommended action</th>}
        </tr></thead>
        <tbody>
          {rows.map((asset, index) => {
            const typeLabel = humanize(asset.asset_type || 'Road Segment');
            const classLabel = asset.road_class ? humanize(asset.road_class) : '';
            const segmentLabel = asset.display_title || (asset.locality ? `${classLabel ? `${classLabel} ` : ''}${typeLabel} · ${asset.locality}` : `${classLabel ? `${classLabel} ` : ''}${typeLabel}`);
            const rulDays = asset.remaining_useful_life_days != null
              ? asset.remaining_useful_life_days
              : (asset.remaining_useful_life != null ? Math.round(Number(asset.remaining_useful_life) > 100 ? Number(asset.remaining_useful_life) : Number(asset.remaining_useful_life) * 365) : null);

            return (
              <tr key={`${asset.asset_id || 'infra'}-${index}`}>
                <td className="rank-cell">{String(index + 1).padStart(2, '0')}</td>
                <td><strong>{segmentLabel}</strong></td>
                <td><span className="infra-pill">{typeLabel}</span></td>
                <td>{asset.locality || asset.zone || asset.pune_ward || 'Pune'}</td>
                <td>{formatPercent(asset.failure_probability)}</td>
                <td><RiskBadge risk={asset.risk_level} /></td>
                <td>{rulDays != null ? `${formatNumber(rulDays)} days` : 'Not available'}</td>
                <td>{asset.priority || 'Standard'}</td>
                {!compact && <td className="action-cell">{asset.recommendation || 'Continuous IoT monitoring'}</td>}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
