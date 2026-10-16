import axios from 'axios';

const baseURL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

const client = axios.create({
  baseURL: `${baseURL}/api`,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

export const getHealth = () => client.get('/health').then(({ data }) => data);
export const getDashboard = () => client.get('/dashboard').then(({ data }) => data);
export const getPopularCorridors = () => client.get('/corridors').then(({ data }) => data);
export const predictRisk = (payload) => client.post('/predict', payload).then(({ data }) => data);
export const getAnalytics = () => client.get('/analytics').then(({ data }) => data);
export const getInfrastructure = () => client.get('/infrastructure').then(({ data }) => data);
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

export const getAuditSummary = () => client.get('/audit/summary').then(({ data }) => data);
export const getAuditFindings = (params = {}) => client.get('/audit/findings', { params }).then(({ data }) => data);
export const runPipelineTests = () => client.post('/pipeline-tests/run').then(({ data }) => data);
export const getPipelineTestResults = () => client.get('/pipeline-tests/results').then(({ data }) => data);

export const exportAuditCsvUrl = `${baseURL}/api/audit/export/csv`;
export const exportAuditJsonUrl = `${baseURL}/api/audit/export/json`;

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
