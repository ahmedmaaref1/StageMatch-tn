/**
 * src/api/index.js — Centralized Axios Client for FastAPI Backend
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ── API HELPER METHODS ────────────────────────────────────────────────────────

export const getOffers = async (params = {}) => {
  const response = await api.get('/offers', { params });
  return response.data;
};

export const getOfferById = async (offerId) => {
  const response = await api.get(`/offers/${offerId}`);
  return response.data;
};

export const createOrUpdateStudent = async (studentData) => {
  const response = await api.post('/students', studentData);
  return response.data;
};

export const getStudentById = async (studentId) => {
  const response = await api.get(`/students/${studentId}`);
  return response.data;
};

export const getRecommendations = async (studentId, topK = 10) => {
  const response = await api.get(`/recommendations/${studentId}`, {
    params: { top_k: topK },
  });
  return response.data;
};

export const triggerLiveScrape = async () => {
  const response = await api.post('/offers/scrape');
  return response.data;
};

export const parseStudentCV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/students/parse-cv', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getMarketAnalytics = async () => {
  const response = await api.get('/offers/analytics');
  return response.data;
};

export const getScrapingStatus = async () => {
  const response = await api.get('/offers/scraping/status');
  return response.data;
};

export const triggerManualScraping = async () => {
  const response = await api.post('/offers/scraping/trigger');
  return response.data;
};

export default api;