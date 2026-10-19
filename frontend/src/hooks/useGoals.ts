import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { goalApi, type GoalCreate, type GoalUpdate, type GoalProposalApprove } from "@/api/goalApi"

export function useGoals(projectId: string) {
  return useQuery({
    queryKey: ["goals", projectId],
    queryFn: () => goalApi.fetchGoals(projectId),
    enabled: !!projectId,
  })
}

export function useGoal(goalId: string) {
  return useQuery({
    queryKey: ["goal", goalId],
    queryFn: () => goalApi.fetchGoal(goalId),
    enabled: !!goalId,
  })
}

export function useCreateGoal(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: GoalCreate) => goalApi.createGoal(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["goals", projectId] })
    },
  })
}

export function useUpdateGoal(projectId?: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      goalId,
      payload,
    }: {
      goalId: string
      payload: GoalUpdate
    }) => goalApi.updateGoal(goalId, payload),
    onSuccess: (_, { goalId }) => {
      queryClient.invalidateQueries({ queryKey: ["goal", goalId] })
      if (projectId) {
        queryClient.invalidateQueries({ queryKey: ["canvas", projectId] })
      }
    },
  })
}

export function useDeleteGoal(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (goalId: string) => goalApi.deleteGoal(goalId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["goals", projectId] })
    },
  })
}

export function useGoalProposals(projectId: string) {
  return useQuery({
    queryKey: ["goal-proposals", projectId],
    queryFn: () => goalApi.fetchGoalProposals(projectId),
    enabled: !!projectId,
  })
}

export function useApproveProposal(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: GoalProposalApprove) =>
      goalApi.approveGoalProposal(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["goals", projectId] })
      queryClient.invalidateQueries({ queryKey: ["goal-proposals", projectId] })
      queryClient.invalidateQueries({ queryKey: ["canvas", projectId] })
    },
  })
}

export function useValidateGoal() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (goalId: string) => goalApi.validateGoal(goalId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["goals"] })
    },
  })
}

export function useSimilarityMatrix(projectId: string) {
  return useQuery({
    queryKey: ["similarity-matrix", projectId],
    queryFn: () => goalApi.getSimilarityMatrix(projectId),
    enabled: !!projectId,
  })
}

export function useRun3Times(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => goalApi.run3Times(projectId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["goals", projectId] })
      queryClient.invalidateQueries({ queryKey: ["goal-proposals", projectId] })
      queryClient.invalidateQueries({ queryKey: ["similarity-matrix", projectId] })
    },
  })
}
