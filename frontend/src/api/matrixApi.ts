import { apiClient } from "./client"

export type CrossTaskStatus =
  | "NOT_STARTED"
  | "IN_PROGRESS"
  | "WAITING_INFO"
  | "DONE"
  | "OVERDUE"

export interface CrossTask {
  id: string
  project_id: string
  from_section_code: string
  to_section_code: string
  status: CrossTaskStatus
  description: string | null
  created_at: string
  updated_at: string
}

export interface CrossTaskTask {
  id: string
  project_id: string
  title: string
  description: string | null
  status: string
  assignee_id: string | null
  deadline: string | null
  section_code: string | null
  to_section_code: string | null
  sort_order: number
  source: string
  created_at: string
  updated_at: string
  overdue_days: number
  days_until_deadline: number | null
}

export const CROSS_TASK_STATUS_LABELS: Record<CrossTaskStatus, string> = {
  NOT_STARTED: "Не начато",
  IN_PROGRESS: "В работе",
  WAITING_INFO: "Ждёт информации",
  DONE: "Готово",
  OVERDUE: "Просрочено",
}

export const CROSS_TASK_STATUS_COLORS: Record<CrossTaskStatus, string> = {
  NOT_STARTED: "bg-gray-100 text-gray-800 border-gray-300",
  IN_PROGRESS: "bg-blue-100 text-blue-800 border-blue-300",
  WAITING_INFO: "bg-yellow-100 text-yellow-800 border-yellow-300",
  DONE: "bg-green-100 text-green-800 border-green-300",
  OVERDUE: "bg-red-100 text-red-800 border-red-300",
}

export const matrixApi = {
  async getMatrix(projectId: string): Promise<CrossTask[]> {
    const { data } = await apiClient.get<CrossTask[]>(`/projects/${projectId}/matrix`)
    return data
  },

  async generate(projectId: string): Promise<{ project_id: string; cross_tasks_created: number }> {
    const { data } = await apiClient.post<{ project_id: string; cross_tasks_created: number }>(
      `/projects/${projectId}/matrix/generate`,
    )
    return data
  },

  async updateCrossTask(
    crossTaskId: string,
    payload: { status?: CrossTaskStatus; description?: string | null },
  ): Promise<CrossTask> {
    const { data } = await apiClient.patch<CrossTask>(`/cross-tasks/${crossTaskId}`, payload)
    return data
  },

    async getCrossTaskTasks(crossTaskId: string): Promise<CrossTaskTask[]> {
    const { data } = await apiClient.get<CrossTaskTask[]>(
      `/cross-tasks/${crossTaskId}/tasks`,
    )
    return data
  },
}