import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  // Courses
  getCourses: (language = 'ur') => 
    api.get(`/api/courses?language=${language}`),
  
  getCourse: (id, language = 'ur') => 
    api.get(`/api/courses/${id}?language=${language}`),

  // Market Prices
  getMarketPrices: (cropName = null, region = null) => {
    const params = new URLSearchParams();
    if (cropName) params.append('crop_name', cropName);
    if (region) params.append('region', region);
    return api.get(`/api/market-prices?${params.toString()}`);
  },

  getPriceForecast: (cropName, region = null) => {
    const params = region ? `?region=${region}` : '';
    return api.get(`/api/market-prices/forecast/${cropName}${params}`);
  },

  // Weather Alerts
  getWeatherAlerts: (region = null, language = 'ur') => {
    const params = new URLSearchParams();
    if (region) params.append('region', region);
    params.append('language', language);
    return api.get(`/api/weather-alerts?${params.toString()}`);
  },

  // Pest Alerts
  getPestAlerts: (region = null, language = 'ur') => {
    const params = new URLSearchParams();
    if (region) params.append('region', region);
    params.append('language', language);
    return api.get(`/api/pest-alerts?${params.toString()}`);
  },

  // Wiki Articles
  getWikiArticles: (category = null, language = 'ur') => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    params.append('language', language);
    return api.get(`/api/wiki?${params.toString()}`);
  },

  getWikiArticle: (id, language = 'ur') => 
    api.get(`/api/wiki/${id}?language=${language}`),

  // Chat
  sendChatMessage: (message, userId = null, language = 'ur') => 
    api.post('/api/chat', {
      user_id: userId,
      question: message,
      language: language,
    }),

  // Users
  createUser: (userData) => 
    api.post('/api/users', userData),

  getUser: (userId) => 
    api.get(`/api/users/${userId}`),
};

export default api;

