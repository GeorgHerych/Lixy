import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? '/api',
  withCredentials: true
});

export async function fetchPosts() {
  const response = await api.get('/posts/');
  return response.data;
}

export async function authenticate(username, password) {
  const response = await api.post('/auth/token/', { username, password });
  const { token } = response.data;
  api.defaults.headers.common.Authorization = `Token ${token}`;
  return token;
}

export default api;
