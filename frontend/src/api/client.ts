import axios from "axios"

export const apiClient = axios.create({
  baseURL: "/api",
  timeout: 30000,
  // ⚠️ НЕ задаём Content-Type здесь!
  // Axios сам подставит:
  //   - application/json для обычных объектов
  //   - multipart/form-data с boundary для FormData
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error(
      "[API Error]",
      error.config?.method?.toUpperCase(),
      error.config?.url,
      error.response?.status,
      error.response?.data,
      error.message,
    )
    return Promise.reject(error)
  },
)