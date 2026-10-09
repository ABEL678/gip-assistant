import { apiClient } from "./client"

export type TaskStatus =
  | "NOT_STARTED"
  | "IN_PROGRESS"
  | "REVIEW"
  | "REWORK"
  | "DONE"
  | "CANCELLED"

export interface Task {
  id: string
  project_id: string
  title: string
  description: string | null
  status: TaskStatus
  assignee_id: string | null
  deadline: string | null
  section_code: string | null
  sort_order: number
  source: string
  created_at: string
  updated_at: string
}

export const TASK_STATUS_LABELS: Record<TaskStatus, string> = {
  NOT_STARTED: "Не начата",
  IN_PROGRESS: "В работе",
  REVIEW: "На проверке",
  REWORK: "Доработка",
  DONE: "Готово",
  CANCELLED: "Отменена",
}

export const TASK_STATUS_COLORS: Record<TaskStatus, string> = {
  NOT_STARTED: "bg-gray-100 text-gray-800",
  IN_PROGRESS: "bg-blue-100 text-blue-800",
  REVIEW: "bg-yellow-100 text-yellow-800",
  REWORK: "bg-orange-100 text-orange-800",
  DONE: "bg-green-100 text-green-800",
  CANCELLED: "bg-red-100 text-red-800",
}

export const tasksApi = {
  async getByProject(
    projectId: string,
    params?: { limit?: number; offset?: number },
  ): Promise<Task[]> {
    const { data } = await apiClient.get<Task[]>(`/projects/${projectId}/tasks`, {
      params,
    })
    return data
  },

  async update(
    taskId: string,
    payload: Partial<Pick<Task, "title" | "description" | "status" | "deadline" | "section_code">>,
  ): Promise<Task> {
    const { data } = await apiClient.patch<Task>(`/tasks/${taskId}`, payload)
    return data
  },

  async getById(taskId: string): Promise<Task> {
    const { data } = await apiClient.get<Task>(`/tasks/${taskId}`)
    return data
  },
}