import { useState } from 'react';
import { Link } from 'react-router-dom';
import ErrorMessage from '../components/ErrorMessage.jsx';
import GoogleCorridorMap from '../components/GoogleCorridorMap.jsx';
import PredictionCard from '../components/PredictionCard.jsx';
import RecommendationCard from '../components/RecommendationCard.jsx';
import RiskFactors from '../components/RiskFactors.jsx';
import { getApiErrorMessage, predictRisk } from '../services/api.js';

const ASSET_TYPES = [
  { value: 'Road', label: '🛣️ Road Corridor', defaultMaterial: 'Asphalt', defaultAge: 12 },
  { value: 'Bridge', label: '🌉 Civil Bridge / Flyover', defaultMaterial: 'Concrete', defaultAge: 25 },
  { value: 'Pipeline', label: '🚰 Water / Utility Pipeline', defaultMaterial: 'Steel', defaultAge: 18 },
  { value: 'Drainage', label: '🌊 Drainage / Culvert', defaultMaterial: 'Concrete', defaultAge: 20 },
  { value: 'Streetlight', label: '💡 Streetlight Array', defaultMaterial: 'Steel', defaultAge: 8 },
  { value: 'Electrical Pole', label: '⚡ Electrical Utility Pole', defaultMaterial: 'Concrete', defaultAge: 15 },
];

const MATERIALS = ['Asphalt', 'Concrete', 'Steel', 'PVC', 'Copper', 'Composite'];

const CONDITION_OPTIONS = [
  {
    value: 'Good',
    title: 'Good',
    desc: 'No major visible deterioration; sound structural integrity.',
    badge: '🟢 Minor / None',
  },
  {
    value: 'Fair',
    title: 'Fair',
    desc: 'Moderate wear, minor surface cracks, weathering or light corrosion.',
    badge: '🟡 Routine Watch',
  },
  {
    value: 'Poor',
    title: 'Poor',
    desc: 'Substantial cracking, deep potholes, exposed rebar or heavy corrosion.',
    badge: '🔴 Urgent Defect',
  },
  {
    value: 'Unknown',
    title: 'Unknown',
    desc: 'Visual condition has not been formally audited; uses regional baseline.',
    badge: '⚪ Unaudited',
  },
];

const TRAFFIC_OPTIONS = [
  { value: 'Low', title: 'Low Traffic', desc: 'Rural / residential quiet roads' },
  { value: 'Moderate', title: 'Moderate Traffic', desc: 'Urban arterial / suburban avenues' },
  { value: 'Heavy', title: 'Heavy Traffic', desc: 'Multi-lane expressways, freight corridors' },
  { value: 'Unknown', title: 'Unknown', desc: 'Volume unmeasured' },
];

const RECENCY_OPTIONS = [
  { value: '< 1 year', title: 'Within Last Year', desc: 'Recent preventive maintenance' },
  { value: '1-3 years', title: '1–3 Years Ago', desc: 'Standard service cycle' },
  { value: '> 3 years', title: 'Over 3 Years Ago', desc: 'Deferred intervention' },
  { value: 'Unknown', title: 'History Unknown', desc: 'No verifiable logs' },
];

const INITIAL_LOCATION = {
  address: 'Mumbai - Pune Expressway, Lonavala-Khandala, Maharashtra 410401, India',
  latitude: 18.756,
  longitude: 73.4116,
  city: 'Pune',
  state: 'Maharashtra',
  postal_code: '410401',
};

