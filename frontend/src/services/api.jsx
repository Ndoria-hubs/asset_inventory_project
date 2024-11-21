// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://ht-json-server-vercel.vercel.app/',
});

export default api;
