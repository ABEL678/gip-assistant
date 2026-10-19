import { apiClient } from "./client"

// ====== Типы ======

export type GoalState = "plan" | "in_progress" | "achieved" | "cancelled"

export interface Goal {
  id: string
  project_id: string
  formulation: string
  deadline: string | null
  responsible_id: string | null
  priority: number | null
  state: GoalState
  verification_status: VerificationStatus
  created_by: string | null
  premise_ids: string[]
  created_at: string
  updated_at: string
}

export interface GoalCreate {
  formulation: string
  deadline?: string | null
  responsible_id?: string | null
  priority?: number | null
  state?: GoalState
  created_by?: string | null
  premise_ids?: string[]
  field_schema?: Record<string, unknown>
}

export interface GoalUpdate {
  formulation?: string
  deadline?: string | null
  responsible_id?: string | null
  priority?: number | null
  state?: GoalState
  created_by?: string | null
  premise_ids?: string[]
  field_schema?: Record<string, unknown>
}

export interface GoalProposal {
  id: string
  premise: {
    id: string
    project_id: string
    category: string
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
  formulation: string
  deadline: string | null
  priority: number | null
  premise_ids: string[]
  rule: string
  confidence: number
  created_at: string
}

export interface GoalProposalApprove {
  formulation: string
  deadline?: string | null
  priority?: number | null
  premise_ids: string[]
}

export type VerificationStatus = "confirmed" | "requires_check" | "no_data" | "not_confirmed"

export interface ValidationEvidence {
  premise_id: string
  field: string
  value: unknown
  owner: string
}

export interface ValidationResult {
  goal_id: string
  verification_status: VerificationStatus
  evidence: ValidationEvidence[]
  missing: string[]
  contradictions: string[]
}

export interface SimilarityLink {
  from_section: string
  to_section: string
  what: string
  risk: string
}

export interface SimilarityMatrixResponse {
  links: SimilarityLink[]
}

export interface ProtocolSummary {
  total: number
  unanimous: Record<string, VerificationStatus>
  majority: Record<string, VerificationStatus>
  split: string[]
}

// ====== API-клиент ======

export const goalApi = {
  async fetchGoals(projectId: string): Promise<Goal[]> {
    const { data } = await apiClient.get<Goal[]>(
      `/projects/${projectId}/goals`,
    )
    return data
  },

  async fetchGoal(goalId: string): Promise<Goal> {
    const { data } = await apiClient.get<Goal>(`/goals/${goalId}`)
    return data
  },

  async createGoal(
    projectId: string,
    payload: GoalCreate,
  ): Promise<Goal> {
    const { data } = await apiClient.post<Goal>(
      `/projects/${projectId}/goals`,
      payload,
    )
    return data
  },

  async updateGoal(goalId: string, payload: GoalUpdate): Promise<Goal> {
    const { data } = await apiClient.patch<Goal>(`/goals/${goalId}`, payload)
    return data
  },

  async deleteGoal(goalId: string): Promise<void> {
    await apiClient.delete(`/goals/${goalId}`)
  },

  async fetchGoalProposals(projectId: string): Promise<GoalProposal[]> {
    const { data } = await apiClient.get<GoalProposal[]>(
      `/projects/${projectId}/goals/proposals`,
    )
    return data
  },

  async approveGoalProposal(
    projectId: string,
    payload: GoalProposalApprove,
  ): Promise<Goal> {
    const { data } = await apiClient.post<Goal>(
      `/projects/${projectId}/goals/from-proposal`,
      payload,
    )
    return data
  },

  async validateGoal(goalId: string): Promise<ValidationResult> {
    const { data } = await apiClient.post<ValidationResult>(
      `/goals/${goalId}/validate`,
    )
    return data
  },

  async getSimilarityMatrix(
    projectId: string,
  ): Promise<SimilarityMatrixResponse> {
    const { data } = await apiClient.get<SimilarityMatrixResponse>(
      `/projects/${projectId}/goals/similarity-matrix`,
    )
    return data
  },

  async run3Times(projectId: string): Promise<ProtocolSummary> {
    const { data } = await apiClient.post<ProtocolSummary>(
      `/projects/${projectId}/goals/proposals/run-3-times`,
    )
    return data
  },
}
