import axios from "axios";

const api = axios.create({
  baseURL: "https://todocontablecr-bca0o637a-mario-vs-projects.vercel.app",
  headers: { "Content-Type": "application/json" }
});

// Agregar token automáticamente si existe
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default api;
