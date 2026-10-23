import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  decisionApi,
  type DecisionCreate,
  type DecisionUpdate,
  type DecisionProposalApprove,
} from "@/api/decisionApi"

export function useDecisions(projectId: string) {
  return useQuery({
    queryKey: ["decisions", projectId],
    queryFn: () => decisionApi.fetchDecisions(projectId),
    enabled: !!projectId,
  })
}

export function useDecision(decisionId: string) {
  return useQuery({
    queryKey: ["decision", decisionId],
    queryFn: () => decisionApi.getDecision(decisionId),
    enabled: !!decisionId,
  })
}

export function useCreateDecision(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: DecisionCreate) =>
      decisionApi.createDecision(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["decisions", projectId] })
    },
  })
}

export function useUpdateDecision() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      decisionId,
      payload,
    }: {
      decisionId: string
      payload: DecisionUpdate
    }) => decisionApi.updateDecision(decisionId, payload),
    onSuccess: (_, { decisionId }) => {
      queryClient.invalidateQueries({ queryKey: ["decision", decisionId] })
    },
  })
}

export function useDeleteDecision(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (decisionId: string) => decisionApi.deleteDecision(decisionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["decisions", projectId] })
    },
  })
}

export function useDecisionProposals(projectId: string) {
  return useQuery({
    queryKey: ["decision-proposals", projectId],
    queryFn: () => decisionApi.fetchDecisionsProposals(projectId),
    enabled: !!projectId,
  })
}

export function useCreateDecisionFromProposal(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: DecisionProposalApprove) =>
      decisionApi.createFromProposal(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["decisions", projectId] })
      queryClient.invalidateQueries({ queryKey: ["decision-proposals", projectId] })
    },
  })
}
