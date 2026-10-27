import ProjectOverviewCard from '../components/ProjectOverviewCard.jsx';
import ProgressPerformanceCard from '../components/ProgressPerformanceCard.jsx';

const objectives = [
  'Monitor 50,000 civil infrastructure records strictly within the Pune municipal boundary (PMC & PCMC).',
  'Predict the likelihood of road corridor, bridge, and pipeline failures using supervised GBDT & Random Forest models.',
  'Estimate non-negative Remaining Useful Life (RUL in days) with physics-constrained degradation models.',
  'Provide a Pune-focused interactive GIS monitoring interface with risk-differentiated telemetry markers.',
  'Empower citizens and engineers to report field damage with photo uploads, CV analysis, and proximity asset linking.',
  'Prioritize urgent maintenance in a dynamic Priority Queue combining predictive AI with verified damage reports.',
];

const concepts = [
  ['Supervised Classification', 'Estimates failure probability from pavement condition, corrosion, load stress, and environmental wear.'],
  ['Non-Negative Regression', 'Predicts remaining useful life as a continuous temporal metric bounded at 0.0 (end-of-life).'],
  ['Computer Vision Inspection', 'Processes road distress photos using OpenCV edge detection and morphology to calculate Road Damage Index (RDI).'],
  ['Spatial Proximity Linking', 'Calculates distance to nearest infrastructure asset within 400m to associate field reports with monitored inventory.'],
  ['Constrained Optimization', 'Solves 0/1 Knapsack maintenance scheduling via Hill Climbing, Beam Search, and Tabu Search.'],
  ['Zero-Data-Leakage Protocol', 'Strict 80/20 train/test split isolation where imputers, encoders, and scalers learn only from training sets.'],
];

export default function About() {
  return (
    <div className="page-stack about-page">
      {/* Pune Civil Infrastructure Project Overview */}
      <ProjectOverviewCard
        title="Pune Urban Infrastructure AI Predictive Maintenance Platform"
        description="A specialized municipal civil engineering platform delivering AI-driven predictive maintenance and GIS monitoring across 50,000 monitored road segments, bridge approaches, and culvert approaches in the Pune Metropolitan area. By combining sensory metrics, physics-based degradation models, computer vision inspection, and field damage reports, the platform empowers city engineers to prevent dangerous infrastructure failures."
      />

      {/* Dataset Provenance & Synthetic Benchmark Notice */}
      <section className="panel provenance-panel">
        <div className="section-heading">
          <div>
            <span className="eyebrow">DATASET PROVENANCE & TRANSPARENCY NOTICE</span>
            <h2>50,000 Record Pune Expanded Road Infrastructure Dataset</h2>
          </div>
          <span className="small-tag verified-tag">Pune Metropolitan Benchmark</span>
        </div>
        <div className="provenance-content">
          <p>
            <strong>Explicit Transparency Statement:</strong> The current active infrastructure dataset of 50,000 records
            combines authentic Pune municipal road network names and 36 verified localities with physically grounded,
            model-derived synthetic degradation telemetry (including pavement age, corrosion, rainfall, usage intensity, and maintenance history).
          </p>
          <div className="provenance-disclaimer">
            ⚠️ <strong>Academic & Operational Transparency:</strong> This dataset distinguishes real reference seeds (Pune arterial corridors,
            localities, road classes, approximate coordinates) from model-derived fields (failure labels, RUL days, structural scores).
            Synthetic labels and RUL values are generated for predictive benchmarking and should not be cited as empirical municipal observations.
          </div>
        </div>
      </section>

      {/* Progress & Performance Milestones */}
      <ProgressPerformanceCard
        title="Pune Metropolitan Civil Development Milestones"
        description="Tracking lifecycle stages across Pune wards from geotechnical survey planning through sub-base groundwork, bridge pier erection, drainage culvert waterproofing, and final asphalt friction wear paving."
      />

      {/* Core Objectives */}
      <section className="panel">
        <div className="section-heading">
          <div>
            <span className="eyebrow">PROJECT DELIVERABLES</span>
            <h2>Core Platform Objectives</h2>
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

      {/* Algorithmic Framework */}
      <section className="panel">
        <div className="section-heading">
          <div>
            <span className="eyebrow">ALGORITHMIC FRAMEWORK</span>
            <h2>AI / ML & Optimization Architecture</h2>
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

      {/* Engineering Stack */}
      <section className="panel">
        <div className="section-heading">
          <div>
            <span className="eyebrow">ENGINEERING STACK</span>
            <h2>Technology Architecture & MLOps</h2>
          </div>
        </div>
        <div className="stack-grid">
          <div>
            <span>Frontend GIS & Web UI</span>
            <strong>React 18 · Vite · Leaflet GIS · Recharts</strong>
          </div>
          <div>
            <span>Backend Gateway & APIs</span>
            <strong>FastAPI · Python 3.10+ · SQLite · Uvicorn</strong>
          </div>
          <div>
            <span>Machine Learning & MLOps</span>
            <strong>Scikit-Learn · MLflow · FLAML AutoML · Joblib</strong>
          </div>
          <div>
            <span>Computer Vision & GIS</span>
            <strong>OpenCV · Canny Edge Detection · Geo Bounds</strong>
          </div>
        </div>
      </section>
    </div>
  );
}
