export default function FeatureImportanceChart({ data = [] }) {
  if (!data.length) return <div className="chart-empty">Feature importance is not returned by the backend analytics endpoint.</div>;
  return (
    <div className="importance-list">
      {data.map((item) => <div className="importance-row" key={item.name}><span>{item.name}</span><div><i style={{ width: `${Math.min(100, Math.max(0, item.value * 100))}%` }} /></div><strong>{item.value.toFixed(3)}</strong></div>)}
    </div>
  );
}
