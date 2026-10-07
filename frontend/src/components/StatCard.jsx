export default function StatCard({ label, value, note, icon, tone = 'blue' }) {
  return (
    <article className="stat-card">
      <div className={`stat-icon stat-${tone}`} aria-hidden="true">{icon}</div>
      <div className="stat-copy">
        <span className="stat-label">{label}</span>
        <strong className="stat-value">{value}</strong>
        {note && <span className="stat-note">{note}</span>}
      </div>
    </article>
  );
}
