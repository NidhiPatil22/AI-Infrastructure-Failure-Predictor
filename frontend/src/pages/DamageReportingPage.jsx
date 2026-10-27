import { useCallback, useEffect, useRef, useState } from 'react';
import { getDamageReports, submitDamageReport, getApiErrorMessage } from '../services/api.js';

// Pune Municipal Center & Bounding Constraints
const PUNE_BOUNDS = {
  min_lat: 18.4200,
  max_lat: 18.6400,
  min_lng: 73.7400,
  max_lng: 73.9800,
};

const PUNE_WARDS_LIST = [
  'Shivajinagar-Ghole Road Ward',
  'Kothrud-Bavdhan Ward',
  'Aundh-Baner Ward',
  'Hadapsar-Mundhwa Ward',
  'Dhankawadi-Sahakarnagar Ward',
  'Kasba-Vishrambaug Wada Ward',
  'Bhosari MIDC Ward',
  'Nagar Road-Vadgaonsheri Ward',
  'Bibwewadi Ward',
  'Pimpri Industrial Ward',
];

const DAMAGE_TYPES = [
  'Pothole',
  'Alligator Cracking',
  'Longitudinal Crack',
  'Transverse Crack',
  'Damaged Bridge Surface / Expansion Joint',
  'Corrosion & Steel Spalling',
  'Drainage Blockage / Culvert Collapse',
  'Damaged Electrical Pole / Streetlight',
  'Water Pipeline Leak / Rupture',
  'Other Visible Civil Defect',
];

const INFRASTRUCTURE_TYPES = [
  'Road',
  'Bridge',
  'Pipeline',
  'Drainage',
  'Streetlight',
  'Electrical Pole',
];

