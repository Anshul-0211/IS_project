import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 errors (unauthorized)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (username, password) => api.post('/auth/login', { username, password }),
  register: (username, password, email) => api.post('/auth/register', { username, password, email }),
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },
};

// Reports API
export const reportsAPI = {
  getAll: (limit = 50, offset = 0) => api.get(`/reports?limit=${limit}&offset=${offset}`),
  getById: (id) => api.get(`/reports/${id}`),
  decrypt: (id) => api.post(`/reports/${id}/decrypt`),
  search: (query) => api.get(`/reports/search?q=${query}`),
  export: () => api.get('/reports/export', { responseType: 'blob' }),
};

// Whitelist API
export const whitelistAPI = {
  getAll: () => api.get('/whitelist'),
  add: (domain, reason) => api.post('/whitelist', { domain, reason }),
  remove: (domain) => api.delete(`/whitelist/${domain}`),
  check: (domain) => api.get(`/whitelist/check/${domain}`),
};

// Statistics API
export const statsAPI = {
  getOverview: () => api.get('/stats/overview'),
  getTrends: (days = 7) => api.get(`/stats/trends?days=${days}`),
  getTopThreats: (limit = 10) => api.get(`/stats/top-threats?limit=${limit}`),
};

// Audit Logs API
export const auditAPI = {
  getAll: (limit = 100, offset = 0) => api.get(`/audit?limit=${limit}&offset=${offset}`),
  getByUser: (username) => api.get(`/audit/user/${username}`),
  getByAction: (action) => api.get(`/audit/action/${action}`),
  export: () => api.get('/audit/export', { responseType: 'blob' }),
};

// Users API
export const usersAPI = {
  getAll: () => api.get('/users'),
  create: (userData) => api.post('/users', userData),
  update: (username, userData) => api.put(`/users/${username}`, userData),
  delete: (username) => api.delete(`/users/${username}`),
};

export default api;
