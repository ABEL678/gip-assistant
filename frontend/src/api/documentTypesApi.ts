import { apiClient } from "./client"

// ====== Типы ======

export interface DocumentType {
  id: string
  code: string
  name: string
  description: string | null
  gost_code: string | null
  created_at: string
}

// ====== API-клиент ======

export const documentTypesApi = {
  // ---------- DocumentType ----------

  async getAll(): Promise<DocumentType[]> {
    const { data } = await apiClient.get<DocumentType[]>("/document-types")
    return data
  },

  async getById(id: string): Promise<DocumentType> {
    const { data } = await apiClient.get<DocumentType>(`/document-types/${id}`)
    return data
  },

  async getByCode(code: string): Promise<DocumentType> {
    const { data } = await apiClient.get<DocumentType>(`/document-types/by-code/${code}`)
    return data
  },

  async create(
    payload: {
      code: string
      name: string
      description?: string | null
      gost_code?: string | null
    },
  ): Promise<DocumentType> {
    const { data } = await apiClient.post<DocumentType>("/document-types", payload)
    return data
  },

  async update(
    id: string,
    payload: Partial<Pick<DocumentType, "name" | "description" | "gost_code">>,
  ): Promise<DocumentType> {
    const { data } = await apiClient.patch<DocumentType>(`/document-types/${id}`, payload)
    return data
  },

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/document-types/${id}`)
  },
}
