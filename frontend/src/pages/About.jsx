const objectives = [
  'Predict the likelihood of infrastructure failure',
  'Estimate remaining useful life',
  'Surface condition factors for assessment',
  'Group assets by similar condition patterns',
  'Support maintenance prioritization',
  'Provide model-generated recommendations',
];

const concepts = [
  ['Classification', 'Estimates the probability of failure from asset condition and environment inputs.'],
  ['Regression', 'Estimates remaining useful life as a continuous value.'],
  ['Clustering', 'Groups similar asset profiles using K-Means.'],
  ['PCA', 'Reduces feature dimensions for a 2D view; coordinates are not currently exposed by the API.'],
  ['Feature engineering', 'Prepares condition and environment fields for machine-learning models.'],
  ['Recommendation engine', 'Maps the predicted risk level to a maintenance recommendation.'],
];

export default function About() {
  return (
    <div className="page-stack about-page">
      <div className="about-hero"><span className="eyebrow">AIML MINI PROJECT</span><h2>Smarter maintenance starts with better signals.</h2><p>AI Urban Infrastructure Failure Predictor brings asset condition data and machine learning together to support preventive maintenance decisions.</p><span className="about-hero-orbit orbit-one" /><span className="about-hero-orbit orbit-two" /></div>
      <section className="panel about-copy"><div className="section-heading"><div><span className="eyebrow">THE PROJECT</span><h2>About the project</h2></div></div><p>Urban infrastructure such as roads, bridges, pipelines, drainage systems, streetlights and electrical assets can deteriorate because of age, usage, environmental stress and insufficient maintenance. This project demonstrates how machine-learning models can estimate risk and help teams review assets before failures occur.</p></section>
      <section className="panel"><div className="section-heading"><div><span className="eyebrow">PROJECT GOALS</span><h2>Objectives</h2></div></div><div className="objective-grid">{objectives.map((item, index) => <div className="objective-item" key={item}><span>{String(index + 1).padStart(2, '0')}</span><strong>{item}</strong></div>)}</div></section>
      <section className="panel"><div className="section-heading"><div><span className="eyebrow">HOW IT WORKS</span><h2>AI / ML components</h2></div></div><div className="concept-grid">{concepts.map(([title, description]) => <article className="concept-card" key={title}><span className="concept-mark">✦</span><h3>{title}</h3><p>{description}</p></article>)}</div></section>
      <section className="panel"><div className="section-heading"><div><span className="eyebrow">BUILT WITH</span><h2>Technology stack</h2></div></div><div className="stack-grid"><div><span>Frontend</span><strong>React · Vite · Axios · Recharts</strong></div><div><span>Backend</span><strong>FastAPI · Python</strong></div><div><span>Machine learning</span><strong>Pandas · NumPy · Scikit-learn</strong></div><div><span>Storage</span><strong>CSV dataset · SQLite prediction history</strong></div></div></section>
      <section className="future-panel"><div><span className="eyebrow">NEXT POSSIBILITIES</span><h2>Future scope</h2></div><div className="future-chips"><span>IoT sensor integration</span><span>GIS / map views</span><span>Live monitoring</span><span>Mobile application</span><span>Expanded datasets</span></div></section>
    </div>
  );
}
