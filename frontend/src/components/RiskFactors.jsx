import { humanize } from '../utils/formatters.js';

export default function RiskFactors({ factors }) {
  const entries = Object.entries(factors || {});
  return (
    <section className="panel">
      <div className="section-heading"><div><span className="eyebrow">MODEL INPUT CONTEXT</span><h2>Risk factors</h2></div></div>
      {entries.length ? (
        <div className="factor-list">
          {entries.map(([name, value]) => (
            <div className="factor-row" key={name}><span>{humanize(name)}</span><strong>{value ?? 'Not available'}</strong></div>
          ))}
        </div>
      ) : <p className="muted">The prediction response did not include risk factor details.</p>}
    </section>
  );
}
