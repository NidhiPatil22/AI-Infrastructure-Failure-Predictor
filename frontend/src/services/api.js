import axios from 'axios';

const baseURL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '');

const client = axios.create({
  baseURL: `${baseURL}/api`,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

export const getHealth = () => client.get('/health').then(({ data }) => data);
export const getDashboard = () => client.get('/dashboard').then(({ data }) => data);
export const predictRisk = (payload) => client.post('/predict', payload).then(({ data }) => data);
export const getAnalytics = () => client.get('/analytics').then(({ data }) => data);
export const getInfrastructure = () => client.get('/infrastructure').then(({ data }) => data);

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
