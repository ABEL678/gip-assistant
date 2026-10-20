import { apiClient } from "./client"

// ====== Типы ======

export interface Action {
  id: string
  project_id: string
  formulation: string
  task_id: string | null
  measurable_result: string | null
  deadline: string | null
  state: ActionState
  created_at: string
  updated_at: string
}

export type ActionState = "plan" | "in_progress" | "done" | "overdue" | "cancelled"

export const ACTION_STATE_LABELS: Record<ActionState, string> = {
  plan: "План",
  in_progress: "В работе",
  done: "Готово",
  overdue: "Просрочено",
  cancelled: "Отменено",
}

export interface ActionCreate {
  formulation: string
  task_id?: string | null
  measurable_result?: string | null
  deadline?: string | null
  state?: ActionState
}

export interface ActionUpdate {
  formulation?: string
  task_id?: string | null
  measurable_result?: string | null
  deadline?: string | null
  state?: ActionState
}

// ====== API-клиент ======

export const actionApi = {
  async fetchActions(projectId: string): Promise<Action[]> {
    const { data } = await apiClient.get<Action[]>(
      `/projects/${projectId}/actions`,
    )
    return data
  },

  async fetchActionsByTask(taskId: string): Promise<Action[]> {
    const { data } = await apiClient.get<Action[]>(`/tasks/${taskId}/actions`)
    return data
  },

  async fetchAction(actionId: string): Promise<Action> {
    const { data } = await apiClient.get<Action>(`/actions/${actionId}`)
    return data
  },

  async createAction(
    projectId: string,
    payload: ActionCreate,
  ): Promise<Action> {
    const { data } = await apiClient.post<Action>(
      `/projects/${projectId}/actions`,
      payload,
    )
    return data
  },

  async updateAction(
    actionId: string,
    payload: ActionUpdate,
  ): Promise<Action> {
    const { data } = await apiClient.patch<Action>(
      `/actions/${actionId}`,
      payload,
    )
    return data
  },

  async deleteAction(actionId: string): Promise<void> {
    await apiClient.delete(`/actions/${actionId}`)
  },
}
