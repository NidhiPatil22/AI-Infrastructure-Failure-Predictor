import TrafficLight from './TrafficLight.jsx';

export default function ProjectOverviewCard({
  title = 'Project Overview',
  description,
  metrics,
}) {
  const defaultText =
    description ||
    'Urban transportation corridors, bridges, and highway networks are subjected to structural fatigue, environmental weathering, and continuous vehicular load. This road infrastructure intelligence system predicts critical failure points, estimates remaining useful asset lifespan, and delivers proactive maintenance schedules to prevent transit disruption and preserve civil safety.';

  return (
    <section className="overview-card-container">
      {/* Left side: Scenic road, suspension bridge, and vertical traffic light */}
      <div className="overview-scenic-side">
        <svg
          className="overview-scenic-svg"
          viewBox="0 0 500 360"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          preserveAspectRatio="xMidYMid slice"
        >
          {/* Daytime Sky */}
          <rect width="500" height="360" fill="#6ba4e8" />

          {/* Clouds */}
          <path
            d="M 20 90 Q 50 60 90 70 Q 130 50 170 80 Q 210 65 240 90 Q 260 110 240 130 L 10 130 Z"
            fill="#e2eefe"
            opacity="0.85"
          />
          <path
            d="M 120 70 Q 150 40 190 55 Q 230 45 260 70 Q 280 90 260 110 L 120 110 Z"
            fill="#ffffff"
            opacity="0.9"
          />
          <path
            d="M 300 110 Q 340 70 390 90 Q 430 75 460 100 Q 480 120 460 140 L 290 140 Z"
            fill="#e2eefe"
            opacity="0.75"
          />

          {/* Distant Mountains / Rolling Hills */}
          <path
            d="M 0 210 Q 110 140 220 180 Q 340 150 450 190 L 500 200 L 500 360 L 0 360 Z"
            fill="#5b807a"
          />
          <path
            d="M 0 230 Q 140 180 270 215 Q 380 185 500 225 L 500 360 L 0 360 Z"
            fill="#426660"
          />

          {/* Trees / vegetation on hillside */}
          <path
            d="M 230 215 Q 240 200 255 208 Q 270 198 285 210 Q 295 205 310 215 Z"
            fill="#2c4d3b"
          />

          {/* Curved Asphalt Highway leading to Bridge */}
          <path
            d="M 0 225 Q 110 235 200 280 L 200 360 L 0 360 Z"
            fill="#334155"
          />
          {/* Yellow Road Centerline Marking */}
          <path
            d="M 0 242 Q 105 255 190 295"
            stroke="#facc15"
            strokeWidth="4"
            fill="none"
          />
          {/* Outer road white edge line */}
          <path
            d="M 0 228 Q 110 238 198 282"
            stroke="#ffffff"
            strokeWidth="2.5"
            fill="none"
          />
          <path
            d="M 15 220 L 17 235 M 40 222 L 42 237 M 95 230 L 98 245"
            stroke="#e2e8f0"
            strokeWidth="2"
          />

          {/* --- Suspension Bridge --- */}
          {/* Water reflection / dark bay underneath */}
          <rect x="180" y="310" width="320" height="50" fill="#132338" />

          {/* Bridge Roadway Deck */}
          <rect x="160" y="275" width="340" height="16" fill="#475569" />
          <line x1="160" y1="275" x2="500" y2="275" stroke="#cbd5e1" strokeWidth="4" />

          {/* Main Suspension Tower 1 */}
          <g className="bridge-tower-1">
            {/* Vertical Columns */}
            <rect x="200" y="165" width="16" height="150" fill="#94a3b8" />
            <rect x="245" y="165" width="16" height="150" fill="#94a3b8" />
            {/* Top horizontal beam */}
            <rect x="196" y="165" width="69" height="12" fill="#cbd5e1" />
            {/* Middle horizontal beam */}
            <rect x="200" y="220" width="61" height="10" fill="#cbd5e1" />
            {/* Lower deck support beam */}
            <rect x="196" y="270" width="69" height="14" fill="#64748b" />
            {/* Tower Cross Bracing (X truss) */}
            <line x1="216" y1="177" x2="245" y2="220" stroke="#cbd5e1" strokeWidth="3" />
            <line x1="245" y1="177" x2="216" y2="220" stroke="#cbd5e1" strokeWidth="3" />
            <line x1="216" y1="230" x2="245" y2="270" stroke="#cbd5e1" strokeWidth="3" />
            <line x1="245" y1="230" x2="216" y2="270" stroke="#cbd5e1" strokeWidth="3" />
            {/* Tower Piers into water */}
            <rect x="198" y="315" width="20" height="45" fill="#334155" />
            <rect x="243" y="315" width="20" height="45" fill="#334155" />
          </g>

          {/* Main Suspension Tower 2 */}
          <g className="bridge-tower-2">
            <rect x="380" y="200" width="13" height="120" fill="#64748b" />
            <rect x="415" y="200" width="13" height="120" fill="#64748b" />
            <rect x="376" y="200" width="56" height="9" fill="#94a3b8" />
            <rect x="380" y="240" width="48" height="8" fill="#94a3b8" />
            <line x1="393" y1="209" x2="415" y2="240" stroke="#94a3b8" strokeWidth="2.5" />
            <line x1="415" y1="209" x2="393" y2="240" stroke="#94a3b8" strokeWidth="2.5" />
            <rect x="378" y="315" width="17" height="45" fill="#334155" />
            <rect x="413" y="315" width="17" height="45" fill="#334155" />
          </g>

          {/* Main Suspension Cables (Graceful swoop) */}
          <path
            d="M 160 270 Q 185 200 208 165"
            stroke="#e2e8f0"
            strokeWidth="4"
            fill="none"
          />
          <path
            d="M 253 165 Q 315 260 387 200"
            stroke="#e2e8f0"
            strokeWidth="4"
            fill="none"
          />
          <path
            d="M 421 200 Q 460 250 500 275"
            stroke="#cbd5e1"
            strokeWidth="3.5"
            fill="none"
          />

          {/* Vertical Hanger Cables */}
          <line x1="280" y1="225" x2="280" y2="275" stroke="#cbd5e1" strokeWidth="1.5" />
          <line x1="300" y1="242" x2="300" y2="275" stroke="#cbd5e1" strokeWidth="1.5" />
          <line x1="320" y1="248" x2="320" y2="275" stroke="#cbd5e1" strokeWidth="1.5" />
          <line x1="340" y1="244" x2="340" y2="275" stroke="#cbd5e1" strokeWidth="1.5" />
          <line x1="360" y1="228" x2="360" y2="275" stroke="#cbd5e1" strokeWidth="1.5" />
          <line x1="440" y1="230" x2="440" y2="275" stroke="#94a3b8" strokeWidth="1.5" />
          <line x1="460" y1="248" x2="460" y2="275" stroke="#94a3b8" strokeWidth="1.5" />
        </svg>

        {/* Foreground Traffic Light on Pole (Image 2 style) */}
        <div className="overview-traffic-light-foreground">
          <TrafficLight
            orientation="vertical"
            active="all"
            size="lg"
            withPole={true}
          />
        </div>
      </div>

      {/* Right side: Dark navy container with bold yellow title & white description */}
      <div className="overview-content-side">
        <div className="overview-text-block">
          <span className="overview-eyebrow">SYSTEM ARCHITECTURE & ROAD SAFETY</span>
          <h2 className="overview-title">{title}</h2>
          <p className="overview-description">{defaultText}</p>

          <div className="overview-badges">
            <span className="road-tag">
              <i className="tag-dot green" /> Highway Corridors
            </span>
            <span className="road-tag">
              <i className="tag-dot yellow" /> Bridge Inspection
            </span>
            <span className="road-tag">
              <i className="tag-dot red" /> Real-time Alerting
            </span>
          </div>

          {metrics && (
            <div className="overview-quick-metrics">
              {metrics.map((m, idx) => (
                <div key={idx} className="overview-metric-item">
                  <span className="metric-num">{m.value}</span>
                  <span className="metric-lbl">{m.label}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Yellow bottom-right triangle accent (Image 2 style) */}
        <div className="overview-yellow-corner-accent" aria-hidden="true" />
      </div>
    </section>
  );
}