export default function DamageReportingPage() {
  const fileInputRef = useRef(null);

  // Form State
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [damageType, setDamageType] = useState(DAMAGE_TYPES[0]);
  const [infraType, setInfraType] = useState('Road');
  const [puneWard, setPuneWard] = useState(PUNE_WARDS_LIST[0]);
  const [locality, setLocality] = useState('Shivajinagar');
  const [address, setAddress] = useState('');
  const [latitude, setLatitude] = useState(18.5204);
  const [longitude, setLongitude] = useState(73.8567);
  const [description, setDescription] = useState('');

  // UI State
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState('');
  const [submissionSuccess, setSubmissionSuccess] = useState(null);
  const [recentReports, setRecentReports] = useState([]);
  const [loadingReports, setLoadingReports] = useState(false);
  const [locMethod, setLocMethod] = useState('manual'); // 'manual' or 'map'

  // Load existing damage reports
  const loadReports = useCallback(async () => {
    setLoadingReports(true);
    try {
      const res = await getDamageReports({ limit: 20 });
      setRecentReports(Array.isArray(res?.reports) ? res.reports : []);
    } catch (err) {
      console.error('Failed to load damage reports:', err);
    } finally {
      setLoadingReports(false);
    }
  }, []);

  useEffect(() => {
    loadReports();
  }, [loadReports]);

  // Handle File Selection
  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate type
    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      setFormError('Unsupported file type. Please upload a JPG, PNG, or WEBP image.');
      return;
    }

    // Validate size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setFormError('File size exceeds 10 MB limit.');
      return;
    }

    setFormError('');
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  // Validate coordinates inside Pune
  const isCoordInsidePune = (lat, lng) => {
    return (
      lat >= PUNE_BOUNDS.min_lat &&
      lat <= PUNE_BOUNDS.max_lat &&
      lng >= PUNE_BOUNDS.min_lng &&
      lng <= PUNE_BOUNDS.max_lng
    );
  };

  // Preset quick coordinates by locality
  const handleLocalityPreset = (locName) => {
    setLocality(locName);
    const presets = {
      Shivajinagar: { lat: 18.5314, lng: 73.8446, ward: 'Shivajinagar-Ghole Road Ward' },
      Kothrud: { lat: 18.5074, lng: 73.8077, ward: 'Kothrud-Bavdhan Ward' },
      Aundh: { lat: 18.5580, lng: 73.8075, ward: 'Aundh-Baner Ward' },
      Baner: { lat: 18.5590, lng: 73.7868, ward: 'Aundh-Baner Ward' },
      Hadapsar: { lat: 18.5089, lng: 73.9259, ward: 'Hadapsar-Mundhwa Ward' },
      'Viman Nagar': { lat: 18.5679, lng: 73.9143, ward: 'Nagar Road-Vadgaonsheri Ward' },
      Katraj: { lat: 18.4529, lng: 73.8553, ward: 'Dhankawadi-Sahakarnagar Ward' },
      'Bhosari MIDC': { lat: 18.6270, lng: 73.8540, ward: 'Bhosari MIDC Ward' },
    };
    if (presets[locName]) {
      setLatitude(presets[locName].lat);
      setLongitude(presets[locName].lng);
      setPuneWard(presets[locName].ward);
    }
  };

  // Handle Form Submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');
    setSubmissionSuccess(null);

    if (!selectedFile) {
      setFormError('Please select or capture an inspection photograph.');
      return;
    }

    const lat = Number(latitude);
    const lng = Number(longitude);

    if (isNaN(lat) || isNaN(lng)) {
      setFormError('Please enter valid numeric latitude and longitude coordinates.');
      return;
    }

    if (!isCoordInsidePune(lat, lng)) {
      setFormError(
        `Selected coordinates (${lat.toFixed(4)}, ${lng.toFixed(4)}) are outside the Pune city monitoring boundary (Lat: 18.42 - 18.64, Lng: 73.74 - 73.98). Please provide a Pune location.`
      );
      return;
    }

    setSubmitting(true);
    try {
      const formData = new FormData();
      formData.append('image', selectedFile);
      formData.append('latitude', lat.toString());
      formData.append('longitude', lng.toString());
      formData.append('damage_type', damageType);
      formData.append('infrastructure_type', infraType);
      formData.append('pune_ward', puneWard);
      formData.append('locality', locality);
      formData.append('address', address || `${locality}, ${puneWard}, Pune`);
      formData.append('description', description || `Reported ${damageType} in ${locality}`);

      const result = await submitDamageReport(formData);

      setSubmissionSuccess(result.report);
      setSelectedFile(null);
      setPreviewUrl(null);
      setDescription('');
      if (fileInputRef.current) fileInputRef.current.value = '';

      loadReports();
    } catch (err) {
      setFormError(getApiErrorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page-stack">
      {/* Page Header Banner */}
      <div className="damage-reporting-hero">
        <div>
          <span className="eyebrow">CITIZEN & CONTRACTOR FIELD INSPECTIONS</span>
          <h1>Report Infrastructure Damage & Upload Inspection</h1>
          <p>
            Upload civil damage imagery (potholes, structural cracks, bridge joint wear, corrosion, drainage blockages).
            Every report is automatically geo-fenced to the Pune metropolitan monitoring boundary, evaluated by Computer
            Vision for defect severity, and linked to the nearest monitored infrastructure asset.
          </p>
        </div>
      </div>

      <div className="content-grid two-column-grid">
        {/* Left Column: Damage Upload Form */}
        <section className="panel damage-form-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">FIELD TELEMETRY ENTRY</span>
              <h2>Damage Inspection Report</h2>
            </div>
            <span className="small-tag pune-badge">Pune City Only</span>
          </div>

          {formError && <div className="form-error-banner">⚠️ {formError}</div>}

          {submissionSuccess && (
            <div className="form-success-banner">
              <div className="success-header">
                <span className="success-icon">✓</span>
                <div>
                  <strong>Report Successfully Logged: {submissionSuccess.report_id}</strong>
                  <p>Status: <span className="text-accent">{submissionSuccess.status}</span></p>
                </div>
              </div>
              <div className="success-details">
                {submissionSuccess.distance_to_asset_m != null ? (
                  <p>
                    📍 Nearest Infrastructure:{' '}
                    <strong>{submissionSuccess.infrastructure_type || 'Road Segment'} ({submissionSuccess.locality || 'Pune'})</strong>{' '}
                    — Distance: <strong>{submissionSuccess.distance_to_asset_m} m</strong>. Flagged for priority inspection.
                  </p>
                ) : (
                  <p>Logged as independent field observation in Pune monitoring queue.</p>
                )}
                {submissionSuccess.cv_detected && (
                  <p className="success-cv">
                    AI CV Detection: <strong>{submissionSuccess.cv_detected}</strong>
                    {submissionSuccess.cv_confidence && (
                      <small> ({(submissionSuccess.cv_confidence * 100).toFixed(0)}% confidence)</small>
                    )}
                  </p>
                )}
              </div>
            </div>
          )}

          <form onSubmit={handleSubmit} className="damage-upload-form">
            {/* 1. Image Upload Dropzone */}
            <div className="form-group">
              <label className="field-label">
                <strong>Inspection Photograph *</strong>
                <small>JPG, PNG, or WEBP (Max 10 MB)</small>
              </label>

              <div
                className={`image-dropzone ${previewUrl ? 'has-preview' : ''}`}
                onClick={() => fileInputRef.current?.click()}
              >
                {previewUrl ? (
                  <div className="preview-container">
                    <img src={previewUrl} alt="Inspection Preview" className="uploaded-preview-img" />
                    <div className="preview-actions">
                      <button
                        type="button"
                        className="change-image-btn"
                        onClick={(e) => {
                          e.stopPropagation();
                          fileInputRef.current?.click();
                        }}
                      >
                        📷 Change Photo
                      </button>
                      <button
                        type="button"
                        className="remove-image-btn"
                        onClick={(e) => {
                          e.stopPropagation();
                          setSelectedFile(null);
                          setPreviewUrl(null);
                          if (fileInputRef.current) fileInputRef.current.value = '';
                        }}
                      >
                        ✕ Remove
                      </button>
                    </div>
                  </div>
                ) : (
                  <div className="dropzone-placeholder">
                    <span className="upload-icon">📷</span>
                    <strong>Click or Drag to Upload Damage Photo</strong>
                    <small>High resolution close-up of pavement, crack, or structure</small>
                  </div>
                )}
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  accept=".jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp"
                  style={{ display: 'none' }}
                />
              </div>
            </div>

            {/* 2. Defect Type & Infrastructure Type */}
            <div className="form-row-two">
              <div className="form-group">
                <label className="field-label" htmlFor="damage-type-select">
                  <strong>Observed Damage Type *</strong>
                </label>
                <select
                  id="damage-type-select"
                  className="form-input"
                  value={damageType}
                  onChange={(e) => setDamageType(e.target.value)}
                >
                  {DAMAGE_TYPES.map((t) => (
                    <option key={t} value={t}>
                      {t}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="field-label" htmlFor="infra-type-select">
                  <strong>Infrastructure Category</strong>
                </label>
                <select
                  id="infra-type-select"
                  className="form-input"
                  value={infraType}
                  onChange={(e) => setInfraType(e.target.value)}
                >
                  {INFRASTRUCTURE_TYPES.map((t) => (
                    <option key={t} value={t}>
                      {t}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* 3. Location Specification Method */}
            <div className="form-group">
              <div className="location-method-tabs">
                <button
                  type="button"
                  className={`loc-tab ${locMethod === 'manual' ? 'active' : ''}`}
                  onClick={() => setLocMethod('manual')}
                >
                  Method A: Select Locality & Ward
                </button>
                <button
                  type="button"
                  className={`loc-tab ${locMethod === 'map' ? 'active' : ''}`}
                  onClick={() => setLocMethod('map')}
                >
                  Method B: Coordinate Pin
                </button>
              </div>

              {locMethod === 'manual' ? (
                <div className="locality-picker-wrap">
                  <label className="sub-label">Select Pune Locality Preset:</label>
                  <div className="locality-pills">
                    {[
                      'Shivajinagar',
                      'Kothrud',
                      'Aundh',
                      'Baner',
                      'Hadapsar',
                      'Viman Nagar',
                      'Katraj',
                      'Bhosari MIDC',
                    ].map((loc) => (
                      <button
                        key={loc}
                        type="button"
                        className={`pill-btn ${locality === loc ? 'selected' : ''}`}
                        onClick={() => handleLocalityPreset(loc)}
                      >
                        {loc}
                      </button>
                    ))}
                  </div>

                  <div className="form-row-two" style={{ marginTop: '12px' }}>
                    <div>
                      <label className="field-label" htmlFor="pune-ward-select">Pune Ward</label>
                      <select
                        id="pune-ward-select"
                        className="form-input"
                        value={puneWard}
                        onChange={(e) => setPuneWard(e.target.value)}
                      >
                        {PUNE_WARDS_LIST.map((w) => (
                          <option key={w} value={w}>
                            {w}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="field-label" htmlFor="locality-input">Area / Locality Name</label>
                      <input
                        id="locality-input"
                        type="text"
                        className="form-input"
                        value={locality}
                        onChange={(e) => setLocality(e.target.value)}
                        placeholder="e.g., Kothrud, Deccan, Baner"
                      />
                    </div>
                  </div>
                </div>
              ) : null}

              {/* Coordinates Display with Validation Status */}
              <div className="coords-input-grid">
                <div>
                  <label className="field-label" htmlFor="lat-input">Latitude (Pune: 18.42 - 18.64) *</label>
                  <input
                    id="lat-input"
                    type="number"
                    step="0.0001"
                    className="form-input"
                    value={latitude}
                    onChange={(e) => setLatitude(parseFloat(e.target.value) || 0)}
                  />
                </div>
                <div>
                  <label className="field-label" htmlFor="lng-input">Longitude (Pune: 73.74 - 73.98) *</label>
                  <input
                    id="lng-input"
                    type="number"
                    step="0.0001"
                    className="form-input"
                    value={longitude}
                    onChange={(e) => setLongitude(parseFloat(e.target.value) || 0)}
                  />
                </div>
              </div>

              <div
                className={`geo-validation-note ${
                  isCoordInsidePune(latitude, longitude) ? 'valid' : 'invalid'
                }`}
              >
                {isCoordInsidePune(latitude, longitude)
                  ? '✓ Location is within active Pune city monitoring area'
                  : '✕ Coordinates outside Pune boundary! Reports outside Pune are rejected.'}
              </div>
            </div>

            {/* 4. Optional Address / Landmark */}
            <div className="form-group">
              <label className="field-label" htmlFor="landmark-input">Landmark / Street Address</label>
              <input
                id="landmark-input"
                type="text"
                className="form-input"
                placeholder="e.g., Near Paud Road Flyover Pier 4, opposite metro station"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
              />
            </div>

            {/* 5. Defect Description */}
            <div className="form-group">
              <label className="field-label" htmlFor="desc-textarea">Description & Visual Severity Notes</label>
              <textarea
                id="desc-textarea"
                rows={3}
                className="form-input"
                placeholder="Describe crack length, pothole depth, water pooling, structural deformation..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>

            <button
              type="submit"
              className="primary-button submit-btn full-width"
              disabled={submitting}
            >
              {submitting ? 'Running CV Detection & Logging...' : 'Submit Damage Inspection Report'}
            </button>
          </form>
        </section>

        {/* Right Column: Recent Field Inspections Feed */}
        <section className="panel recent-reports-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">FIELD INSPECTION LOGS</span>
              <h2>Recent Damage Reports</h2>
              <p>Real-time citizen & contractor inspection log across Pune wards.</p>
            </div>
            <button
              type="button"
              className="secondary-button refresh-btn"
              onClick={loadReports}
              disabled={loadingReports}
            >
              ↻ Refresh
            </button>
          </div>

          {recentReports.length === 0 ? (
            <div className="empty-state">
              <span>📋</span>
              <p>No damage reports logged yet. Submit the first inspection above.</p>
            </div>
          ) : (
            <div className="reports-scroll-feed">
              {recentReports.map((report) => (
                <div key={report.report_id} className="feed-report-card">
                  <div className="feed-card-header">
                    <strong>{report.report_id}</strong>
                    <span
                      className={`status-pill ${String(report.status)
                        .toLowerCase()
                        .replace(/\s+/g, '-')}`}
                    >
                      {report.status}
                    </span>
                  </div>

                  <div className="feed-card-type">
                    <span className="defect-badge">⚠️ {report.damage_type}</span>
                    <span className="infra-badge">{report.infrastructure_type || 'Road'}</span>
                  </div>

                  <div className="feed-card-location">
                    <span>📍 {report.locality || 'Pune'}, {report.pune_ward || 'PMC'}</span>
                    <small className="mono-code">
                      ({Number(report.latitude).toFixed(4)}, {Number(report.longitude).toFixed(4)})
                    </small>
                  </div>

                  {report.distance_to_asset_m != null && (
                    <div className="feed-card-linked-asset">
                      📍 Nearest Infrastructure: <strong>{report.infrastructure_type || 'Road Segment'}</strong>
                      {report.locality ? ` · ${report.locality}` : ''}
                      <span> (Distance: {Number(report.distance_to_asset_m).toFixed(1)} m)</span>
                    </div>
                  )}

                  {report.cv_detected && (
                    <div className="feed-card-cv">
                      <span className="cv-tag">AI CV:</span> {report.cv_detected}
                      {report.cv_confidence && (
                        <small> ({(report.cv_confidence * 100).toFixed(0)}% conf)</small>
                      )}
                    </div>
                  )}

                  {report.image_url && (
                    <div className="feed-card-img-wrap">
                      <img
                        src={report.image_url}
                        alt={`Photo for ${report.report_id}`}
                        className="feed-card-img"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none';
                        }}
                      />
                    </div>
                  )}

                  {report.description && <p className="feed-card-desc">{report.description}</p>}

                  <div className="feed-card-footer">
                    <small>Logged: {report.created_at || 'Recently'}</small>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
