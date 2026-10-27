import React from 'react';
import { humanize } from '../utils/formatters.js';

const FACTOR_CONFIG = {
  corrosion_level: {
    label: 'Corrosion Level',
    icon: '🧪',
    unit: '%',
    max: 100,
    hasBar: true,
    getSeverity: (val) => (val >= 60 ? 'critical' : val >= 35 ? 'warning' : 'safe'),
    format: (val) => `${val}%`,
  },
  structural_score: {
    label: 'Structural Score',
    icon: '🏗️',
    unit: '/ 100',
    max: 100,
    hasBar: true,
    getSeverity: (val) => (val < 40 ? 'critical' : val < 70 ? 'warning' : 'safe'),
    format: (val) => `${val} / 100`,
  },
  days_since_maintenance: {
    label: 'Days Since Maintenance',
    icon: '⏱️',
    unit: 'days',
    max: 730,
    hasBar: false,
    getSeverity: (val) => (val > 365 ? 'warning' : 'safe'),
    format: (val) => `${val} days`,
  },
  previous_failures: {
    label: 'Previous Failures',
    icon: '⚠️',
    unit: 'incidents',
    max: 5,
    hasBar: false,
    getSeverity: (val) => (val > 1 ? 'critical' : val === 1 ? 'warning' : 'safe'),
    format: (val) => (val === 1 ? '1 incident' : `${val} incidents`),
  },
  traffic_density: {
    label: 'Traffic Density',
    icon: '🚦',
    unit: '%',
    max: 100,
    hasBar: true,
    getSeverity: (val) => (val >= 75 ? 'warning' : 'safe'),
    format: (val) => `${val}%`,
  },
};

export default function RiskFactors({ factors }) {
  const entries = Object.entries(factors || {});

  return (
    <section className="panel risk-factors-panel">
      <div className="section-heading risk-factors-heading">
        <div className="risk-factors-header-left">
          <span className="eyebrow">MODEL INPUT CONTEXT</span>
          <div className="risk-factors-title-row">
            <h2>Risk factors</h2>
            {entries.length > 0 && (
              <span className="factor-count-pill">{entries.length} Indicators</span>
            )}
          </div>
        </div>
      </div>

      {entries.length ? (
        <div className="factor-list">
          {entries.map(([name, rawValue]) => {
            const config = FACTOR_CONFIG[name] || {
              label: humanize(name),
              icon: '📊',
              getSeverity: () => 'neutral',
              format: (val) => String(val),
              hasBar: false,
            };

            const numVal = Number(rawValue);
            const isValidNum = !isNaN(numVal);
            const severity = config.getSeverity ? config.getSeverity(numVal) : 'neutral';
            const displayVal = isValidNum && config.format ? config.format(numVal) : (rawValue ?? 'Not available');
            const percent = config.hasBar && isValidNum ? Math.min(100, Math.max(0, (numVal / (config.max || 100)) * 100)) : null;

            return (
              <div className={`factor-row factor-${severity}`} key={name}>
                <div className="factor-main">
                  <div className="factor-icon-wrap" aria-hidden="true">
                    {config.icon}
                  </div>
                  <div className="factor-content-col">
                    <div className="factor-label-row">
                      <span className="factor-label">{config.label || humanize(name)}</span>
                    </div>
                    {percent !== null && (
                      <div className="factor-mini-bar-track" title={`${config.label}: ${displayVal}`}>
                        <div
                          className={`factor-mini-bar-fill fill-${severity}`}
                          style={{ width: `${percent}%` }}
                        />
                      </div>
                    )}
                  </div>
                </div>
                <div className={`factor-badge badge-${severity}`}>
                  {displayVal}
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <p className="muted">The prediction response did not include risk factor details.</p>
      )}
    </section>
  );
}
