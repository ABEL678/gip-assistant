import { apiClient } from "./client"
import type { Premise } from "./premiseApi"
import type { Goal, GoalProposal } from "./goalApi"

export const canvasApi = {
  async fetchCanvas(projectId: string): Promise<{
    premises: Premise[]
    goals: Goal[]
    proposals: GoalProposal[]
  }> {
    const [premisesRes, goalsRes, proposalsRes] = await Promise.all([
      apiClient.get(`/projects/${projectId}/premises`),
      apiClient.get(`/projects/${projectId}/goals`),
      apiClient.get(`/projects/${projectId}/goals/proposals`),
    ])
    return {
      premises: premisesRes.data,
      goals: goalsRes.data,
      proposals: proposalsRes.data,
    }
  },
}
