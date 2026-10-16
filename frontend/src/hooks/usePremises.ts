import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { premiseApi, type PremiseCreate, type PremiseUpdate } from "@/api/premiseApi"

export function usePremises(projectId: string) {
  return useQuery({
    queryKey: ["premises", projectId],
    queryFn: () => premiseApi.fetchPremises(projectId),
    enabled: !!projectId,
  })
}

export function usePremise(premiseId: string) {
  return useQuery({
    queryKey: ["premise", premiseId],
    queryFn: () => premiseApi.fetchPremise(premiseId),
    enabled: !!premiseId,
  })
}

export function useCreatePremise(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: PremiseCreate) =>
      premiseApi.createPremise(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["premises", projectId] })
      queryClient.invalidateQueries({ queryKey: ["goal-proposals", projectId] })
    },
  })
}

export function useUpdatePremise() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      premiseId,
      payload,
    }: {
      premiseId: string
      payload: PremiseUpdate
    }) => premiseApi.updatePremise(premiseId, payload),
    onSuccess: (_, { premiseId }) => {
      queryClient.invalidateQueries({ queryKey: ["premise", premiseId] })
    },
  })
}

export function useDeletePremise(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (premiseId: string) => premiseApi.deletePremise(premiseId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["premises", projectId] })
      queryClient.invalidateQueries({ queryKey: ["goal-proposals", projectId] })
    },
  })
}
