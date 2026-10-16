import { apiClient } from "./client"
import { type LifecycleStatus } from "./documentEnums"

// ====== Типы ======

export interface Document {
  id: string
  guid: string
  project_id: string
  entity_id: string | null
  task_id: string | null
  cipher: string
  document_name: string
  document_kind: "ПД" | "РД"
  doc_part_type: "ТЧ" | "ГЧ" | null
  section_code: string | null
  mark: string | null
  base_designation: string | null
  document_type_id: string
  current_version_id: string | null
  version_parent_id: string | null
  replaces_id: string | null
  replaced_by_id: string | null
  lifecycle_status: LifecycleStatus
  signed_by: string | null
  signed_at: string | null
  signature_hash: string | null
  signature_status: string | null
  created_by: string | null
  created_at: string
  updated_at: string
}

// ====== API-клиент ======

export const documentsApi = {
  // ---------- Document ----------

  async getByProject(
    projectId: string,
    lifecycleStatus?: LifecycleStatus,
  ): Promise<Document[]> {
    const params = lifecycleStatus ? { lifecycle_status: lifecycleStatus } : undefined
    const { data } = await apiClient.get<Document[]>(
      `/projects/${projectId}/documents`,
      { params },
    )
    return data
  },

  async getById(id: string): Promise<Document> {
    const { data } = await apiClient.get<Document>(`/documents/${id}`)
    return data
  },

  async getByGuid(guid: string): Promise<Document> {
    const { data } = await apiClient.get<Document>(`/documents/by-guid/${guid}`)
    return data
  },

  async create(
    projectId: string,
    payload: {
      document_type_id: string
      document_name: string
      cipher: string
      document_kind?: "ПД" | "РД"
      doc_part_type?: "ТЧ" | "ГЧ" | null
      section_code?: string | null
      mark?: string | null
      base_designation?: string | null
      entity_id?: string | null
      task_id?: string | null
      lifecycle_status?: LifecycleStatus
      version_parent_id?: string | null
      replaces_id?: string | null
      replaced_by_id?: string | null
    },
  ): Promise<Document> {
    const { data } = await apiClient.post<Document>(
      `/projects/${projectId}/documents`,
      payload,
    )
    return data
  },

  async update(
    id: string,
    payload: Partial<
      Pick<
        Document,
        | "document_name"
        | "document_kind"
        | "doc_part_type"
        | "section_code"
        | "mark"
        | "base_designation"
        | "lifecycle_status"
      >
    >,
  ): Promise<Document> {
    const { data } = await apiClient.patch<Document>(`/documents/${id}`, payload)
    return data
  },

  async delete(id: string): Promise<void> {
    await apiClient.delete(`/documents/${id}`)
  },
}
