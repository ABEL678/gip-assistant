import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  decisionLinkApi,
  type DecisionLinkCreate,
} from "@/api/decisionLinkApi"

export function useDecisionLinks(projectId: string) {
  return useQuery({
    queryKey: ["decision-links", projectId],
    queryFn: () => decisionLinkApi.fetchDecisionLinks(projectId),
    enabled: !!projectId,
  })
}

export function useDecisionLink(linkId: string) {
  return useQuery({
    queryKey: ["decision-link", linkId],
    queryFn: () => decisionLinkApi.getDecisionLink(linkId),
    enabled: !!linkId,
  })
}

export function useCreateDecisionLink(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: DecisionLinkCreate) =>
      decisionLinkApi.createDecisionLink(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["decision-links", projectId] })
    },
  })
}

export function useDeleteDecisionLink(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (linkId: string) => decisionLinkApi.deleteDecisionLink(linkId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["decision-links", projectId] })
    },
  })
}

export function useDecisionLinksByDecision(decisionId: string) {
  return useQuery({
    queryKey: ["decision-links-by-decision", decisionId],
    queryFn: () => decisionLinkApi.fetchLinksByDecision(decisionId),
    enabled: !!decisionId,
  })
}
