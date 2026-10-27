import axios from 'axios';

const baseURL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

const client = axios.create({
  baseURL: `${baseURL}/api`,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

export const getHealth = () => client.get('/health').then(({ data }) => data);

// 1. Dashboard & Live Infrastructure Counters
export const getDashboard = () => client.get('/dashboard').then(({ data }) => data);
export const getInfrastructureStats = () => client.get('/dashboard/infrastructure-stats').then(({ data }) => data);
export const getInfrastructureTrend = () => client.get('/dashboard/infrastructure-trend').then(({ data }) => data);
export const getRiskBreakdown = () => client.get('/dashboard/risk-breakdown').then(({ data }) => data);
export const getAssetTypeRisk = () => client.get('/dashboard/asset-type-risk').then(({ data }) => data);
export const getZoneRisk = () => client.get('/dashboard/zone-risk').then(({ data }) => data);

// 2. Pune Infrastructure Assets & GIS Map Queries
export const getInfrastructure = (params = {}) => client.get('/infrastructure', { params }).then(({ data }) => data);
export const getInfrastructureGeoConfig = () => client.get('/infrastructure/config').then(({ data }) => data);
export const getInfrastructureAssetDetail = (assetId) =>
  client.get(`/infrastructure/${encodeURIComponent(assetId)}`).then(({ data }) => data);

// 3. Field Damage Inspections & Reporting
export const getDamageReports = (params = {}) => client.get('/damage-reports', { params }).then(({ data }) => data);
export const getDamageReportById = (reportId) =>
  client.get(`/damage-reports/${encodeURIComponent(reportId)}`).then(({ data }) => data);
export const submitDamageReport = (formData) =>
  client
    .post('/damage-reports', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    .then(({ data }) => data);
export const updateDamageReportStatus = (reportId, status) =>
  client.patch(`/damage-reports/${encodeURIComponent(reportId)}/status`, { status }).then(({ data }) => data);

// 4. ML Predictions & Corridors
export const getPopularCorridors = () => client.get('/corridors').then(({ data }) => data);
export const predictRisk = (payload) => client.post('/predict', payload).then(({ data }) => data);

// 5. Maintenance Priority Queue & Optimization
export const getPrioritizedQueue = (limit = 50) =>
  client.get('/optimization/priority-queue', { params: { limit } }).then(({ data }) => data);
export const compareOptimization = (payload) =>
  client.post('/optimization/compare', payload).then(({ data }) => data);

// 6. ROVER AI Assistant
export const sendChatMessage = (
  message = null,
  history = [],
  provider = null,
  workflow = 'main',
  step = 'menu',
  selectedChoiceId = null
) =>
  client
    .post('/chat', {
      message,
      history,
      provider,
      workflow,
      step,
      selected_choice_id: selectedChoiceId,
    })
    .then(({ data }) => data);
export const getChatStatus = (provider = null) =>
  client.get('/chat/status', { params: provider ? { provider } : {} }).then(({ data }) => data);

// 7. Dataset Quality & Audit
export const getAuditSummary = () => client.get('/audit/summary').then(({ data }) => data);
export const getAuditFindings = (params = {}) => client.get('/audit/findings', { params }).then(({ data }) => data);
export const runPipelineTests = () => client.post('/pipeline-tests/run').then(({ data }) => data);
export const getPipelineTestResults = () => client.get('/pipeline-tests/results').then(({ data }) => data);

export const exportAuditCsvUrl = `${baseURL}/api/audit/export/csv`;
export const exportAuditJsonUrl = `${baseURL}/api/audit/export/json`;
export const getDamageImageUrl = (reportId) => `${baseURL}/api/damage-reports/${encodeURIComponent(reportId)}/image`;

export function getApiErrorMessage(error) {
  if (!error?.response) {
    return 'Unable to connect to the prediction server. Make sure the FastAPI backend is running.';
  }
  if (typeof error.response.data?.detail === 'string') {
    return error.response.data.detail;
  }
  if (error.response.status === 422) {
    return 'The server rejected the submitted values. Check the form and try again.';
  }
  return `The server could not complete this request (HTTP ${error.response.status}). Please try again.`;
}
