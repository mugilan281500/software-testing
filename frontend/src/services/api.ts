import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getLiveMonitoringFeed = async () => (await api.get('/monitoring/live-feed')).data;
export const getTransactionScorecard = async (txId: string) => (await api.get(`/monitoring/transactions/${txId}/scorecard`)).data;
export const getRiskTimeline = async () => (await api.get('/monitoring/timeline')).data;
export const getUserBaseline = async (accountNum: string) => (await api.get(`/monitoring/baseline/${accountNum}`)).data;

export const executeManualTransfer = async (payload: { sender_account: string; receiver_account: string; amount: number; currency?: string; device_id?: string; ip_address?: string }) =>
  (await api.post('/mock-bank/transfer', payload)).data;

export const getMockAccounts = async () => (await api.get('/mock-bank/accounts')).data;
export const getBeneficiaries = async (acc: string) => (await api.get(`/mock-bank/beneficiaries/${acc}`)).data;
export const getSandboxToggles = async () => (await api.get('/mock-bank/sandbox/toggles')).data;
export const updateSandboxToggle = async (key: string, is_enabled: boolean) =>
  (await api.put('/mock-bank/sandbox/toggles', { key, is_enabled })).data;

export const getSimulationScenarios = async () => (await api.get('/simulation/scenarios')).data;
export const runSimulationScenario = async (scenario_key: string, sender_account?: string, receiver_account?: string) =>
  (await api.post('/simulation/run-scenario', { scenario_key, sender_account, receiver_account })).data;

export const getSecurityIncidents = async () => (await api.get('/incidents')).data;
export const updateIncidentStatus = async (code: string, status: string, notes?: string, marked_by?: string) =>
  (await api.put(`/incidents/${code}/status`, { status, resolution_notes: notes, marked_by })).data;
export const markFalsePositive = async (code: string, is_false_positive: boolean, tester_name: string, reason: string) =>
  (await api.post(`/incidents/${code}/mark-false-positive`, { is_false_positive, tester_name, reason })).data;

export const getSecurityAlerts = async () => (await api.get('/flags')).data;

export const getAdaptiveTestQueue = async () => (await api.get('/tests/queue')).data;
export const runFullAutomatedTest = async () => (await api.post('/tests/run-full')).data;
export const runSelectedTests = async (modules: string[]) => (await api.post('/tests/run-selected', { modules })).data;
export const getTestRunsHistory = async () => (await api.get('/tests/runs')).data;
export const getTestRunDetails = async (id: number) => (await api.get(`/tests/runs/${id}`)).data;
export const importOpenApiSpec = async (title: string, version: string, endpoints_json: any[]) =>
  (await api.post('/tests/openapi-import', { title, version, endpoints_json })).data;

export const getSecurityRules = async () => (await api.get('/rules/security')).data;
export const updateSecurityRule = async (rule_key: string, is_enabled?: boolean, weight?: number, params?: any) =>
  (await api.put('/rules/security', { rule_key, is_enabled, weight, params })).data;
export const getBankingRules = async () => (await api.get('/rules/banking')).data;
export const updateBankingRule = async (rule_code: string, is_enabled?: boolean, threshold_value?: number, action_on_fail?: string, risk_weight?: number) =>
  (await api.put('/rules/banking', { rule_code, is_enabled, threshold_value, action_on_fail, risk_weight })).data;

export const getSecurityPosture = async () => (await api.get('/posture')).data;
export const getBeforeAfterComparison = async () => (await api.get('/posture/comparison')).data;

export const getApiInventory = async () => (await api.get('/apis')).data;
export const getSecurityFindings = async () => (await api.get('/findings')).data;
export const getAuditLogs = async () => (await api.get('/reports/audit-logs')).data;

export const generateReport = async (title: string, format: string) => (await api.post('/reports/generate', { title, format })).data;
export const getReportsList = async () => (await api.get('/reports')).data;

export default api;
