import axios from "axios"

export const apiClient = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
})

// Перехватчик для логирования ошибок (пригодится при отладке)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("[API Error]", error.config?.method?.toUpperCase(), error.config?.url, error.response?.status, error.message)
    return Promise.reject(error)
  }
)