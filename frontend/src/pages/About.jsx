import TrafficLight from '../components/TrafficLight.jsx';
import ProjectOverviewCard from '../components/ProjectOverviewCard.jsx';
import ProgressPerformanceCard from '../components/ProgressPerformanceCard.jsx';

const objectives = [
  'Predict the likelihood of road corridor & bridge failures',
  'Estimate remaining useful asset lifecycle (RUL in years)',
  'Surface critical pavement distress & structural corrosion factors',
  'Cluster highway assets by wear patterns and traffic intensity',
  'Prioritize urgent road maintenance to prevent transit bottlenecks',
  'Provide automated engineering recommendations and resurfacing plans',
];

const concepts = [
  ['Classification', 'Estimates failure probability from pavement condition, load stress, and environmental wear.'],
  ['Regression', 'Predicts remaining useful life as a continuous temporal metric.'],
  ['Clustering', 'Groups similar highway asset profiles using unsupervised K-Means.'],
  ['PCA & Dimensionality', 'Condenses high-dimensional asset telemetry for structural grouping.'],
  ['Feature Engineering', 'Prepares traffic density, rainfall, and material stress inputs for predictive modeling.'],
  ['Recommendation Engine', 'Maps the predicted risk matrix to immediate engineering interventions.'],
];

export default function About() {
  return (
    <div className="page-stack about-page">
      {/* Road Infrastructure Project Overview (Image 2 style) */}
      <ProjectOverviewCard
        title="Road Infrastructure Project"
        description="A specialized intelligent transportation research project delivering machine-learning predictive maintenance for roads, highways, bridges, and municipal transit assets. By transforming real-time condition telemetry into actionable risk forecasts, municipal departments can eliminate dangerous road failures before they emerge."
      />

      {/* Progress & Performance Milestones (Image 3 style) */}
      <ProgressPerformanceCard
        title="Engineering Progress & Lifecycle"
        description="Tracking milestones from early stage geotechnical survey planning through sub-base groundwork, structural pier erection, and final wearing course asphalt paving."
      />

      <section className="panel about-copy">
        <div className="section-heading">
          <div>
            <span className="eyebrow">CIVIL ENGINEERING SCOPE</span>
            <h2>Project Mission</h2>
          </div>
        </div>
        <p>
          Road and transit infrastructure such as asphalt highways, concrete overpasses, suspension bridges, drainage culverts, and electrical corridors deteriorate progressively under heavy axle loads, freeze-thaw weathering, and delayed maintenance. The Road Infrastructure Failure Predictor applies advanced ML models to predict risk scores and optimize resource deployment.
        </p>
      </section>

      <section className="panel">
        <div className="section-heading">
          <div>
            <span className="eyebrow">PROJECT DELIVERABLES</span>
            <h2>Core Objectives</h2>
          </div>
        </div>
        <div className="objective-grid">
          {objectives.map((item, index) => (
            <div className="objective-item" key={item}>
              <span className="objective-num">{String(index + 1).padStart(2, '0')}</span>
              <strong>{item}</strong>
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="section-heading">
          <div>
            <span className="eyebrow">ALGORITHMIC FRAMEWORK</span>
            <h2>AI / ML Architecture</h2>
          </div>
        </div>
        <div className="concept-grid">
          {concepts.map(([title, description]) => (
            <article className="concept-card" key={title}>
              <span className="concept-mark">✦</span>
              <h3>{title}</h3>
              <p>{description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="panel">
        <div className="section-heading">
          <div>
            <span className="eyebrow">ENGINEERING STACK</span>
            <h2>Technology Architecture</h2>
          </div>
        </div>
        <div className="stack-grid">
          <div>
            <span>Frontend Interface</span>
            <strong>React 18 · Vite · Recharts · CSS3 Grid</strong>
          </div>
          <div>
            <span>Backend Gateway</span>
            <strong>FastAPI · Python 3.10+ · Uvicorn</strong>
          </div>
          <div>
            <span>Machine Learning</span>
            <strong>Scikit-Learn · Pandas · NumPy</strong>
          </div>
          <div>
            <span>Data Repository</span>
            <strong>Road Infrastructure Dataset · SQLite</strong>
          </div>
        </div>
      </section>

      <section className="future-panel">
        <div>
          <span className="eyebrow">ROADMAP & ADVANCED SENSORS</span>
          <h2>Future Capabilities</h2>
        </div>
        <div className="future-chips">
          <span>Highway Weigh-in-Motion (WIM)</span>
          <span>GIS Satellite Road Mapping</span>
          <span>Drone Crack Photogrammetry</span>
          <span>IoT Bridge Vibration Sensors</span>
          <span>Automated Work-Order Dispatch</span>
        </div>
      </section>
    </div>
  );
}
