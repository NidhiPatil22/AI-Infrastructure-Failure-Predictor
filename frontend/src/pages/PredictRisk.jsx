import { useState } from 'react';
import ErrorMessage from '../components/ErrorMessage.jsx';
import PredictionCard from '../components/PredictionCard.jsx';
import RecommendationCard from '../components/RecommendationCard.jsx';
import RiskFactors from '../components/RiskFactors.jsx';
import { getApiErrorMessage, predictRisk } from '../services/api.js';

const categorical = {
  asset_type: ['Road', 'Bridge', 'Pipeline', 'Drainage', 'Streetlight', 'Electrical Pole'],
  zone: ['North', 'South', 'East', 'West', 'Central', 'Industrial'],
  material: ['Concrete', 'Steel', 'PVC', 'Asphalt', 'Copper', 'Composite'],
};

const fields = [
  ['age_years', 'Asset age', 0, 100, 1, 'years'],
  ['traffic_density', 'Traffic density', 0, 100, 1, '%'],
  ['average_load', 'Average load', 0, 200, 1, 'units'],
  ['annual_rainfall', 'Annual rainfall', 0, 5000, 1, 'mm'],
  ['average_temperature', 'Average temperature', -50, 60, 1, '°C'],
  ['maintenance_count', 'Maintenance count', 0, 50, 1, 'times'],
  ['days_since_maintenance', 'Days since maintenance', 0, 5000, 1, 'days'],
  ['days_since_inspection', 'Days since inspection', 0, 5000, 1, 'days'],
  ['structural_score', 'Structural score', 0, 100, 1, '/ 100'],
  ['corrosion_level', 'Corrosion level', 0, 100, 1, '%'],
  ['previous_failures', 'Previous failures', 0, 50, 1, 'events'],
  ['usage_intensity', 'Usage intensity', 0, 100, 1, '%'],
];

const initialForm = {
  asset_type: 'Bridge', zone: 'Central', material: 'Concrete', age_years: 27, traffic_density: 78,
  average_load: 120, annual_rainfall: 1650, average_temperature: 28.5, maintenance_count: 6,
  days_since_maintenance: 210, days_since_inspection: 320, structural_score: 58,
  corrosion_level: 72, previous_failures: 2, usage_intensity: 83,
};

export default function PredictRisk() {
  const [form, setForm] = useState(initialForm);
  const [errors, setErrors] = useState({});
  const [result, setResult] = useState(null);
  const [requestError, setRequestError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const update = (event) => {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: categorical[name] ? value : value }));
    setErrors((current) => ({ ...current, [name]: '' }));
  };

  const validate = () => {
    const next = {};
    for (const [name, label, min, max] of fields) {
      const number = Number(form[name]);
      if (form[name] === '' || !Number.isFinite(number)) next[name] = `${label} is required and must be numeric.`;
      else if (number < min || number > max) next[name] = `Enter a value from ${min} to ${max}.`;
    }
    for (const [name, label] of [['asset_type', 'Asset type'], ['zone', 'Zone'], ['material', 'Material']]) {
      if (!form[name]) next[name] = `${label} is required.`;
    }
    return next;
  };

  const submit = async (event) => {
    event.preventDefault();
    const nextErrors = validate();
    setErrors(nextErrors);
    setRequestError('');
    setResult(null);
    if (Object.keys(nextErrors).length) return;

    const payload = Object.fromEntries(Object.entries(form).map(([key, value]) => [
      key,
      categorical[key] ? value : Number(value),
    ]));
    payload.previous_failures = Math.trunc(payload.previous_failures);
    setSubmitting(true);
    try {
      setResult(await predictRisk(payload));
    } catch (error) {
      setRequestError(getApiErrorMessage(error));
    } finally {
      setSubmitting(false);
    }
  };

  const reset = () => {
    setForm(initialForm);
    setErrors({});
    setResult(null);
    setRequestError('');
  };

  return (
    <div className="page-stack">
      <div className="page-intro-row"><div><span className="eyebrow">PREDICTIVE MAINTENANCE</span><h2>Assess an infrastructure asset</h2><p>Enter the asset conditions below. Fields match the backend’s <code>AssetInput</code> request schema.</p></div><span className="schema-pill">15 required fields</span></div>
      <div className="predict-layout">
        <form className="panel prediction-form" onSubmit={submit} noValidate>
          <div className="form-section-title"><span className="step-number">01</span><div><h3>Asset information</h3><p>Identity and location of the infrastructure.</p></div></div>
          <div className="form-grid">
            {Object.entries(categorical).map(([name, options]) => (
              <label className="field" key={name}>
                <span>{name === 'asset_type' ? 'Asset type' : name === 'zone' ? 'Zone' : 'Material'} <b>*</b></span>
                <select name={name} value={form[name]} onChange={update}>
                  <option value="">Select {name.replace('_', ' ')}</option>
                  {options.map((option) => <option key={option}>{option}</option>)}
                </select>
                {errors[name] && <small className="field-error">{errors[name]}</small>}
              </label>
            ))}
          </div>
          <div className="form-section-title form-section-spaced"><span className="step-number">02</span><div><h3>Condition & environment</h3><p>Use the latest inspection or maintenance records where possible.</p></div></div>
          <div className="form-grid">
            {fields.map(([name, label, min, max, step, suffix]) => (
              <label className="field" key={name}>
                <span>{label} <b>*</b></span>
                <div className="input-with-suffix">
                  <input name={name} type="number" min={min} max={max} step={step} value={form[name]} onChange={update} required />
                  <span>{suffix}</span>
                </div>
                {errors[name] && <small className="field-error">{errors[name]}</small>}
              </label>
            ))}
          </div>
          {requestError && <div className="inline-error" role="alert">{requestError}</div>}
          <div className="form-actions">
            <button className="secondary-button" type="button" onClick={reset}>Reset form</button>
            <button className="primary-button" type="submit" disabled={submitting}>{submitting ? <><span className="button-spinner" /> Analyzing Infrastructure...</> : <>Predict Failure Risk <span>→</span></>}</button>
          </div>
        </form>
        <aside className="predict-aside">
          <div className="aside-tip"><span className="tip-icon">✧</span><span className="eyebrow">MODEL NOTE</span><h3>Use measured values</h3><p>This form submits directly to the existing FastAPI model. Results are generated by the trained backend bundle.</p></div>
          {result && <RiskFactors factors={result.key_factors} />}
          {!result && <div className="aside-checklist"><span className="eyebrow">ASSESSMENT FLOW</span><div><i>1</i><span>Describe the asset</span></div><div><i>2</i><span>Enter condition data</span></div><div><i>3</i><span>Review model output</span></div></div>}
        </aside>
      </div>
      {result && <>
        <PredictionCard result={result} />
        <RecommendationCard recommendation={result.recommendation} priority={result.priority} />
      </>}
    </div>
  );
}
