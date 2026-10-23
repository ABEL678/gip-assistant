import { apiClient } from "./client"

// ====== Типы ======

export type NormType = "gost" | "snip" | "npa" | "xml_schema" | "other"

export const NORM_TYPE_LABELS: Record<NormType, string> = {
  gost: "ГОСТ",
  snip: "СНиП",
  npa: "НПА",
  xml_schema: "XML Schema",
  other: "Другое",
}

export interface Norm {
  id: string
  project_id: string
  code: string
  title: string
  norm_type: NormType
  issued_at: string | null
  source_url: string | null
  document_id: string | null
  created_at: string | null
  updated_at: string | null
}

export interface NormCreate {
  code: string
  title: string
  norm_type: NormType
  issued_at?: string | null
  source_url?: string | null
  document_id?: string | null
}

export interface NormUpdate {
  code?: string
  title?: string
  norm_type?: NormType
  issued_at?: string | null
  source_url?: string | null
  document_id?: string | null
}

// ====== API-клиент ======

export const normApi = {
  async fetchNorms(projectId: string): Promise<Norm[]> {
    const { data } = await apiClient.get<Norm[]>(
      `/projects/${projectId}/norms`,
    )
    return data
  },

  async createNorm(
    projectId: string,
    payload: NormCreate,
  ): Promise<Norm> {
    const { data } = await apiClient.post<Norm>(
      `/projects/${projectId}/norms`,
      payload,
    )
    return data
  },

  async getNorm(normId: string): Promise<Norm> {
    const { data } = await apiClient.get<Norm>(`/norms/${normId}`)
    return data
  },

  async updateNorm(
    normId: string,
    payload: NormUpdate,
  ): Promise<Norm> {
    const { data } = await apiClient.patch<Norm>(`/norms/${normId}`, payload)
    return data
  },

  async deleteNorm(normId: string): Promise<void> {
    await apiClient.delete(`/norms/${normId}`)
  },
}
