import { useCallback, useEffect, useMemo, useState } from 'react';
import ErrorMessage from '../components/ErrorMessage.jsx';
import InfrastructureTable from '../components/InfrastructureTable.jsx';
import Loading from '../components/Loading.jsx';
import { getApiErrorMessage, getInfrastructure } from '../services/api.js';

export default function InfrastructurePriority() {
  const [state, setState] = useState({ loading: true, error: '', assets: [] });
  const [risk, setRisk] = useState('all');
  const [type, setType] = useState('all');
  const [zone, setZone] = useState('all');
  const [search, setSearch] = useState('');

  const load = useCallback(async () => {
    setState({ loading: true, error: '', assets: [] });
    try {
      const response = await getInfrastructure();
      setState({ loading: false, error: '', assets: Array.isArray(response?.assets) ? response.assets : [] });
    } catch (error) {
      setState({ loading: false, error: getApiErrorMessage(error), assets: [] });
    }
  }, []);
  useEffect(() => { load(); }, [load]);

  const types = useMemo(() => [...new Set(state.assets.map((asset) => asset.asset_type).filter(Boolean))].sort(), [state.assets]);
  const zones = useMemo(() => [...new Set(state.assets.map((asset) => asset.zone).filter(Boolean))].sort(), [state.assets]);
  const filtered = useMemo(() => state.assets.filter((asset) => (
    (risk === 'all' || String(asset.risk_level).toLowerCase() === risk)
    && (type === 'all' || asset.asset_type === type)
    && (zone === 'all' || asset.zone === zone)
    && String(asset.asset_id || '').toLowerCase().includes(search.toLowerCase())
  )), [state.assets, risk, type, zone, search]);

  if (state.loading) return <Loading label="Loading infrastructure history..." />;
  if (state.error) return <ErrorMessage message={state.error} onRetry={load} />;

  return (
    <div className="page-stack">
      <div className="priority-banner"><div><span className="eyebrow">MAINTENANCE QUEUE</span><h2>Assets requiring immediate attention</h2><p>The API returns up to 20 most recent saved predictions, not a complete asset inventory.</p></div><div className="priority-count"><strong>{filtered.length}</strong><span>visible records</span></div></div>
      <section className="panel">
        <div className="filter-bar">
          <label className="search-field"><span aria-hidden="true">⌕</span><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search Asset ID" aria-label="Search Asset ID" /></label>
          <label className="filter-field"><span>Risk level</span><select value={risk} onChange={(event) => setRisk(event.target.value)}><option value="all">All risks</option><option value="high">High</option><option value="medium">Medium</option><option value="low">Low</option></select></label>
          <label className="filter-field"><span>Infrastructure type</span><select value={type} onChange={(event) => setType(event.target.value)}><option value="all">All types</option>{types.map((item) => <option key={item}>{item}</option>)}</select></label>
          <label className="filter-field"><span>Zone</span><select value={zone} onChange={(event) => setZone(event.target.value)}><option value="all">All zones</option>{zones.map((item) => <option key={item}>{item}</option>)}</select></label>
          <button className="secondary-button filter-reset" onClick={() => { setRisk('all'); setType('all'); setZone('all'); setSearch(''); }}>Clear filters</button>
        </div>
        <InfrastructureTable assets={filtered} />
        <div className="table-footnote">Failure probability and priority are not included in the infrastructure-history route, so these columns are explicitly marked unavailable.</div>
      </section>
    </div>
  );
}
