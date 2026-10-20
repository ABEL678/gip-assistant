import { apiClient } from "./client"

// ====== Типы ======

export interface Revision {
  id: string
  document_id: string
  version: number
  date: string | null
  source: string | null
  notified: boolean
  stop_flag: boolean
  created_at: string
  updated_at: string
}

export interface Change {
  id: string
  revision_id: string
  field: string
  old_value: string | null
  new_value: string | null
  status: "added" | "removed" | "changed" | "unchanged"
  created_at: string
}

export interface RevisionDecision {
  id: string
  change_id: string
  decision:
    | "accepted"
    | "accepted_with_frame"
    | "remark"
    | "rejected"
    | "moved"
    | "deadline"
  decided_by: string | null
  deadline: string | null
  created_at: string
}

export interface StopFlag {
  id: string
  revision_id: string
  reason: string
  resolved: boolean
  created_at: string
}

export interface RevisionCreate {
  version: number
  date?: string | null
  source?: string | null
  notified?: boolean
  stop_flag?: boolean
}

export interface ChangeCreate {
  field: string
  old_value?: string | null
  new_value?: string | null
  status: "added" | "removed" | "changed" | "unchanged"
}

export interface RevisionDecisionCreate {
  decision:
    | "accepted"
    | "accepted_with_frame"
    | "remark"
    | "rejected"
    | "moved"
    | "deadline"
  decided_by?: string | null
  deadline?: string | null
}

export interface StopFlagCreate {
  reason: string
  resolved?: boolean
}

// ====== API-клиент ======

export const revisionApi = {
  async listRevisions(documentId: string): Promise<Revision[]> {
    const { data } = await apiClient.get<Revision[]>(
      `/documents/${documentId}/revisions`,
    )
    return data
  },

  async getRevision(revisionId: string): Promise<Revision> {
    const { data } = await apiClient.get<Revision>(`/revisions/${revisionId}`)
    return data
  },

  async createRevision(
    documentId: string,
    payload: RevisionCreate,
  ): Promise<Revision> {
    const { data } = await apiClient.post<Revision>(
      `/documents/${documentId}/revisions`,
      payload,
    )
    return data
  },

  async deleteRevision(revisionId: string): Promise<void> {
    await apiClient.delete(`/revisions/${revisionId}`)
  },

  async listChanges(revisionId: string): Promise<Change[]> {
    const { data } = await apiClient.get<Change[]>(
      `/revisions/${revisionId}/changes`,
    )
    return data
  },

  async createChange(
    revisionId: string,
    payload: ChangeCreate,
  ): Promise<Change> {
    const { data } = await apiClient.post<Change>(
      `/revisions/${revisionId}/changes`,
      payload,
    )
    return data
  },

  async createDecision(
    changeId: string,
    payload: RevisionDecisionCreate,
  ): Promise<RevisionDecision> {
    const { data } = await apiClient.post<RevisionDecision>(
      `/changes/${changeId}/decision`,
      payload,
    )
    return data
  },

  async createStopFlag(
    revisionId: string,
    payload: StopFlagCreate,
  ): Promise<StopFlag> {
    const { data } = await apiClient.post<StopFlag>(
      `/revisions/${revisionId}/stop-flags`,
      payload,
    )
    return data
  },
}
