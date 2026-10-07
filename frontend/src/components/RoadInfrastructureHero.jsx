import { Link } from 'react-router-dom';
import TrafficLight from './TrafficLight.jsx';

export default function RoadInfrastructureHero() {
  return (
    <div className="road-hero-container">
      {/* Yellow top and left framing border */}
      <div className="road-hero-yellow-frame" aria-hidden="true">
        <div className="frame-top-bar" />
        <div className="frame-left-bar" />
        <div className="frame-corner" />
      </div>

      {/* Main Content Area */}
      <div className="road-hero-content">
        {/* Left Side: Traffic Light + ROAD INFRASTRUCTURE PROJECT */}
        <div className="road-hero-left">
          <div className="road-hero-signal-mount">
            <TrafficLight
              orientation="horizontal"
              active="all"
              size="md"
              withMount={true}
              className="hero-traffic-light"
            />
          </div>

          <div className="road-hero-typography">
            <h1 className="road-hero-title">
              <span className="road-word-road">R O A D</span>
              <span className="road-word-infra">INFRASTRUCTURE</span>
              <span className="road-word-project">PROJECT</span>
            </h1>
            <p className="road-hero-subtitle">
              Planning · Construction · Progress · Impact
            </p>
          </div>

          <div className="road-hero-meta">
            <div className="hero-status-pill">
              <span className="hero-status-dot" />
              <span>AI Predictive Maintenance System</span>
            </div>
            <div className="road-hero-actions">
              <Link to="/predict" className="hero-btn-primary">
                <span>＋</span> Run Prediction
              </Link>
              <Link to="/priority" className="hero-btn-secondary">
                View Maintenance Queue
              </Link>
            </div>
          </div>
        </div>

        {/* Diagonal Yellow Divider Accent */}
        <div className="road-hero-diagonal-divider" aria-hidden="true" />

        {/* Right Side: Highway Overpass & Cars Illustration */}
        <div className="road-hero-right" aria-label="Road infrastructure elevated highway illustration">
          <svg
            className="road-highway-svg"
            viewBox="0 0 600 450"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            preserveAspectRatio="xMidYMid meet"
          >
            {/* Background elements: sky & light gantries */}
            <rect width="600" height="450" fill="#0f1724" />

            {/* Overhead highway lighting / gantry poles */}
            <path d="M 430 0 L 430 140 M 438 0 L 438 140" stroke="#ffffff" strokeWidth="3" opacity="0.8" />
            <path d="M 400 30 L 468 30" stroke="#ffffff" strokeWidth="3" opacity="0.8" />
            <path d="M 330 0 L 330 90 M 520 0 L 520 120" stroke="#ffffff" strokeWidth="2" opacity="0.4" />
            <path d="M 330 90 Q 340 100 350 95" stroke="#ffffff" strokeWidth="2" fill="none" opacity="0.5" />
            <path d="M 520 120 Q 530 130 540 125" stroke="#ffffff" strokeWidth="2" fill="none" opacity="0.5" />

            {/* Background Highway Pillars (Dark concrete supports) */}
            <rect x="330" y="240" width="22" height="130" rx="4" fill="#334155" />
            <rect x="420" y="270" width="24" height="120" rx="4" fill="#334155" />
            <rect x="220" y="260" width="20" height="110" rx="4" fill="#1e293b" />
            <rect x="520" y="320" width="24" height="90" rx="4" fill="#1e293b" />

            {/* Pillar footings */}
            <ellipse cx="341" cy="370" rx="16" ry="6" fill="#1e293b" />
            <ellipse cx="432" cy="390" rx="18" ry="7" fill="#1e293b" />

            {/* --- Lower Curved Overpass Deck --- */}
            {/* Underside shadow */}
            <path
              d="M 180 280 Q 280 270 420 300 L 420 328 Q 280 298 180 308 Z"
              fill="#192333"
            />
            {/* Lower Road Surface */}
            <path
              d="M 175 270 Q 280 260 425 290 Q 480 305 560 340 L 555 375 Q 470 340 415 320 Q 275 290 170 300 Z"
              fill="#64748b"
            />
            {/* Lower guardrail */}
            <path
              d="M 175 270 Q 280 260 425 290 Q 480 305 560 340"
              stroke="#94a3b8"
              strokeWidth="5"
              fill="none"
            />
            {/* Lower lane markings */}
            <path
              d="M 185 285 Q 285 275 420 305 Q 475 320 550 355"
              stroke="#ffffff"
              strokeWidth="2.5"
              strokeDasharray="9 7"
              fill="none"
            />

            {/* Car on lower level: Orange car */}
            <g transform="translate(195, 268) rotate(5)">
              <rect x="0" y="0" width="26" height="15" rx="5" fill="#f97316" />
              <rect x="6" y="2" width="13" height="11" rx="2" fill="#fed7aa" />
              <circle cx="5" cy="1" r="2.5" fill="#0f172a" />
              <circle cx="21" cy="1" r="2.5" fill="#0f172a" />
              <circle cx="5" cy="14" r="2.5" fill="#0f172a" />
              <circle cx="21" cy="14" r="2.5" fill="#0f172a" />
            </g>

            {/* --- Main Upper Sweeping Highway Overpass --- */}
            {/* Overpass Bridge Shadow */}
            <path
              d="M 270 200 Q 380 215 480 280 Q 530 320 540 450 L 515 450 Q 505 335 460 295 Q 365 235 265 220 Z"
              fill="#0d141e"
              opacity="0.7"
            />
            {/* Concrete Underbody / Structure */}
            <path
              d="M 270 195 Q 380 210 480 275 Q 545 325 565 450 L 525 450 Q 505 340 450 295 Q 360 230 260 215 Z"
              fill="#475569"
            />
            {/* Overpass Asphalt Road Deck */}
            <path
              d="M 285 180 Q 395 200 495 260 Q 565 310 590 450 L 545 450 Q 520 325 460 275 Q 375 215 275 195 Z"
              fill="#94a3b8"
            />
            {/* Outer Concrete Guardrail (Light Gray) */}
            <path
              d="M 285 180 Q 395 200 495 260 Q 565 310 590 450"
              stroke="#cbd5e1"
              strokeWidth="6"
              fill="none"
            />
            {/* Inner Guardrail */}
            <path
              d="M 275 195 Q 375 215 460 275 Q 520 325 545 450"
              stroke="#64748b"
              strokeWidth="5"
              fill="none"
            />

            {/* Center Dashed White Road Line */}
            <path
              d="M 280 188 Q 385 208 478 268 Q 542 318 568 450"
              stroke="#ffffff"
              strokeWidth="3.5"
              strokeDasharray="14 10"
              fill="none"
            />

            {/* Additional Highway ramp crossing down center */}
            <path
              d="M 420 0 L 420 180 Q 425 240 460 280"
              stroke="#cbd5e1"
              strokeWidth="4"
              fill="none"
              opacity="0.4"
            />

            {/* --- Stylized Vehicles on the Highway --- */}
            {/* 1. Dark Grey/Cyan Car on upper ramp */}
            <g transform="translate(345, 185) rotate(12)">
              <rect x="0" y="0" width="28" height="15" rx="4" fill="#3b82f6" />
              <rect x="7" y="2" width="13" height="11" rx="2" fill="#bfdbfe" />
              <circle cx="5" cy="0" r="2.5" fill="#0f172a" />
              <circle cx="23" cy="0" r="2.5" fill="#0f172a" />
              <circle cx="5" cy="15" r="2.5" fill="#0f172a" />
              <circle cx="23" cy="15" r="2.5" fill="#0f172a" />
            </g>

            {/* 2. Blue Truck / Van */}
            <g transform="translate(425, 218) rotate(22)">
              <rect x="0" y="0" width="34" height="18" rx="4" fill="#0284c7" />
              <rect x="22" y="2" width="9" height="14" rx="2" fill="#bae6fd" />
              <circle cx="6" cy="0" r="3" fill="#0f172a" />
              <circle cx="27" cy="0" r="3" fill="#0f172a" />
              <circle cx="6" cy="18" r="3" fill="#0f172a" />
              <circle cx="27" cy="18" r="3" fill="#0f172a" />
            </g>

            {/* 3. Red Sedan */}
            <g transform="translate(485, 270) rotate(34)">
              <rect x="0" y="0" width="28" height="16" rx="5" fill="#ef4444" />
              <rect x="7" y="2" width="13" height="12" rx="2" fill="#fecaca" />
              <circle cx="5" cy="0" r="2.5" fill="#0f172a" />
              <circle cx="23" cy="0" r="2.5" fill="#0f172a" />
              <circle cx="5" cy="16" r="2.5" fill="#0f172a" />
              <circle cx="23" cy="16" r="2.5" fill="#0f172a" />
            </g>

            {/* 4. Purple Hatchback */}
            <g transform="translate(525, 335) rotate(55)">
              <rect x="0" y="0" width="27" height="16" rx="5" fill="#a855f7" />
              <rect x="7" y="2" width="12" height="12" rx="2" fill="#f3e8ff" />
              <circle cx="5" cy="0" r="2.5" fill="#0f172a" />
              <circle cx="22" cy="0" r="2.5" fill="#0f172a" />
              <circle cx="5" cy="16" r="2.5" fill="#0f172a" />
              <circle cx="22" cy="16" r="2.5" fill="#0f172a" />
            </g>

            {/* 5. Green Sports Car */}
            <g transform="translate(555, 395) rotate(75)">
              <rect x="0" y="0" width="28" height="15" rx="5" fill="#22c55e" />
              <rect x="7" y="2" width="13" height="11" rx="2" fill="#bbf7d0" />
              <circle cx="5" cy="0" r="2.5" fill="#0f172a" />
              <circle cx="23" cy="0" r="2.5" fill="#0f172a" />
              <circle cx="5" cy="15" r="2.5" fill="#0f172a" />
              <circle cx="23" cy="15" r="2.5" fill="#0f172a" />
            </g>

            {/* Bottom Asphalt Highway Road with White Markings */}
            <g className="road-bottom-markings">
              <rect x="0" y="420" width="600" height="30" fill="#0f172a" />
              {/* White lane markings / pedestrian dash bar */}
              <rect x="35" y="426" width="55" height="12" rx="5" fill="#f8fafc" />
              <rect x="135" y="426" width="55" height="12" rx="5" fill="#f8fafc" />
              <rect x="235" y="426" width="55" height="12" rx="5" fill="#f8fafc" />
              <rect x="335" y="426" width="55" height="12" rx="5" fill="#f8fafc" />
              <rect x="435" y="426" width="55" height="12" rx="5" fill="#f8fafc" />
            </g>
          </svg>
        </div>
      </div>

      {/* Bottom Road Surface Strip with White Dashes and Yellow Trim */}
      <div className="road-hero-bottom-strip" aria-hidden="true">
        <div className="bottom-curb-yellow" />
        <div className="bottom-asphalt">
          <div className="asphalt-dash" />
          <div className="asphalt-dash" />
          <div className="asphalt-dash" />
          <div className="asphalt-dash" />
          <div className="asphalt-dash" />
          <div className="asphalt-dash" />
        </div>
      </div>
    </div>
  );
}
