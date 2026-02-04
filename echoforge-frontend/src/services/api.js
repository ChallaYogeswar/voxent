import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (email, password) => api.post('/auth/login', { email, password }),
  verify: () => api.get('/auth/verify'),
};

// Upload and Processing API
export const uploadAPI = {
  uploadAudio: (formData) => 
    api.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getStatus: (jobId) => api.get(`/status/${jobId}`),
};

// Download API
export const downloadAPI = {
  getSpeakerAudio: (jobId, speakerId) => 
    api.get(`/download/${jobId}/${speakerId}`, { responseType: 'blob' }),
  getOriginalAudio: (jobId) => 
    api.get(`/download/${jobId}/original`, { responseType: 'blob' }),
  getMetadata: (jobId) => api.get(`/download/${jobId}/metadata.json`),
};

// Training API
export const trainingAPI = {
  uploadTrainingData: (formData) => 
    api.post('/train/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  startTraining: (data) => api.post('/train/start', data),
  getTrainingStatus: (trainingJobId) => api.get(`/train/status/${trainingJobId}`),
};

// Analytics API
export const analyticsAPI = {
  getUserAnalytics: () => api.get('/analytics/user'),
  getJobHistory: (limit = 20, offset = 0) => 
    api.get(`/analytics/jobs?limit=${limit}&offset=${offset}`),
};

export default api;
