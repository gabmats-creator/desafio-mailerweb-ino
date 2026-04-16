import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:8080/mailerweb/v1', 
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('@MailerWeb:token');

  if (token) {
    config.headers.set('Authorization', `Bearer ${token}`);
  }
  
  return config;
}, (error) => {
  return Promise.reject(error);
});