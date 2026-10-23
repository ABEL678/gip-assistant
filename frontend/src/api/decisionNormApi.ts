import { apiClient } from "./client"

// ====== API-клиент для связей Decision ↔ Norm ======

export const decisionNormApi = {
  async linkNorm(decisionId: string, normId: string): Promise<void> {
    await apiClient.post(`/decisions/${decisionId}/norms/${normId}`)
  },

  async unlinkNorm(decisionId: string, normId: string): Promise<void> {
    await apiClient.delete(`/decisions/${decisionId}/norms/${normId}`)
  },

  async fetchNormIds(decisionId: string): Promise<string[]> {
    const { data } = await apiClient.get<string[]>(
      `/decisions/${decisionId}/norms`,
    )
    return data
  },

  async fetchDecisionIds(normId: string): Promise<string[]> {
    const { data } = await apiClient.get<string[]>(
      `/norms/${normId}/decisions`,
    )
    return data
  },
}
