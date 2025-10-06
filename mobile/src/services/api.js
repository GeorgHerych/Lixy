import axios from 'axios';

const api = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000/api',
  timeout: 8000
});

export async function fetchPosts() {
  const response = await api.get('/posts/');
  return response.data;
}

export default api;
