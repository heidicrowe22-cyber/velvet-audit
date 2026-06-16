import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('velvet_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('velvet_token')
      if (!window.location.pathname.includes('/login')) {
         window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export interface Audit {
  id: string;
  website_url: string;
  status: 'pending' | 'running' | 'completed' | 'failed';
  score: number;
  created_at: string;
}

export interface Report {
  audit_id: string;
  categories: {
    name: string;
    score: number;
    issue_count: number;
  }[];
  issues: {
    title: string;
    category: string;
    severity: string;
    impact_description: string;
  }[];
  top_fixes: {
    title: string;
    severity: string;
    impact_description: string;
    price: number;
  }[];
}

// ─── Auth ──────────────────────────────────────────────────────

export const auth = {
  signup: (data: any) => api.post('/auth/signup', data).then(r => r.data),
  login: (data: any) => api.post('/auth/login', data).then(r => r.data),
}

// ─── Websites ──────────────────────────────────────────────────

export const websites = {
  create: (data: any) => api.post('/websites', data).then(r => r.data),
  list: () => api.get('/websites').then(r => r.data),
  get: (id: string) => api.get(`/websites/${id}`).then(r => r.data),
}

// ─── Audits ────────────────────────────────────────────────────

export const audits = {
  start: (data: { website_url: string }): Promise<Audit> => api.post('/audits', data).then(r => r.data),
  list: (): Promise<Audit[]> => api.get('/audits').then(r => r.data),
  get: (id: string): Promise<Audit> => api.get(`/audits/${id}`).then(r => r.data),
  getStatus: (id: string) => api.get(`/audits/${id}/status`).then(r => r.data),
}

// ─── Reports ───────────────────────────────────────────────────

export const reports = {
  get: (auditId: string): Promise<Report> => api.get(`/reports/${auditId}`).then(r => r.data),
}

// ─── Fixes ─────────────────────────────────────────────────────

export const fixes = {
  listPackages: () => api.get('/fixes/packages').then(r => r.data),
  estimate: (data: any) => api.post('/fixes/estimate', data).then(r => r.data),
}

// ─── Orders ────────────────────────────────────────────────────

export const orders = {
  create: (data: any) => api.post('/orders', data).then(r => r.data),
  list: () => api.get('/orders').then(r => r.data),
  get: (id: string) => api.get(`/orders/${id}`).then(r => r.data),
}

export default api
