import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  projectStandardApi,
  type ProjectStandardCreate,
  type ProjectStandardUpdate,
} from "@/api/projectStandardApi"

export function useProjectStandards(premiseId: string) {
  return useQuery({
    queryKey: ["standards", premiseId],
    queryFn: () => projectStandardApi.fetchStandards(premiseId),
    enabled: !!premiseId,
  })
}

export function useProjectStandard(standardId: string) {
  return useQuery({
    queryKey: ["standard", standardId],
    queryFn: () => projectStandardApi.fetchStandard(standardId),
    enabled: !!standardId,
  })
}

export function useCreateStandard(premiseId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ProjectStandardCreate) =>
      projectStandardApi.createStandard(premiseId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["standards", premiseId] })
    },
  })
}

export function useUpdateStandard(premiseId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      standardId,
      payload,
    }: {
      standardId: string
      payload: ProjectStandardUpdate
    }) => projectStandardApi.updateStandard(standardId, payload),
    onSuccess: (_, { standardId }) => {
      queryClient.invalidateQueries({ queryKey: ["standard", standardId] })
      queryClient.invalidateQueries({ queryKey: ["standards", premiseId] })
    },
  })
}

export function useDeleteStandard(premiseId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (standardId: string) => projectStandardApi.deleteStandard(standardId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["standards", premiseId] })
    },
  })
}
