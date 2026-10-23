import { apiClient } from "./client"

// ====== Типы ======

export type DecisionLinkType = "sequential" | "parallel" | "nested"

export const DECISION_LINK_TYPE_LABELS: Record<DecisionLinkType, string> = {
  sequential: "Последовательная",
  parallel: "Параллельная",
  nested: "Вложенная",
}

export interface DecisionLink {
  id: string
  project_id: string
  from_decision_id: string
  to_decision_id: string
  link_type: DecisionLinkType
  created_at: string | null
}

export interface DecisionLinkCreate {
  from_decision_id: string
  to_decision_id: string
  link_type: DecisionLinkType
}

// ====== API-клиент ======

export const decisionLinkApi = {
  async fetchDecisionLinks(projectId: string): Promise<DecisionLink[]> {
    const { data } = await apiClient.get<DecisionLink[]>(
      `/projects/${projectId}/decision-links`,
    )
    return data
  },

  async createDecisionLink(
    projectId: string,
    payload: DecisionLinkCreate,
  ): Promise<DecisionLink> {
    const { data } = await apiClient.post<DecisionLink>(
      `/projects/${projectId}/decision-links`,
      payload,
    )
    return data
  },

  async getDecisionLink(linkId: string): Promise<DecisionLink> {
    const { data } = await apiClient.get<DecisionLink>(`/decision-links/${linkId}`)
    return data
  },

  async deleteDecisionLink(linkId: string): Promise<void> {
    await apiClient.delete(`/decision-links/${linkId}`)
  },

  async fetchLinksByDecision(decisionId: string): Promise<DecisionLink[]> {
    const { data } = await apiClient.get<DecisionLink[]>(
      `/decisions/${decisionId}/links`,
    )
    return data
  },
}
