import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  rfiApi,
  type RfiCreate,
  type RfiProposalApprove,
  type RfiUpdate,
} from "@/api/rfiApi"

export function useRfis(projectId: string) {
  return useQuery({
    queryKey: ["rfis", projectId],
    queryFn: () => rfiApi.fetchRfis(projectId),
    enabled: !!projectId,
  })
}

export function useRfi(rfiId: string) {
  return useQuery({
    queryKey: ["rfi", rfiId],
    queryFn: () => rfiApi.getRfi(rfiId),
    enabled: !!rfiId,
  })
}

export function useRfiProposals(projectId: string) {
  return useQuery({
    queryKey: ["rfi-proposals", projectId],
    queryFn: () => rfiApi.fetchRfiProposals(projectId),
    enabled: !!projectId,
  })
}

export function useCreateRfi(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: RfiCreate) => rfiApi.createRfi(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["rfis", projectId] })
      queryClient.invalidateQueries({ queryKey: ["rfi-proposals", projectId] })
    },
  })
}

export function useUpdateRfi(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      rfiId,
      payload,
    }: {
      rfiId: string
      payload: RfiUpdate
    }) => rfiApi.updateRfi(rfiId, payload),
    onSuccess: (_, { rfiId }) => {
      queryClient.invalidateQueries({ queryKey: ["rfis", projectId] })
      queryClient.invalidateQueries({ queryKey: ["rfi", rfiId] })
    },
  })
}

export function useDeleteRfi(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (rfiId: string) => rfiApi.deleteRfi(rfiId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["rfis", projectId] })
      queryClient.invalidateQueries({ queryKey: ["rfi-proposals", projectId] })
    },
  })
}

export function useEscalateRfi(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (rfiId: string) => rfiApi.escalateRfi(rfiId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["rfis", projectId] })
      queryClient.invalidateQueries({ queryKey: ["rfi-proposals", projectId] })
    },
  })
}

export function useCreateRfiFromProposal(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: RfiProposalApprove) =>
      rfiApi.createFromProposal(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["rfis", projectId] })
      queryClient.invalidateQueries({ queryKey: ["rfi-proposals", projectId] })
    },
  })
}
