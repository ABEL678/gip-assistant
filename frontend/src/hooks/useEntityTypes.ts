import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { entityApi, type EntityType } from "@/api/entityApi"

export function useEntityTypes(projectId: string) {
  return useQuery({
    queryKey: ["entity-types", projectId],
    queryFn: () => entityApi.getTypesByProject(projectId),
    enabled: !!projectId,
  })
}

export function useEntityType(entityTypeId: string) {
  return useQuery({
    queryKey: ["entity-type", entityTypeId],
    queryFn: () => entityApi.getType(entityTypeId),
    enabled: !!entityTypeId,
  })
}

export function useCreateEntityType(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: {
      name: string
      icon?: string
      color?: string
      description?: string | null
      schema: { fields: Record<string, unknown>[] }
      sort_order?: number
    }) => entityApi.createType(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entity-types", projectId] })
    },
  })
}

export function useUpdateEntityType(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      entityTypeId,
      payload,
    }: {
      entityTypeId: string
      payload: Partial<
        Pick<EntityType, "name" | "icon" | "color" | "description" | "schema" | "sort_order">
      >
    }) => entityApi.updateType(entityTypeId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entity-types", projectId] })
    },
  })
}

export function useDeleteEntityType(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (entityTypeId: string) => entityApi.deleteType(entityTypeId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entity-types", projectId] })
    },
  })
}
