import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import ErrorMessage from '../components/ErrorMessage.jsx';
import Loading from '../components/Loading.jsx';
import {
  getApiErrorMessage,
  getPipelineTestResults,
  runPipelineTests,
} from '../services/api.js';

export default function PipelineVerification() {
  const [loading, setLoading] = useState(true);
  const [running, setRunning] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('ALL');

  const loadResults = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const data = await getPipelineTestResults();
      setResults(data);
    } catch (err) {
      setError(getApiErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, []);

  const handleRunTests = async () => {
    setRunning(true);
    setError('');
    try {
      const data = await runPipelineTests();
      setResults(data);
    } catch (err) {
      setError(getApiErrorMessage(err));
    } finally {
      setRunning(false);
    }
  };

  useEffect(() => {
    loadResults();
  }, [loadResults]);

  if (loading) return <Loading label="Loading pipeline verification state..." />;
  if (error) return <ErrorMessage message={error} onRetry={loadResults} />;
  if (!results) return null;

  const { summary_counts, checks, execution_time_seconds, timestamp, overall_status } = results;

  const categories = ['ALL', ...new Set(checks.map((c) => c.category))];

  const filteredChecks = checks.filter((c) => {
    if (selectedCategory === 'ALL') return true;
    return c.category === selectedCategory;
  });

  const getStatusBadge = (status) => {
    switch (status) {
      case 'PASSED':
        return { bg: 'rgba(16, 185, 129, 0.15)', text: '#10b981', border: '#10b981', label: '✔ PASSED' };
      case 'WARNING':
        return { bg: 'rgba(245, 158, 11, 0.15)', text: '#d97706', border: '#f59e0b', label: '⚠️ WARNING' };
      case 'FAILED':
        return { bg: 'rgba(239, 68, 68, 0.15)', text: '#ef4444', border: '#ef4444', label: '✖ FAILED' };
      default:
        return { bg: 'rgba(100, 116, 139, 0.15)', text: '#64748b', border: '#94a3b8', label: 'NOT VERIFIED' };
    }
  };

  return (
    <div className="page-stack">
      {/* Top Banner Row */}
      <div className="page-intro-row">
        <div>
          <span className="eyebrow">ZERO-DATA-LEAKAGE VERIFICATION</span>
          <h2>Clean ML Pipeline Verification</h2>
          <p>
            Real executable test suite verifying statistical isolation between training partitions and held-out test sets.
          </p>
        </div>
        <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
          <Link to="/model-performance" className="action-button secondary" style={{ textDecoration: 'none' }}>
            🎯 View Model Performance
          </Link>
          <button
            type="button"
            className="action-button"
            disabled={running}
            style={{
              backgroundColor: '#10b981',
              cursor: running ? 'not-allowed' : 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
            }}
            onClick={handleRunTests}
          >
            {running ? (
              <>
                <span className="spinner" style={{ width: '14px', height: '14px', border: '2px solid #fff', borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
                <span>Executing Test Suite...</span>
              </>
            ) : (
              <>
                <span>▶ Run Pipeline Tests</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Verification Status Summary Strip */}
      <div className="content-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))' }}>
        <div className="panel stat-panel" style={{ borderLeft: '4px solid #10b981' }}>
          <span className="eyebrow">OVERALL STATUS</span>
          <div className="stat-number" style={{ fontSize: '20px', color: '#10b981', marginTop: '6px' }}>
            {overall_status === 'ALL_PASSED' ? 'ALL CHECKS PASSED' : overall_status}
          </div>
          <small>Verified at {timestamp}</small>
        </div>
        <div className="panel stat-panel">
          <span className="eyebrow">PASSED CHECKS</span>
          <div className="stat-number" style={{ color: '#10b981' }}>{summary_counts.passed}</div>
          <small>of {summary_counts.total_checks} automated checks</small>
        </div>
        <div className="panel stat-panel">
          <span className="eyebrow">WARNINGS</span>
          <div className="stat-number" style={{ color: summary_counts.warnings > 0 ? '#f59e0b' : '#10b981' }}>
            {summary_counts.warnings}
          </div>
          <small>Potential leakage flags</small>
        </div>
        <div className="panel stat-panel">
          <span className="eyebrow">FAILURES</span>
          <div className="stat-number" style={{ color: summary_counts.failed > 0 ? '#ef4444' : '#10b981' }}>
            {summary_counts.failed}
          </div>
          <small>Zero tolerance violations</small>
        </div>
        <div className="panel stat-panel">
          <span className="eyebrow">EXECUTION TIME</span>
          <div className="stat-number" style={{ color: '#2563eb' }}>{execution_time_seconds}s</div>
          <small>Isolated probe suite</small>
        </div>
      </div>

      {/* Category Filter Tabs */}
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', margin: '4px 0 16px 0' }}>
        {categories.map((cat) => (
          <button
            key={cat}
            type="button"
            className={`schema-pill ${selectedCategory === cat ? 'active' : ''}`}
            style={{
              cursor: 'pointer',
              background: selectedCategory === cat ? '#1e3a5f' : 'transparent',
              color: selectedCategory === cat ? '#fff' : 'inherit',
              padding: '6px 14px',
              fontSize: '12px',
            }}
            onClick={() => setSelectedCategory(cat)}
          >
            {cat} {cat === 'ALL' ? `(${checks.length})` : `(${checks.filter((c) => c.category === cat).length})`}
          </button>
        ))}
      </div>

      {/* Checks Grid / List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {filteredChecks.map((chk) => {
          const badge = getStatusBadge(chk.status);
          return (
            <div
              key={chk.check_id}
              className="panel"
              style={{
                borderLeft: `4px solid ${badge.border}`,
                display: 'flex',
                flexDirection: 'column',
                gap: '12px',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '8px' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                    <span style={{ fontSize: '11px', fontFamily: 'monospace', color: '#64748b', fontWeight: 600 }}>
                      {chk.check_id}
                    </span>
                    <span className="schema-pill" style={{ fontSize: '11px', padding: '1px 6px' }}>
                      {chk.category}
                    </span>
                  </div>
                  <h3 style={{ margin: 0, fontSize: '18px', color: 'var(--text-heading, #0f172a)' }}>
                    {chk.name}
                  </h3>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <code style={{ fontSize: '12px', color: '#64748b' }}>{chk.file_reference}</code>
                  <span
                    style={{
                      padding: '4px 10px',
                      borderRadius: '4px',
                      fontSize: '12px',
                      fontWeight: 700,
                      backgroundColor: badge.bg,
                      color: badge.text,
                      border: `1px solid ${badge.border}`,
                    }}
                  >
                    {badge.label}
                  </span>
                </div>
              </div>

              <div style={{ fontSize: '13px', lineHeight: 1.5, color: 'var(--text-body, #334155)' }}>
                <strong>Test Objective:</strong> {chk.description}
              </div>

              <div style={{ fontSize: '12.5px', lineHeight: 1.5, color: '#475569' }}>
                <strong>Why This Matters:</strong> {chk.rationale}
              </div>

              <div
                style={{
                  background: 'var(--panel-subtle, #f8fafc)',
                  border: '1px solid #e2e8f0',
                  borderRadius: '6px',
                  padding: '10px 14px',
                  fontSize: '12px',
                  fontFamily: 'monospace',
                  color: '#0f172a',
                  lineHeight: 1.5,
                  overflowX: 'auto',
                }}
              >
                <div style={{ fontSize: '11px', fontWeight: 700, color: '#64748b', marginBottom: '4px', textTransform: 'uppercase' }}>
                  Observed Verification Evidence:
                </div>
                {chk.evidence}
              </div>

              {chk.recommendation && (
                <div
                  style={{
                    background: 'rgba(245, 158, 11, 0.1)',
                    border: '1px solid #f59e0b',
                    borderRadius: '6px',
                    padding: '8px 12px',
                    fontSize: '12px',
                    color: '#b45309',
                  }}
                >
                  <strong>Recommended Corrective Action:</strong> {chk.recommendation}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
