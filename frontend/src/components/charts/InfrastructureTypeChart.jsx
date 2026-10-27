import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload || !payload.length) return null;
  const row = payload[0]?.payload || {};
  const total = row.total || ((row.low || 0) + (row.medium || 0) + (row.high || 0));
  return (
    <div
      style={{
        backgroundColor: '#0f1722',
        border: '1px solid #22344a',
        borderRadius: '8px',
        padding: '10px 14px',
        color: '#ffffff',
        fontSize: '12px',
        boxShadow: '0 8px 24px rgba(0, 0, 0, 0.45)',
      }}
    >
      <div style={{ fontWeight: 700, marginBottom: '6px', color: '#fecb00', borderBottom: '1px solid #22344a', paddingBottom: '4px' }}>
        {label || row.name || row.type}
      </div>
      <div style={{ display: 'grid', gap: '4px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px' }}>
          <span style={{ color: '#94a3b8' }}>Total Assets:</span>
          <strong>{total?.toLocaleString()}</strong>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px' }}>
          <span style={{ color: '#ef4444', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', backgroundColor: '#ef4444', display: 'inline-block' }} /> High Risk:
          </span>
          <strong>{row.high?.toLocaleString()} ({total ? Math.round((row.high / total) * 100) : 0}%)</strong>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px' }}>
          <span style={{ color: '#facc15', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', backgroundColor: '#facc15', display: 'inline-block' }} /> Medium Risk:
          </span>
          <strong>{row.medium?.toLocaleString()} ({total ? Math.round((row.medium / total) * 100) : 0}%)</strong>
        </div>
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: '16px' }}>
          <span style={{ color: '#10b981', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', backgroundColor: '#10b981', display: 'inline-block' }} /> Low Risk:
          </span>
          <strong>{row.low?.toLocaleString()} ({total ? Math.round((row.low / total) * 100) : 0}%)</strong>
        </div>
      </div>
    </div>
  );
}

export default function InfrastructureTypeChart({ data = [], onRetry }) {
  if (!data || !data.length) {
    return (
      <div className="chart-empty" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', minHeight: '180px', gap: '8px', color: '#94a3b8', fontSize: '12px' }}>
        <span>Risk distribution temporarily unavailable</span>
        {onRetry && (
          <button
            type="button"
            onClick={onRetry}
            style={{
              background: 'transparent',
              border: '1px solid #22344a',
              borderRadius: '4px',
              color: '#fecb00',
              padding: '4px 10px',
              fontSize: '11px',
              cursor: 'pointer',
            }}
          >
            Retry Loading
          </button>
        )}
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="chart-area" style={{ height: '185px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            layout="vertical"
            data={data}
            margin={{ top: 5, right: 12, left: 10, bottom: 5 }}
          >
            <CartesianGrid stroke="#22344a" horizontal={false} strokeDasharray="3 3" />
            <XAxis type="number" tickLine={false} axisLine={{ stroke: '#22344a' }} tick={{ fill: '#94a3b8', fontSize: 10 }} />
            <YAxis
              type="category"
              dataKey="name"
              tickLine={false}
              axisLine={{ stroke: '#22344a' }}
              tick={{ fill: '#cbd5e1', fontSize: 10 }}
              width={82}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="low" name="Low Risk" stackId="a" fill="#10b981" />
            <Bar dataKey="medium" name="Medium Risk" stackId="a" fill="#facc15" />
            <Bar dataKey="high" name="High Risk" stackId="a" fill="#ef4444" radius={[0, 3, 3, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '14px',
          marginTop: '6px',
          fontSize: '11px',
          color: '#94a3b8',
        }}
      >
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '5px' }}>
          <i style={{ width: 8, height: 8, borderRadius: 2, backgroundColor: '#10b981', display: 'inline-block' }} /> Low Risk
        </span>
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '5px' }}>
          <i style={{ width: 8, height: 8, borderRadius: 2, backgroundColor: '#facc15', display: 'inline-block' }} /> Medium Risk
        </span>
        <span style={{ display: 'inline-flex', alignItems: 'center', gap: '5px' }}>
          <i style={{ width: 8, height: 8, borderRadius: 2, backgroundColor: '#ef4444', display: 'inline-block' }} /> High Risk
        </span>
      </div>
    </div>
  );
}

