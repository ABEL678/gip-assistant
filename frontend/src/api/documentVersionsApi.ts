import { apiClient } from "./client"

// ====== Типы ======

export interface DocumentVersion {
  id: string
  document_id: string
  version: string
  change_number: number | null
  file_path: string
  file_name: string
  hash_sha256: string
  format_original: string
  format_archive: string | null
  size_bytes: number
  is_current: boolean
  uploaded_by: string | null
  uploaded_at: string
}

// ====== API-клиент ======

export const documentVersionsApi = {
  // ---------- DocumentVersion ----------

  async listByDocument(documentId: string): Promise<DocumentVersion[]> {
    const { data } = await apiClient.get<DocumentVersion[]>(
      `/documents/${documentId}/versions`,
    )
    return data
  },

  async getCurrent(documentId: string): Promise<DocumentVersion> {
    const { data } = await apiClient.get<DocumentVersion>(
      `/documents/${documentId}/versions/current`,
    )
    return data
  },

  async getById(versionId: string): Promise<DocumentVersion> {
    const { data } = await apiClient.get<DocumentVersion>(
      `/document-versions/${versionId}`,
    )
    return data
  },

  async create(
    documentId: string,
    payload: {
      version: string
      file_path: string
      file_name: string
      hash_sha256: string
      format_original: string
      format_archive?: string | null
      size_bytes: number
      change_number?: number | null
    },
  ): Promise<DocumentVersion> {
    const { data } = await apiClient.post<DocumentVersion>(
      `/documents/${documentId}/versions`,
      payload,
    )
    return data
  },

  async setCurrent(
    documentId: string,
    versionId: string,
  ): Promise<void> {
    await apiClient.patch(`/documents/${documentId}/versions/${versionId}/set-current`)
  },

  async delete(versionId: string): Promise<void> {
    await apiClient.delete(`/document-versions/${versionId}`)
  },
}
