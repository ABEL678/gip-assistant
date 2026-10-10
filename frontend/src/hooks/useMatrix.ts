import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { matrixApi, type CrossTask, type CrossTaskStatus } from "@/api/matrixApi"

export function useMatrix(projectId: string) {
  return useQuery({
    queryKey: ["matrix", projectId],
    queryFn: () => matrixApi.getMatrix(projectId),
    enabled: !!projectId,
  })
}

export function useGenerateMatrix(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: () => matrixApi.generate(projectId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["matrix", projectId] })
    },
  })
}

export function useUpdateCrossTask(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      crossTaskId,
      payload,
    }: {
      crossTaskId: string
      payload: { status?: CrossTaskStatus; description?: string | null }
    }) => matrixApi.updateCrossTask(crossTaskId, payload),
    onSuccess: (updatedCrossTask) => {
      queryClient.setQueryData<CrossTask[]>(["matrix", projectId], (old) => {
        if (!old) return old
        return old.map((ct) => (ct.id === updatedCrossTask.id ? updatedCrossTask : ct))
      })
      queryClient.invalidateQueries({ queryKey: ["matrix", projectId] })
    },
  })
}

export function useCrossTaskTasks(crossTaskId: string | null) {
  return useQuery({
    queryKey: ["cross-task-tasks", crossTaskId],
    queryFn: () => matrixApi.getCrossTaskTasks(crossTaskId!),
    enabled: !!crossTaskId,
  })
}