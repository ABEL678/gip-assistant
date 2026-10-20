import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  actionApi,
  type ActionCreate,
  type ActionUpdate,
} from "@/api/actionApi"

export function useActions(projectId: string) {
  return useQuery({
    queryKey: ["actions", projectId],
    queryFn: () => actionApi.fetchActions(projectId),
    enabled: !!projectId,
  })
}

export function useAction(actionId: string) {
  return useQuery({
    queryKey: ["action", actionId],
    queryFn: () => actionApi.fetchAction(actionId),
    enabled: !!actionId,
  })
}

export function useActionsByTask(taskId: string) {
  return useQuery({
    queryKey: ["actions-by-task", taskId],
    queryFn: () => actionApi.fetchActionsByTask(taskId),
    enabled: !!taskId,
  })
}

export function useCreateAction(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ActionCreate) =>
      actionApi.createAction(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["actions", projectId] })
    },
  })
}

export function useUpdateAction(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      actionId,
      payload,
    }: {
      actionId: string
      payload: ActionUpdate
    }) => actionApi.updateAction(actionId, payload),
    onSuccess: (_, { actionId }) => {
      queryClient.invalidateQueries({ queryKey: ["action", actionId] })
      queryClient.invalidateQueries({ queryKey: ["actions", projectId] })
    },
  })
}

export function useDeleteAction(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (actionId: string) => actionApi.deleteAction(actionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["actions", projectId] })
    },
  })
}
