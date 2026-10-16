import { apiClient } from "./client"
import { type DocumentLinkType } from "./documentEnums"

export type { DocumentLinkType }

// ====== Типы ======

export interface DocumentLink {
  id: string
  source_document_id: string
  target_document_id: string
  link_type: DocumentLinkType
  created_at: string
}

// ====== API-клиент ======

export const documentLinksApi = {
  // ---------- DocumentLink ----------

  async listOutgoing(documentId: string): Promise<DocumentLink[]> {
    const { data } = await apiClient.get<DocumentLink[]>(
      `/documents/${documentId}/links`,
    )
    return data
  },

  async listIncoming(documentId: string): Promise<DocumentLink[]> {
    const { data } = await apiClient.get<DocumentLink[]>(
      `/documents/${documentId}/links/incoming`,
    )
    return data
  },

  async create(
    documentId: string,
    payload: {
      target_document_id: string
      link_type: DocumentLinkType
    },
  ): Promise<DocumentLink> {
    const { data } = await apiClient.post<DocumentLink>(
      `/documents/${documentId}/links`,
      payload,
    )
    return data
  },

  async delete(linkId: string): Promise<void> {
    await apiClient.delete(`/document-links/${linkId}`)
  },
}
