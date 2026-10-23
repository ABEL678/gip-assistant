import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  normApi,
  type NormCreate,
  type NormUpdate,
} from "@/api/normApi"

export function useNorms(projectId: string) {
  return useQuery({
    queryKey: ["norms", projectId],
    queryFn: () => normApi.fetchNorms(projectId),
    enabled: !!projectId,
  })
}

export function useNorm(normId: string) {
  return useQuery({
    queryKey: ["norm", normId],
    queryFn: () => normApi.getNorm(normId),
    enabled: !!normId,
  })
}

export function useCreateNorm(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: NormCreate) =>
      normApi.createNorm(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["norms", projectId] })
    },
  })
}

export function useUpdateNorm() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      normId,
      payload,
    }: {
      normId: string
      payload: NormUpdate
    }) => normApi.updateNorm(normId, payload),
    onSuccess: (_, { normId }) => {
      queryClient.invalidateQueries({ queryKey: ["norm", normId] })
    },
  })
}

export function useDeleteNorm(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (normId: string) => normApi.deleteNorm(normId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["norms", projectId] })
    },
  })
}
