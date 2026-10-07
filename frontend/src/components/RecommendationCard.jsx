export default function RecommendationCard({ recommendation, priority }) {
  return (
    <section className="recommendation-card">
      <div className="recommendation-icon" aria-hidden="true">✦</div>
      <div>
        <span className="eyebrow">MAINTENANCE GUIDANCE {priority ? `· ${priority} PRIORITY` : ''}</span>
        <h2>Recommended action</h2>
        <p>{recommendation || 'No recommendation was included in the prediction response.'}</p>
      </div>
    </section>
  );
}
