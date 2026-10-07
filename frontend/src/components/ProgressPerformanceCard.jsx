import { useState } from 'react';
import TrafficLight from './TrafficLight.jsx';

const defaultStages = [
  { name: 'Planning', value: 78, color: '#facc15', target: '78% complete', description: 'Surveys, CAD schematics & geotechnical risk assessment' },
  { name: 'Groundwork', value: 60, color: '#facc15', target: '60% complete', description: 'Drainage excavation, sub-base compaction & utility conduits' },
  { name: 'Structures', value: 45, color: '#facc15', target: '45% complete', description: 'Concrete bridge piers, retaining walls & steel girders' },
  { name: 'Paving', value: 30, color: '#facc15', target: '30% complete', description: 'Asphalt binder course, friction wear layer & lane striping' },
];

export default function ProgressPerformanceCard({
  title = 'Progress & Performance',
  description,
  stages = defaultStages,
}) {
  const [activeStage, setActiveStage] = useState(null);

  const defaultText =
    description ||
    'Comprehensive lifecycle monitoring across road infrastructure development stages. Predictive condition metrics evaluate structural health and environmental stress factors from initial foundation groundwork to final friction wear paving.';

  return (
    <section className="progress-perf-card">
      <div className="progress-perf-body">
        {/* Left Side: Styled Bar Chart (matching Image 3) */}
        <div className="progress-chart-container">
          <div className="progress-bar-chart-card">
            {/* Y-Axis Labels */}
            <div className="chart-y-axis">
              <span>80</span>
              <span>60</span>
              <span>40</span>
              <span>20</span>
              <span>0</span>
            </div>

            {/* Grid & Bars Area */}
            <div className="chart-plot-area">
              {/* Horizontal Grid lines */}
              <div className="chart-grid-line line-80" />
              <div className="chart-grid-line line-60" />
              <div className="chart-grid-line line-40" />
              <div className="chart-grid-line line-20" />
              <div className="chart-grid-line line-0" />

              {/* Bars Columns */}
              <div className="chart-bars-group">
                {stages.map((stage) => {
                  // Normalize value relative to max 80 scale (so 80 = 100% height)
                  const heightPercent = Math.min(100, Math.max(8, (stage.value / 80) * 100));
                  const isHovered = activeStage?.name === stage.name;

                  return (
                    <div
                      key={stage.name}
                      className={`chart-bar-col ${isHovered ? 'bar-active' : ''}`}
                      onMouseEnter={() => setActiveStage(stage)}
                      onMouseLeave={() => setActiveStage(null)}
                    >
                      <div className="bar-track">
                        <div
                          className="bar-fill"
                          style={{
                            height: `${heightPercent}%`,
                            backgroundColor: stage.color || '#facc15',
                          }}
                        >
                          <span className="bar-tooltip">
                            {stage.name}: {stage.value}%
                          </span>
                        </div>
                      </div>
                      <span className="bar-label">{stage.name}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {activeStage && (
            <div className="active-stage-callout">
              <strong>{activeStage.name} ({activeStage.value}%):</strong> {activeStage.description}
            </div>
          )}
        </div>

        {/* Center/Right: Heading & Description Text */}
        <div className="progress-content-col">
          <span className="progress-eyebrow">MILESTONES & CONDITION METRICS</span>
          <h2 className="progress-title">{title}</h2>
          <p className="progress-description">{defaultText}</p>

          <div className="progress-summary-chips">
            <div className="perf-chip">
              <span className="chip-label">Target Completion</span>
              <strong className="chip-val">Q4 2026</strong>
            </div>
            <div className="perf-chip">
              <span className="chip-label">Avg Structural Health</span>
              <strong className="chip-val">74.2 / 100</strong>
            </div>
            <div className="perf-chip">
              <span className="chip-label">Active Workzones</span>
              <strong className="chip-val">18 Corridors</strong>
            </div>
          </div>
        </div>

        {/* Rightmost: Vertical Traffic Light on Post (matching Image 3) */}
        <div className="progress-traffic-light-col">
          <TrafficLight
            orientation="vertical"
            active="all"
            size="md"
            withPole={true}
          />
        </div>
      </div>

      {/* Bottom Road Surface Strip with Yellow Curb (matching Image 3) */}
      <div className="progress-perf-bottom-curb" aria-hidden="true">
        <div className="curb-yellow-stripe" />
        <div className="curb-asphalt-bed" />
      </div>
    </section>
  );
}
