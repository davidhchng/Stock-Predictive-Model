/**
 * API service for communicating with the backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Response Error:', error);
    if (error.response) {
      // Server responded with error status
      throw new Error(error.response.data.detail || 'Server error occurred');
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error - please check your connection');
    } else {
      // Something else happened
      throw new Error('An unexpected error occurred');
    }
  }
);

// API service functions
export const apiService = {
  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Ticker endpoints
  getTickers: async () => {
    const response = await api.get('/tickers');
    return response.data;
  },

  checkTickerExists: async (ticker) => {
    const response = await api.get(`/tickers/${ticker}/exists`);
    return response.data;
  },

  // Stock data endpoints
  getStockData: async (ticker, startDate = null, endDate = null) => {
    const params = {};
    if (startDate) params.start_date = startDate;
    if (endDate) params.end_date = endDate;
    
    const response = await api.get(`/stocks/${ticker}/data`, { params });
    return response.data;
  },

  getLatestStockData: async (ticker) => {
    const response = await api.get(`/stocks/${ticker}/latest`);
    return response.data;
  },

  // Technical analysis endpoints
  getTechnicalAnalysis: async (ticker) => {
    const response = await api.get(`/analysis/${ticker}/technical`);
    return response.data;
  },

  getTechnicalIndicators: async (ticker) => {
    const response = await api.get(`/analysis/${ticker}/indicators`);
    return response.data;
  },

  // Seasonality analysis endpoints
  getSeasonalityAnalysis: async (ticker) => {
    const response = await api.get(`/analysis/${ticker}/seasonality`);
    return response.data;
  },

  getSeasonalityHeatmap: async (ticker, periodType = 'monthly') => {
    const response = await api.get(`/analysis/${ticker}/seasonality/heatmap`, {
      params: { period_type: periodType }
    });
    return response.data;
  },

  // Prediction endpoints
  getPrediction: async (ticker) => {
    const response = await api.get(`/prediction/${ticker}`);
    return response.data;
  },

  // Comprehensive analysis endpoints
  getComprehensiveAnalysis: async (ticker) => {
    const response = await api.get(`/analysis/${ticker}/comprehensive`);
    return response.data;
  },

  getAnalysisSummary: async (ticker) => {
    const response = await api.get(`/analysis/${ticker}/summary`);
    return response.data;
  },

  // Data management endpoints
  getDataStatus: async () => {
    const response = await api.get('/data/status');
    return response.data;
  },
};

export default apiService;
