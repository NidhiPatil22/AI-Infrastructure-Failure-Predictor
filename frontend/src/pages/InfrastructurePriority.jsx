import { useCallback, useEffect, useMemo, useState } from 'react';
import ErrorMessage from '../components/ErrorMessage.jsx';
import Loading from '../components/Loading.jsx';
import { getApiErrorMessage, getPrioritizedQueue, compareOptimization } from '../services/api.js';

export default function InfrastructurePriority() {
  const [state, setState] = useState({ loading: true, error: '', queue: [] });
  const [riskFilter, setRiskFilter] = useState('all');
  const [typeFilter, setTypeFilter] = useState('all');
  const [priorityFilter, setPriorityFilter] = useState('all');
  const [search, setSearch] = useState('');
  const [selectedAsset, setSelectedAsset] = useState(null);

  // Optimization Modal / Panel State
  const [optimizing, setOptimizing] = useState(false);
  const [optimizationResult, setOptimizationResult] = useState(null);

  const load = useCallback(async () => {
    setState({ loading: true, error: '', queue: [] });
    try {
      const response = await getPrioritizedQueue(100);
      setState({
        loading: false,
        error: '',
        queue: Array.isArray(response?.priority_queue) ? response.priority_queue : [],
      });
    } catch (error) {
      setState({ loading: false, error: getApiErrorMessage(error), queue: [] });
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const handleRunOptimizer = async () => {
    setOptimizing(true);
    try {
      const res = await compareOptimization({
        budget_limit: 65000,
        capacity_limit: 180,
      });
      setOptimizationResult(res?.comparison);
    } catch (err) {
      console.error('Failed to run optimizer:', err);
    } finally {
      setOptimizing(false);
    }
  };

  const types = useMemo(
    () => [...new Set(state.queue.map((a) => a.asset_type).filter(Boolean))].sort(),
    [state.queue]
  );

  const filtered = useMemo(() => {
    return state.queue.filter((asset) => {
      const q = search.toLowerCase();
      const matchesSearch =
        !search ||
        String(asset.display_type || '').toLowerCase().includes(q) ||
        String(asset.road_class || '').toLowerCase().includes(q) ||
        String(asset.asset_type || '').toLowerCase().includes(q) ||
        String(asset.locality || '').toLowerCase().includes(q) ||
        String(asset.pune_ward || '').toLowerCase().includes(q);

      const matchesRisk =
        riskFilter === 'all' || String(asset.risk_level || '').toLowerCase() === riskFilter.toLowerCase();

      const matchesType = typeFilter === 'all' || asset.asset_type === typeFilter;

      const matchesPriority =
        priorityFilter === 'all' || String(asset.priority || '').toLowerCase() === priorityFilter.toLowerCase();

      return matchesSearch && matchesRisk && matchesType && matchesPriority;
    });
  }, [state.queue, search, riskFilter, typeFilter, priorityFilter]);

  if (state.loading) return <Loading label="Evaluating Pune maintenance priority queue..." />;
  if (state.error) return <ErrorMessage message={state.error} onRetry={load} />;

  const criticalCount = state.queue.filter((a) => a.priority === 'CRITICAL').length;
  const highCount = state.queue.filter((a) => a.priority === 'HIGH').length;

  return (
    <div className="page-stack">
      {/* Priority Queue Banner */}
      <div className="priority-banner">
        <div>
          <span className="eyebrow">INTELLIGENT MAINTENANCE TRIAGE</span>
          <h2>Civil Infrastructure Priority Queue</h2>
          <p>
            Multi-factor prioritization combining <strong>ML Failure Risk</strong>,{' '}
            <strong>Remaining Useful Life (RUL)</strong>, and <strong>Field Damage Inspections</strong>.
            Reported defects escalate priority without overwriting baseline predictive telemetry.
          </p>
        </div>
        <div className="priority-actions">
          <div className="priority-count">
            <strong>{filtered.length}</strong>
            <span>Active Triage Items</span>
          </div>
          <button
            type="button"
            className="primary-button optimizer-trigger-btn"
            onClick={handleRunOptimizer}
            disabled={optimizing}
          >
            {optimizing ? 'Computing Knapsack Schedule...' : '⚡ Run Search Space Optimizer'}
          </button>
        </div>
      </div>

      {/* Optimization Schedule Results Modal / Banner */}
      {optimizationResult && (
        <section className="panel optimization-results-panel">
          <div className="section-heading">
            <div>
              <span className="eyebrow">CONSTRAINED CAPITAL OPTIMIZATION</span>
              <h2>Knapsack Schedule: Hill Climbing vs. Beam vs. Tabu Search</h2>
              <p>Search-space comparison maximizing risk mitigation within budget and labor hour caps.</p>
            </div>
            <button
              type="button"
              className="secondary-button"
              onClick={() => setOptimizationResult(null)}
            >
              Close
            </button>
          </div>

          <div className="optimizer-cards-grid">
            {optimizationResult.comparison_table?.map((item) => (
              <div
                key={item.algorithm}
                className={`optimizer-plan-card ${item.algorithm.includes('Tabu') ? 'best-plan' : ''}`}
              >
                <div className="plan-algo-header">
                  <strong>{item.algorithm}</strong>
                  {item.algorithm.includes('Tabu') && <span className="best-tag">Highest Objective</span>}
                </div>
                <div className="plan-objective">
                  Score: <strong>{Number(item.objective_value).toFixed(2)}</strong>
                </div>
                <div className="plan-stats">
                  <span>Selected Assets: <strong>{item.selected_assets_count}</strong></span>
                  <span>Cost: <strong>${Number(item.total_cost).toLocaleString()}</strong></span>
                  <span>Labor: <strong>{item.total_capacity_hours} hrs</strong></span>
                  <span>Feasible: <strong className="text-green">✓ Yes</strong></span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Filter Toolbar */}
      <section className="panel">
        <div className="filter-bar">
          <label className="search-field">
            <span aria-hidden="true">⌕</span>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search Asset ID, locality, or ward..."
              aria-label="Search assets"
            />
          </label>

          <label className="filter-field">
            <span>Priority Triage</span>
            <select value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value)}>
              <option value="all">All Priorities</option>
              <option value="critical">Critical (Immediate)</option>
              <option value="high">High (30 Days)</option>
              <option value="medium">Medium (Scheduled)</option>
              <option value="low">Low (Monitoring)</option>
            </select>
          </label>

          <label className="filter-field">
            <span>Infrastructure Type</span>
            <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
              <option value="all">All Types</option>
              {types.map((item) => (
                <option key={item} value={item}>
                  {item}
                </option>
              ))}
            </select>
          </label>

          <label className="filter-field">
            <span>Model Risk Tier</span>
            <select value={riskFilter} onChange={(e) => setRiskFilter(e.target.value)}>
              <option value="all">All Risks</option>
              <option value="high">High Risk</option>
              <option value="medium">Medium Risk</option>
              <option value="low">Low Risk</option>
            </select>
          </label>

          <button
            className="secondary-button filter-reset"
            onClick={() => {
              setRiskFilter('all');
              setTypeFilter('all');
              setPriorityFilter('all');
              setSearch('');
            }}
          >
            Clear Filters
          </button>
        </div>

        {/* Prioritized Assets Cards / Table */}
        <div className="priority-queue-table-wrap">
          <table className="priority-table">
            <thead>
              <tr>
                <th>Priority Level</th>
                <th>Infrastructure Segment</th>
                <th>Pune Location</th>
                <th>ML Predicted Risk & RUL</th>
                <th>Why Was Priority Assigned? (Reasons)</th>
                <th>Recommended Action</th>
                <th>Est. Repair</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((item, idx) => {
                const priorityClass =
                  item.priority === 'CRITICAL'
                    ? 'prio-critical'
                    : item.priority === 'HIGH'
                    ? 'prio-high'
                    : item.priority === 'MEDIUM'
                    ? 'prio-medium'
                    : 'prio-low';

                const prob = Number(item.failure_probability || 0);
                const rulDays = item.remaining_useful_life_days != null
                  ? item.remaining_useful_life_days
                  : Math.round(Number(item.remaining_useful_life || 0) * 365);

                const displayType = item.display_type || (item.road_class ? `${item.road_class} ${item.asset_type}` : item.asset_type || 'Road Infrastructure');
                const condLabel = item.condition_label || (item.condition_score < 50 ? 'Poor' : (item.condition_score < 75 ? 'Fair' : 'Good'));

                return (
                  <tr key={item.asset_id || `infra-prio-${idx}`} className={`prio-row ${priorityClass}`}>
                    <td>
                      <span className={`prio-pill ${priorityClass}`}>
                        {item.priority === 'CRITICAL' ? '🚨 CRITICAL' : item.priority}
                      </span>
                    </td>
                    <td>
                      <strong className="infra-segment-title">{displayType}</strong>
                      <div className="table-subtext">
                        <span className={`infra-condition-tag condition-${condLabel.toLowerCase()}`}>{condLabel} Condition</span>
                        {item.material ? ` · ${item.material}` : ''}
                      </div>
                    </td>
                    <td>
                      <div><strong>{item.locality || 'Pune'}</strong></div>
                      <small className="text-muted">{item.pune_ward || 'PMC Sector'}</small>
                    </td>
                    <td>
                      <div>
                        Risk: <strong>{(prob * 100).toFixed(1)}%</strong>
                      </div>
                      <small className="text-muted">{rulDays} days estimated RUL</small>
                    </td>
                    <td className="reasons-cell">
                      <ul className="priority-reasons-list">
                        {item.priority_reasons?.map((reason, rIdx) => (
                          <li key={rIdx} className={reason.includes('damage') ? 'reason-damage' : ''}>
                            {reason.includes('damage') ? '⚠️ ' : '• '}
                            {reason}
                          </li>
                        ))}
                      </ul>
                    </td>
                    <td className="action-cell">
                      <p className="rec-text">{item.recommended_action}</p>
                    </td>
                    <td className="cost-cell">
                      <strong>${(item.estimated_repair_cost || 5000).toLocaleString()}</strong>
                      <small>{item.estimated_labor_hours || 20} hrs</small>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        <div className="table-footnote">
          Priority calculations evaluate active field damage reports alongside predictive regression/classification
          outputs without overwriting the underlying trained ML model predictions.
        </div>
      </section>
    </div>
  );
}
