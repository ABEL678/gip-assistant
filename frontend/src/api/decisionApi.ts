import { apiClient } from "./client"

// ====== Типы ======

export type DecisionState = "plan" | "in_progress" | "accepted" | "cancelled" | "replaced"

export const DECISION_STATE_LABELS: Record<DecisionState, string> = {
  plan: "План",
  in_progress: "В работе",
  accepted: "Принято",
  cancelled: "Отменено",
  replaced: "Заменено",
}

export interface Decision {
  id: string
  project_id: string
  formulation: string
  rationale: string | null
  context: string | null
  deadline: string | null
  state: DecisionState
  premise_ids: string[]
  goal_ids: string[]
  created_by: string | null
  created_at: string | null
  updated_at: string | null
}

export interface DecisionCreate {
  formulation: string
  rationale?: string | null
  context?: string | null
  deadline?: string | null
  state?: DecisionState
  premise_ids?: string[]
  goal_ids?: string[]
}

export interface DecisionUpdate {
  formulation?: string
  rationale?: string | null
  context?: string | null
  deadline?: string | null
  state?: DecisionState
  premise_ids?: string[] | null
  goal_ids?: string[] | null
}

export interface DecisionProposal {
  id: string
  formulation: string
  rationale: string | null
  state: DecisionState
  premise_ids: string[]
  goal_ids: string[]
  rule: string
}

export interface DecisionProposalApprove {
  formulation: string
  rationale?: string | null
  premise_ids?: string[]
  goal_ids?: string[]
}

// ====== API-клиент ======

export const decisionApi = {
  async fetchDecisions(projectId: string): Promise<Decision[]> {
    const { data } = await apiClient.get<Decision[]>(
      `/projects/${projectId}/decisions`,
    )
    return data
  },

  async fetchDecisionsProposals(projectId: string): Promise<DecisionProposal[]> {
    const { data } = await apiClient.get<DecisionProposal[]>(
      `/projects/${projectId}/decisions/proposals`,
    )
    return data
  },

  async createDecision(
    projectId: string,
    payload: DecisionCreate,
  ): Promise<Decision> {
    const { data } = await apiClient.post<Decision>(
      `/projects/${projectId}/decisions`,
      payload,
    )
    return data
  },

  async getDecision(decisionId: string): Promise<Decision> {
    const { data } = await apiClient.get<Decision>(`/decisions/${decisionId}`)
    return data
  },

  async updateDecision(
    decisionId: string,
    payload: DecisionUpdate,
  ): Promise<Decision> {
    const { data } = await apiClient.patch<Decision>(
      `/decisions/${decisionId}`,
      payload,
    )
    return data
  },

  async deleteDecision(decisionId: string): Promise<void> {
    await apiClient.delete(`/decisions/${decisionId}`)
  },

  async createFromProposal(
    projectId: string,
    payload: DecisionProposalApprove,
  ): Promise<Decision> {
    const { data } = await apiClient.post<Decision>(
      `/projects/${projectId}/decisions/from-proposal`,
      payload,
    )
    return data
  },
}
