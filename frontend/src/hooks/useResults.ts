import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  resultApi,
  type ResultCreate,
  type ResultUpdate,
} from "@/api/resultApi"

export function useResults(projectId: string) {
  return useQuery({
    queryKey: ["results", projectId],
    queryFn: () => resultApi.fetchResults(projectId),
    enabled: !!projectId,
  })
}

export function useResult(resultId: string) {
  return useQuery({
    queryKey: ["result", resultId],
    queryFn: () => resultApi.fetchResult(resultId),
    enabled: !!resultId,
  })
}

export function useCreateResult(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ResultCreate) =>
      resultApi.createResult(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["results", projectId] })
    },
  })
}

export function useUpdateResult(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      resultId,
      payload,
    }: {
      resultId: string
      payload: ResultUpdate
    }) => resultApi.updateResult(resultId, payload),
    onSuccess: (_, { resultId }) => {
      queryClient.invalidateQueries({ queryKey: ["result", resultId] })
      queryClient.invalidateQueries({ queryKey: ["results", projectId] })
    },
  })
}

export function useDeleteResult(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (resultId: string) => resultApi.deleteResult(resultId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["results", projectId] })
    },
  })
}
