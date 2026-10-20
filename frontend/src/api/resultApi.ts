import { apiClient } from "./client"

// ====== Типы ======

export interface Result {
  id: string
  project_id: string
  formulation: string
  source: string | null
  approved_by: string | null
  created_at: string
  updated_at: string
}

export interface ResultCreate {
  formulation: string
  source?: string | null
}

export interface ResultUpdate {
  formulation?: string
  source?: string | null
}

// ====== API-клиент ======

export const resultApi = {
  async fetchResults(projectId: string): Promise<Result[]> {
    const { data } = await apiClient.get<Result[]>(
      `/projects/${projectId}/results`,
    )
    return data
  },

  async fetchResult(resultId: string): Promise<Result> {
    const { data } = await apiClient.get<Result>(`/results/${resultId}`)
    return data
  },

  async createResult(
    projectId: string,
    payload: ResultCreate,
  ): Promise<Result> {
    const { data } = await apiClient.post<Result>(
      `/projects/${projectId}/results`,
      payload,
    )
    return data
  },

  async updateResult(
    resultId: string,
    payload: ResultUpdate,
  ): Promise<Result> {
    const { data } = await apiClient.patch<Result>(
      `/results/${resultId}`,
      payload,
    )
    return data
  },

  async deleteResult(resultId: string): Promise<void> {
    await apiClient.delete(`/results/${resultId}`)
  },
}
