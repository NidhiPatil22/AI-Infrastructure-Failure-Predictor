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
          <th>Rank</th><th>Asset ID</th><th>Type</th><th>Zone</th><th>Failure probability</th><th>Risk</th><th>RUL</th><th>Priority</th>
          {!compact && <th>Recommended action</th>}
        </tr></thead>
        <tbody>
          {rows.map((asset, index) => (
            <tr key={`${asset.asset_id || 'asset'}-${index}`}>
              <td className="rank-cell">{String(index + 1).padStart(2, '0')}</td>
              <td><strong>{asset.asset_id || 'Not available'}</strong></td>
              <td>{humanize(asset.asset_type)}</td>
              <td>{asset.zone || 'Not available'}</td>
              <td>{formatPercent(asset.failure_probability)}</td>
              <td><RiskBadge risk={asset.risk_level} /></td>
              <td>{asset.remaining_useful_life == null ? 'Not available' : `${formatNumber(asset.remaining_useful_life, 1)} yr`}</td>
              <td>{asset.priority || 'Not available'}</td>
              {!compact && <td className="action-cell">{asset.recommendation || 'Not available'}</td>}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
