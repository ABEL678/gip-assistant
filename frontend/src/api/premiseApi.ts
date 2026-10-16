import { apiClient } from "./client"

// ====== Типы ======

export type PremiseCategory =
  | "contract"
  | "tz"
  | "customer_requirement"
  | "source_data"
  | "norm"
  | "npa"
  | "bureaucracy"
  | "internal"

export interface Premise {
  id: string
  project_id: string
  category: PremiseCategory
  name: string
  source: string | null
  date: string | null
  actual: boolean
  mandatory: boolean
  link: string | null
  valid_until: string | null
  data: Record<string, unknown>
  schema: Record<string, unknown>
  created_at: string
  updated_at: string
}

export interface PremiseCreate {
  category: PremiseCategory
  name: string
  source?: string | null
  date?: string | null
  actual?: boolean
  mandatory?: boolean
  link?: string | null
  valid_until?: string | null
  data?: Record<string, unknown>
  field_schema?: Record<string, unknown>
}

export interface PremiseUpdate {
  category?: PremiseCategory
  name?: string
  source?: string | null
  date?: string | null
  actual?: boolean
  mandatory?: boolean
  link?: string | null
  valid_until?: string | null
  data?: Record<string, unknown>
  field_schema?: Record<string, unknown>
}

// ====== API-клиент ======

export const premiseApi = {
  async fetchPremises(projectId: string): Promise<Premise[]> {
    const { data } = await apiClient.get<Premise[]>(
      `/projects/${projectId}/premises`,
    )
    return data
  },

  async fetchPremise(premiseId: string): Promise<Premise> {
    const { data } = await apiClient.get<Premise>(`/premises/${premiseId}`)
    return data
  },

  async createPremise(
    projectId: string,
    payload: PremiseCreate,
  ): Promise<Premise> {
    const { data } = await apiClient.post<Premise>(
      `/projects/${projectId}/premises`,
      payload,
    )
    return data
  },

  async updatePremise(
    premiseId: string,
    payload: PremiseUpdate,
  ): Promise<Premise> {
    const { data } = await apiClient.patch<Premise>(
      `/premises/${premiseId}`,
      payload,
    )
    return data
  },

  async deletePremise(premiseId: string): Promise<void> {
    await apiClient.delete(`/premises/${premiseId}`)
  },
}
