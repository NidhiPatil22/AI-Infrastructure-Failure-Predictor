import PuneInfrastructureMap from '../components/PuneInfrastructureMap.jsx';

export default function InfrastructureMapPage() {
  return (
    <div className="page-stack">
      <div className="map-page-hero">
        <div>
          <span className="eyebrow">PUNE METROPOLITAN INFRASTRUCTURE</span>
          <h1>Pune Civil Infrastructure GIS Monitor</h1>
          <p>
            Interactive GIS monitoring platform tracking 50,000 monitored road segments, bridge approaches, and culvert approaches
            strictly bounded within Pune city limits (PMC & PCMC). Select any infrastructure marker to inspect diagnostics,
            degradation telemetry, remaining useful life (RUL), and linked citizen damage inspection reports.
          </p>
        </div>
      </div>

      <section className="panel map-panel-container">
        <PuneInfrastructureMap />
      </section>
    </div>
  );
}
