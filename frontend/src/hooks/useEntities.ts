import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { entityApi, type Entity } from "@/api/entityApi"

export function useEntities(entityTypeId: string) {
  return useQuery({
    queryKey: ["entities", entityTypeId],
    queryFn: () => entityApi.getEntitiesByType(entityTypeId),
    enabled: !!entityTypeId,
  })
}

export function useEntity(entityId: string) {
  return useQuery({
    queryKey: ["entity", entityId],
    queryFn: () => entityApi.getEntity(entityId),
    enabled: !!entityId,
  })
}

export function useCreateEntity(entityTypeId: string, projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: {
      project_id: string
      data?: Record<string, unknown>
      sort_order?: number
    }) => entityApi.createEntity(entityTypeId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entities", entityTypeId] })
    },
  })
}

export function useUpdateEntity(entityTypeId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      entityId,
      payload,
    }: {
      entityId: string
      payload: Partial<Pick<Entity, "data" | "sort_order">>
    }) => entityApi.updateEntity(entityId, payload),
    onSuccess: (_, { entityId }) => {
      queryClient.invalidateQueries({ queryKey: ["entities", entityTypeId] })
      queryClient.invalidateQueries({ queryKey: ["entity", entityId] })
    },
  })
}

export function useDeleteEntity(entityTypeId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (entityId: string) => entityApi.deleteEntity(entityId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entities", entityTypeId] })
    },
  })
}
