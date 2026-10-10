import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { tasksApi, type Task } from "@/api/tasksApi"

export function useTasks(projectId: string) {
  return useQuery({
    queryKey: ["tasks", projectId],
    queryFn: () => tasksApi.getByProject(projectId, { limit: 1000, offset: 0 }),
    enabled: !!projectId,
  })
}

export function useUpdateTask(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      taskId,
      payload,
    }: {
      taskId: string
      payload: Partial<Pick<Task, "title" | "description" | "status" | "deadline" | "section_code">>
    }) => tasksApi.update(taskId, payload),
    onSuccess: () => {
      // Кэш задач проекта (TaskList)
      queryClient.invalidateQueries({ queryKey: ["tasks", projectId] })
      // Кэш задач пары (страница «МЕХ → АР(КЖ)»)
      queryClient.invalidateQueries({ queryKey: ["cross-task-tasks"] })
      // Кэш матрицы (цвет ячейки может измениться)
      queryClient.invalidateQueries({ queryKey: ["matrix", projectId] })
    },
  })
}