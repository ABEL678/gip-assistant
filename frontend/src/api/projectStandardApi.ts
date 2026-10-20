import { apiClient } from "./client"

// ====== Типы ======

export type ProjectStandardType = "deadline" | "composition" | "format"

export interface ProjectStandard {
  id: string
  premise_id: string
  type: ProjectStandardType
  value: Record<string, unknown>
  approved_by: string | null
  created_at: string
  updated_at: string
}

export interface ProjectStandardCreate {
  premise_id: string
  type: ProjectStandardType
  value?: Record<string, unknown>
}

export interface ProjectStandardUpdate {
  premise_id?: string
  type?: ProjectStandardType
  value?: Record<string, unknown>
}

// ====== API-клиент ======

export const projectStandardApi = {
  async fetchStandards(premiseId: string): Promise<ProjectStandard[]> {
    const { data } = await apiClient.get<ProjectStandard[]>(
      `/premises/${premiseId}/standards`,
    )
    return data
  },

  async fetchStandard(standardId: string): Promise<ProjectStandard> {
    const { data } = await apiClient.get<ProjectStandard>(
      `/standards/${standardId}`,
    )
    return data
  },

  async createStandard(
    premiseId: string,
    payload: ProjectStandardCreate,
  ): Promise<ProjectStandard> {
    const { data } = await apiClient.post<ProjectStandard>(
      `/premises/${premiseId}/standards`,
      payload,
    )
    return data
  },

  async updateStandard(
    standardId: string,
    payload: ProjectStandardUpdate,
  ): Promise<ProjectStandard> {
    const { data } = await apiClient.patch<ProjectStandard>(
      `/standards/${standardId}`,
      payload,
    )
    return data
  },

  async deleteStandard(standardId: string): Promise<void> {
    await apiClient.delete(`/standards/${standardId}`)
  },
}
