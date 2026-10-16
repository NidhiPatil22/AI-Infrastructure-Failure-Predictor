import { useCallback, useEffect, useState } from 'react';
import ErrorMessage from '../components/ErrorMessage.jsx';
import Loading from '../components/Loading.jsx';
import {
  exportAuditCsvUrl,
  exportAuditJsonUrl,
  getApiErrorMessage,
  getAuditFindings,
  getAuditSummary,
} from '../services/api.js';

export default function DatasetAudit() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [auditData, setAuditData] = useState(null);
  const [findings, setFindings] = useState([]);
  const [filterType, setFilterType] = useState('ALL');

  const loadData = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const [summaryRes, findingsRes] = await Promise.all([
        getAuditSummary(),
        getAuditFindings({ limit: 100 }),
      ]);
      setAuditData(summaryRes);
      setFindings(findingsRes.findings || []);
    } catch (err) {
      setError(getApiErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  if (loading) return <Loading label="Executing dynamic dataset audit..." />;
  if (error) return <ErrorMessage message={error} onRetry={loadData} />;
  if (!auditData) return null;

  const { summary, provenance, target_analysis, missing_breakdown, domain_validation, leakage_warnings } = auditData;

  const filteredFindings = findings.filter((f) => {
    if (filterType === 'ALL') return true;
    return f.issue_type === filterType;
  });

  return (
    <div className="page-stack">
      {/* Top Banner Row */}
      <div className="page-intro-row">
        <div>
          <span className="eyebrow">QUALITY AUDIT & PROVENANCE INSPECTION</span>
          <h2>Dataset Quality & Schema Audit</h2>
          <p>
            Dynamically evaluated from active telemetry dataset (
            <code>backend/data/urban_infrastructure_data.csv</code>).
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <a
            href={exportAuditCsvUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="action-button"
            style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
          >
            📥 Export Findings (CSV)
          </a>
          <a
            href={exportAuditJsonUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="action-button secondary"
            style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
          >
            📄 Audit Report (JSON)
          </a>
          <button
            type="button"
            className="action-button"
            style={{ backgroundColor: '#2563eb' }}
            onClick={loadData}
          >
            🔄 Re-Audit Dataset
          </button>
        </div>
      </div>

      {/* KPI Overview Grid */}
      <div className="content-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))' }}>
        <div className="panel stat-panel">
          <span className="eyebrow">MONITORED ASSETS</span>
          <div className="stat-number">{summary.total_records?.toLocaleString()}</div>
          <small>Dynamic row count</small>
        </div>
        <div className="panel stat-panel">
          <span className="eyebrow">DATASET ATTRIBUTES</span>
          <div className="stat-number">{summary.total_features}</div>
          <small>15 features + 3 engineered targets</small>
        </div>
        <div className="panel stat-panel">
          <span className="eyebrow">DATA QUALITY SCORE</span>
          <div className="stat-number" style={{ color: summary.data_quality_score >= 90 ? '#10b981' : '#f59e0b' }}>
            {summary.data_quality_score}%
          </div>
          <small>{summary.data_quality_grade}</small>
        </div>
        <div className="panel stat-panel">
          <span className="eyebrow">MISSING CELLS</span>
          <div className="stat-number" style={{ color: summary.missing_percentage > 2 ? '#ef4444' : '#10b981' }}>
            {summary.missing_percentage}%
          </div>
          <small>{summary.total_missing_cells} cells across {summary.columns_with_missing_count} columns</small>
        </div>
        <div className="panel stat-panel">
          <span className="eyebrow">DUPLICATE RECORDS</span>
          <div className="stat-number" style={{ color: summary.duplicate_rows > 0 ? '#ef4444' : '#10b981' }}>
            {summary.duplicate_rows}
          </div>
          <small>0 duplicate asset keys</small>
        </div>
      </div>

      {/* Provenance & Limitations Banner */}
      <section className="panel" style={{ borderLeft: '4px solid #fecb00' }}>
        <div className="section-heading">
          <div>
            <span className="eyebrow">DATASET PROVENANCE & ACADEMIC LIMITATIONS</span>
            <h2>{provenance.dataset_origin}</h2>
          </div>
          <span className="schema-pill" style={{ background: 'rgba(254, 203, 0, 0.2)', color: '#b45309', borderColor: '#fecb00' }}>
            {provenance.verification_status}
          </span>
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '10px' }}>
          <div>
            <h4 style={{ margin: '0 0 6px 0', fontSize: '14px', color: '#1e3a5f' }}>Ingestion & Generation Pipeline</h4>
            <p style={{ margin: 0, fontSize: '13px', lineHeight: 1.6, color: 'var(--text-muted, #64748b)' }}>
              {provenance.telemetry_description}
            </p>
            <div style={{ marginTop: '8px', fontSize: '12px' }}>
              <strong>Generator Script:</strong> <code>{provenance.generator_script}</code>
            </div>
          </div>
          <div>
            <h4 style={{ margin: '0 0 6px 0', fontSize: '14px', color: '#b45309' }}>Experimental Boundaries & Integrity</h4>
            <p style={{ margin: 0, fontSize: '13px', lineHeight: 1.6, color: 'var(--text-muted, #64748b)' }}>
              {provenance.academic_limitation}
            </p>
            <div style={{ marginTop: '8px', fontSize: '12px' }}>
              <strong>Configured Geography:</strong> <span>{provenance.geography}</span>
            </div>
          </div>
        </div>
      </section>

      {/* Target Distribution & Imbalance Section */}
      {target_analysis && (
        <section className="panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">TARGET DISTRIBUTION & CLASS IMBALANCE</span>
              <h2>Classification Target: <code>{target_analysis.target_column}</code></h2>
              <p>Dynamic class breakdown and clinical assessment of majority/minority imbalance.</p>
            </div>
            <span className={`schema-pill ${target_analysis.is_imbalanced ? 'warning' : 'success'}`}>
              Imbalance Ratio: {target_analysis.imbalance_ratio} ({target_analysis.severity})
            </span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', alignItems: 'center' }}>
            <div>
              <div style={{ marginBottom: '14px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px', fontSize: '13px' }}>
                  <strong>Operational (0)</strong>
                  <span>{target_analysis.class_counts['Operational (0)']} ({target_analysis.class_percentages['Operational (0)']}%)</span>
                </div>
                <div style={{ background: '#e2e8f0', borderRadius: '4px', height: '14px', overflow: 'hidden' }}>
                  <div
                    style={{
                      width: `${target_analysis.class_percentages['Operational (0)']}%`,
                      background: '#10b981',
                      height: '100%',
                    }}
                  />
                </div>
              </div>

              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px', fontSize: '13px' }}>
                  <strong style={{ color: '#ef4444' }}>Failure Incident (1) - Minority Class</strong>
                  <span style={{ color: '#ef4444' }}>
                    {target_analysis.class_counts['Failure Incident (1)']} ({target_analysis.class_percentages['Failure Incident (1)']}%)
                  </span>
                </div>
                <div style={{ background: '#e2e8f0', borderRadius: '4px', height: '14px', overflow: 'hidden' }}>
                  <div
                    style={{
                      width: `${target_analysis.class_percentages['Failure Incident (1)']}%`,
                      background: '#ef4444',
                      height: '100%',
                    }}
                  />
                </div>
              </div>
            </div>

            <div style={{ background: 'var(--panel-subtle, #f8fafc)', padding: '16px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
              <strong style={{ fontSize: '13px', color: '#0f172a' }}>Why Imbalance Affects Model Evaluation:</strong>
              <p style={{ margin: '6px 0 10px 0', fontSize: '12.5px', lineHeight: 1.5, color: '#475569' }}>
                {target_analysis.imbalance_rationale}
              </p>
              <strong style={{ fontSize: '12px', color: '#b45309' }}>Recommended Model Controls:</strong>
              <ul style={{ margin: '4px 0 0 16px', padding: 0, fontSize: '12px', color: '#475569' }}>
                {target_analysis.recommended_actions.map((act, i) => (
                  <li key={i}>{act}</li>
                ))}
              </ul>
            </div>
          </div>
        </section>
      )}

      {/* Domain-Specific Validation Rules */}
      <section className="panel">
        <div className="section-heading">
          <div>
            <span className="eyebrow">INFRASTRUCTURE DOMAIN CONSTRAINTS</span>
            <h2>Civil Engineering Domain Validation</h2>
            <p>17 domain physics and schema range checks executed across all records.</p>
          </div>
          <span className="schema-pill success">
            {domain_validation.filter((r) => r.status === 'PASSED').length} / {domain_validation.length} Rules Passed
          </span>
        </div>

        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th>Telemetry Field</th>
                <th>Engineering Specification</th>
                <th>Violations Found</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {domain_validation.map((rule, idx) => (
                <tr key={idx}>
                  <td><code>{rule.field}</code></td>
                  <td>{rule.description}</td>
                  <td>
                    <strong>{rule.violations_count}</strong>
                  </td>
                  <td>
                    <span
                      style={{
                        padding: '3px 8px',
                        borderRadius: '4px',
                        fontSize: '11px',
                        fontWeight: 700,
                        backgroundColor: rule.status === 'PASSED' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                        color: rule.status === 'PASSED' ? '#10b981' : '#ef4444',
                        border: `1px solid ${rule.status === 'PASSED' ? '#10b981' : '#ef4444'}`,
                      }}
                    >
                      {rule.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Missing Values Breakdown & Leakage Warnings */}
      <div className="content-grid" style={{ gridTemplateColumns: '1.2fr 1fr' }}>
        <section className="panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">MISSING ATTRIBUTES</span>
              <h2>Missing Values Analysis</h2>
            </div>
          </div>
          {missing_breakdown.length === 0 ? (
            <div className="chart-empty">No missing values detected across dataset features.</div>
          ) : (
            <div className="table-scroll">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Column</th>
                    <th>Data Type</th>
                    <th>Missing Count</th>
                    <th>Missing %</th>
                  </tr>
                </thead>
                <tbody>
                  {missing_breakdown.map((col, idx) => (
                    <tr key={idx}>
                      <td><code>{col.column}</code></td>
                      <td><span>{col.dtype}</span></td>
                      <td><strong>{col.missing_count}</strong></td>
                      <td>{col.missing_percentage}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        <section className="panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">LEAKAGE PREVENTION</span>
              <h2>Data Leakage & Integrity Audit</h2>
            </div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {leakage_warnings.map((warn, i) => (
              <div
                key={i}
                style={{
                  padding: '12px',
                  borderRadius: '6px',
                  background: warn.severity === 'WARNING' ? 'rgba(239, 68, 68, 0.08)' : 'rgba(37, 99, 235, 0.08)',
                  borderLeft: `4px solid ${warn.severity === 'WARNING' ? '#ef4444' : '#2563eb'}`,
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                  <strong style={{ fontSize: '13px', color: warn.severity === 'WARNING' ? '#ef4444' : '#1e3a5f' }}>
                    {warn.type}
                  </strong>
                  <span style={{ fontSize: '11px', fontWeight: 600, color: '#64748b' }}><code>{warn.field}</code></span>
                </div>
                <p style={{ margin: 0, fontSize: '12.5px', color: '#475569', lineHeight: 1.5 }}>
                  {warn.detail}
                </p>
              </div>
            ))}
          </div>
        </section>
      </div>

      {/* Record-Level Findings Inspection */}
      <section className="panel">
        <div className="section-heading">
          <div>
            <span className="eyebrow">RECORD-LEVEL LOGS</span>
            <h2>Validation Findings Sample</h2>
            <p>Detailed view of records requiring imputation or domain verification.</p>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            {['ALL', 'Missing Value', 'Domain Range Violation'].map((t) => (
              <button
                key={t}
                type="button"
                className={`schema-pill ${filterType === t ? 'active' : ''}`}
                style={{ cursor: 'pointer', background: filterType === t ? '#1e3a5f' : 'transparent', color: filterType === t ? '#fff' : 'inherit' }}
                onClick={() => setFilterType(t)}
              >
                {t}
              </button>
            ))}
          </div>
        </div>

        {filteredFindings.length === 0 ? (
          <div className="chart-empty">No record findings match the current filter.</div>
        ) : (
          <div className="table-scroll" style={{ maxHeight: '360px', overflowY: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Row</th>
                  <th>Asset ID</th>
                  <th>Field</th>
                  <th>Observed Value</th>
                  <th>Issue Type</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {filteredFindings.slice(0, 50).map((item, idx) => (
                  <tr key={idx}>
                    <td>{item.row_index}</td>
                    <td><strong>{item.asset_id}</strong></td>
                    <td><code>{item.field}</code></td>
                    <td><span style={{ color: '#b45309' }}>{item.value}</span></td>
                    <td>
                      <span
                        style={{
                          fontSize: '11px',
                          fontWeight: 600,
                          padding: '2px 6px',
                          borderRadius: '4px',
                          backgroundColor: item.issue_type === 'Missing Value' ? 'rgba(245, 158, 11, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                          color: item.issue_type === 'Missing Value' ? '#d97706' : '#ef4444',
                        }}
                      >
                        {item.issue_type}
                      </span>
                    </td>
                    <td>{item.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </div>
  );
}
