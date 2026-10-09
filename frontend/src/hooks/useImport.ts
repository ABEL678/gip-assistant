import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { importApi, type ColumnMappingPayload } from "@/api/importApi"

export function useImportPreview() {
  return useMutation({
    mutationFn: ({
      projectId,
      file,
      headerRow,
    }: {
      projectId: string
      file: File
      headerRow?: number
    }) => importApi.preview(projectId, file, headerRow),
  })
}

export function useImportConfirm() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      projectId,
      file,
      columnMapping,
      headerRow,
    }: {
      projectId: string
      file: File
      columnMapping: ColumnMappingPayload
      headerRow?: number
    }) => importApi.confirm(projectId, file, columnMapping, headerRow),
    onSuccess: (_, variables) => {
      // Обновляем список задач проекта после импорта
      queryClient.invalidateQueries({ queryKey: ["tasks", variables.projectId] })
      queryClient.invalidateQueries({ queryKey: ["import-logs", variables.projectId] })
    },
  })
}

export function useImportLogs(projectId: string) {
  return useQuery({
    queryKey: ["import-logs", projectId],
    queryFn: () => importApi.getLogs(projectId),
    enabled: !!projectId,
  })
}