export default function PredictRisk() {
  const [selectedLocation, setSelectedLocation] = useState(INITIAL_LOCATION);
  const [assetType, setAssetType] = useState('Road');
  const [material, setMaterial] = useState('Asphalt');
  const [ageYears, setAgeYears] = useState(12);
  const [ageUnknown, setAgeUnknown] = useState(false);
  const [condition, setCondition] = useState('Fair');
  const [trafficLevel, setTrafficLevel] = useState('Heavy');
  const [maintenanceRecency, setMaintenanceRecency] = useState('1-3 years');
  const [observationNotes, setObservationNotes] = useState('');

  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [requestError, setRequestError] = useState('');

  // Auto-update material when asset type changes if user hasn't explicitly customized
  const handleAssetTypeChange = (newType) => {
    setAssetType(newType);
    const assetMeta = ASSET_TYPES.find((a) => a.value === newType);
    if (assetMeta) {
      setMaterial(assetMeta.defaultMaterial);
      if (!ageUnknown) {
        setAgeYears(assetMeta.defaultAge);
      }
    }
  };

  const handleLocationSelect = (loc) => {
    setSelectedLocation(loc);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setRequestError('');
    setResult(null);
    setSubmitting(true);

    const payload = {
      asset_type: assetType,
      material,
      age_years: ageUnknown ? null : Number(ageYears) || 12,
      condition,
      traffic_level: trafficLevel,
      maintenance_recency: maintenanceRecency,
      observation_notes: observationNotes,
      location: {
        address: selectedLocation?.address || 'Pune, Maharashtra, India',
        latitude: selectedLocation?.latitude || 18.756,
        longitude: selectedLocation?.longitude || 73.4116,
        city: selectedLocation?.city || 'Pune',
        state: selectedLocation?.state || 'Maharashtra',
        postal_code: selectedLocation?.postal_code || '',
        place_id: selectedLocation?.place_id || null,
      },
    };

    try {
      const response = await predictRisk(payload);
      setResult(response);
    } catch (err) {
      setRequestError(getApiErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  const handleReset = () => {
    setSelectedLocation(INITIAL_LOCATION);
    setAssetType('Road');
    setMaterial('Asphalt');
    setAgeYears(12);
    setAgeUnknown(false);
    setCondition('Fair');
    setTrafficLevel('Heavy');
    setMaintenanceRecency('1-3 years');
    setObservationNotes('');
    setResult(null);
    setRequestError('');
  };

  return (
    <div className="page-stack">
      {/* Page Title & Intro */}
      <div className="page-intro-row">
        <div>
          <span className="eyebrow">LOCATION-AWARE PREDICTIVE MAINTENANCE</span>
          <h2>Assess Corridor Infrastructure Risk</h2>
          <p>
            Pinpoint any Indian road, bridge, or corridor on Google Maps and enter observable field indicators.
            Our trained Random Forest model predicts structural failure probability and Remaining Useful Life (RUL).
          </p>
        </div>
        <div className="header-badges-row">
          <span className="schema-pill">📍 Real Indian GIS Corridors</span>
          <span className="schema-pill">🧠 Supervised Machine Learning</span>
        </div>
      </div>

      {/* Two-Column Responsive Layout: Map Left, Realistic Form Right */}
      <div className="predict-two-column-layout">
        {/* Left Column: Google Maps & Indian Corridor Navigator */}
        <div className="predict-col-map">
          <GoogleCorridorMap
            selectedLocation={selectedLocation}
            onLocationSelect={handleLocationSelect}
          />
        </div>

        {/* Right Column: Realistic 5-6 Input Assessment Form */}
        <div className="predict-col-form">
          <form className="panel realistic-assessment-form" onSubmit={handleSubmit} noValidate>
            {/* Step 01 Card: Asset Specifications */}
            <div className="form-step-card">
              <div className="form-section-title">
                <span className="step-number">01</span>
                <div>
                  <h3>Asset Specifications</h3>
                  <p>Select the infrastructure type and structural material.</p>
                </div>
              </div>

              {/* Field A: Infrastructure Asset Type */}
              <div className="field-group-spaced">
                <label className="field-label">
                  <span>Infrastructure Asset Type <b>*</b></span>
                </label>
                <div className="asset-type-chips-grid">
                  {ASSET_TYPES.map((a) => (
                    <button
                      key={a.value}
                      type="button"
                      className={`asset-type-chip ${assetType === a.value ? 'selected' : ''}`}
                      onClick={() => handleAssetTypeChange(a.value)}
                    >
                      <span>{a.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              <div className="form-grid-two">
                {/* Material Dropdown */}
                <label className="field">
                  <span>Primary Structural Material <b>*</b></span>
                  <select value={material} onChange={(e) => setMaterial(e.target.value)}>
                    {MATERIALS.map((m) => (
                      <option key={m} value={m}>{m}</option>
                    ))}
                  </select>
                </label>

                {/* Field B: Approximate Asset Age */}
                <label className="field">
                  <span>Approximate Asset Age (Years) <b>*</b></span>
                  <div className="age-input-row">
                    <input
                      type="number"
                      min="0"
                      max="100"
                      step="1"
                      value={ageUnknown ? '' : ageYears}
                      onChange={(e) => setAgeYears(e.target.value)}
                      disabled={ageUnknown}
                      placeholder={ageUnknown ? 'Unknown age' : 'e.g. 15'}
                      required={!ageUnknown}
                    />
                    <label className="checkbox-sublabel">
                      <input
                        type="checkbox"
                        checked={ageUnknown}
                        onChange={(e) => setAgeUnknown(e.target.checked)}
                      />
                      <span>Unknown</span>
                    </label>
                  </div>
                </label>
              </div>
            </div>

            {/* Step 02 Card: Observable Field Condition */}
            <div className="form-step-card">
              <div className="form-section-title">
                <span className="step-number">02</span>
                <div>
                  <h3>Observable Field Condition</h3>
                  <p>Enter visible indicators verifiable without specialized lab instrumentation.</p>
                </div>
              </div>

              {/* Field C: Current Visible Condition */}
              <div className="field-group-spaced">
                <label className="field-label">
                  <span>Current Visible Physical Condition <b>*</b></span>
                </label>
                <div className="condition-cards-grid">
                  {CONDITION_OPTIONS.map((c) => (
                    <div
                      key={c.value}
                      className={`condition-choice-card ${condition === c.value ? 'selected' : ''}`}
                      onClick={() => setCondition(c.value)}
                    >
                      <div className="cond-card-header">
                        <strong>{c.title}</strong>
                        <span className="cond-badge">{c.badge}</span>
                      </div>
                      <p>{c.desc}</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Field D: Traffic or Usage Level */}
              <div className="field-group-spaced">
                <label className="field-label">
                  <span>Traffic Volume / Usage Intensity <b>*</b></span>
                </label>
                <div className="traffic-chips-grid">
                  {TRAFFIC_OPTIONS.map((t) => (
                    <button
                      key={t.value}
                      type="button"
                      className={`traffic-chip ${trafficLevel === t.value ? 'selected' : ''}`}
                      onClick={() => setTrafficLevel(t.value)}
                    >
                      <strong>{t.title}</strong>
                      <small>{t.desc}</small>
                    </button>
                  ))}
                </div>
              </div>

              {/* Field E: Maintenance Recency */}
              <div className="field-group-spaced">
                <label className="field-label">
                  <span>Maintenance Recency <b>*</b></span>
                </label>
                <div className="recency-chips-grid">
                  {RECENCY_OPTIONS.map((r) => (
                    <button
                      key={r.value}
                      type="button"
                      className={`recency-chip ${maintenanceRecency === r.value ? 'selected' : ''}`}
                      onClick={() => setMaintenanceRecency(r.value)}
                    >
                      <strong>{r.title}</strong>
                      <small>{r.desc}</small>
                    </button>
                  ))}
                </div>
              </div>

              {/* Field F: Optional Supporting Information */}
              <div className="field-group-spaced">
                <label className="field-label">
                  <span>Field Observation Notes (Optional)</span>
                </label>
                <textarea
                  className="notes-textarea"
                  rows="2"
                  value={observationNotes}
                  onChange={(e) => setObservationNotes(e.target.value)}
                  placeholder="e.g. Minor hairline cracks on northbound lane; water pooling near culvert joint after monsoon showers..."
                />
                <div className="cv-hint-tip">
                  <span>📸 Have pavement distress photos?</span>{' '}
                  <Link to="/dashboard" className="cv-hint-link">
                    Launch Module 04: OpenCV Road Damage Inspector →
                  </Link>
                </div>
              </div>
            </div>

            {/* Error Message */}
            {requestError && <div className="inline-error" role="alert">{requestError}</div>}

            {/* Form Actions */}
            <div className="form-actions">
              <button className="secondary-button" type="button" onClick={handleReset}>
                Reset Form
              </button>
              <button className="primary-button" type="submit" disabled={submitting}>
                {submitting ? (
                  <>
                    <span className="button-spinner" /> Running ML Assessment...
                  </>
                ) : (
                  <>
                    Assess Infrastructure Risk <span>→</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Model Assessment Results Section */}
      {result && (
        <div className="assessment-results-anchor">
          <PredictionCard result={result} />
          <div className="result-guidance-grid">
            <RecommendationCard
              recommendation={result.recommendation}
              priority={result.priority}
            />
            <RiskFactors factors={result.key_factors} />
          </div>
        </div>
      )}
    </div>
  );
}
