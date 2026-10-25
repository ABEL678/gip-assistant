import { type TaskStatus } from "./tasksApi"
import { apiClient } from "./client"

// ====== Типы ======

export type RfiState =
  | "open"
  | "sent"
  | "answered"
  | "registered"
  | "closed"
  | "escalated"

export const RFI_STATE_LABELS: Record<RfiState, string> = {
  open: "Открыт",
  sent: "Отправлен",
  answered: "Отвечен",
  registered: "Зарегистрирован",
  closed: "Закрыт",
  escalated: "Эскалирован",
}

export const RFI_STATE_COLORS: Record<RfiState, string> = {
  open: "bg-gray-100 text-gray-800",
  sent: "bg-blue-100 text-blue-800",
  answered: "bg-indigo-100 text-indigo-800",
  registered: "bg-green-100 text-green-800",
  closed: "bg-zinc-200 text-zinc-800",
  escalated: "bg-red-100 text-red-800",
}

export interface Rfi {
  id: string
  project_id: string
  title: string
  rfi_cause_decision_id: string | null
  rfi_cause_goal_id: string | null
  rfi_due_date: string | null
  rfi_state: RfiState
  deadline: string | null
  assignee_id: string | null
  is_complex: boolean
  status: TaskStatus
  sort_order: number
  source: string
  created_at: string | null
  updated_at: string | null
  premise_ids: string[]
}

export interface RfiCreate {
  title: string
  rfi_cause_decision_id?: string | null
  rfi_cause_goal_id?: string | null
  rfi_due_date?: string | null
  rfi_state?: RfiState
  // ниже — поля контракта, формой 6.12d не отправляются:
  deadline?: string | null
  assignee_id?: string | null
  is_complex?: boolean
}

export type RfiUpdate = Partial<RfiCreate>

export type RfiProposalAction = "create" | "escalate"

export interface RfiProposal {
  id: string | null // DTO nullable; сервис заполняет uuid5 всегда
  action: RfiProposalAction
  rule: string
  formulation: string
  rationale: string | null
  reason_decision_id: string | null
  existing_rfi_id: string | null
  rfi_due_date: string | null
}

export function proposalKey(p: RfiProposal): string {
  return `${p.id ?? "no-id"}:${p.reason_decision_id ?? p.existing_rfi_id ?? ""}`
}

/**
 * Форматирует дату из ISO-вида `YYYY-MM-DD` в `DD.MM.YYYY`.
 * Разбор по частям вместо `new Date(...)`: строка без времени парсится
 * как UTC и в поясах западнее UTC даёт сдвиг на день.
 */
export function formatIsoDate(value: string | null): string {
  if (!value) return "—"
  const [year, month, day] = value.split("-")
  if (!year || !month || !day) return value
  return `${day}.${month}.${year}`
}

export interface RfiProposalApprove {
  formulation: string
  rationale?: string | null
  rfi_cause_decision_id: string
  rfi_due_date: string
  rfi_state?: RfiState
}

// ====== API-клиент ======

export const rfiApi = {
  async fetchRfis(projectId: string): Promise<Rfi[]> {
    const { data } = await apiClient.get<Rfi[]>(`/projects/${projectId}/rfis`)
    return data
  },

  async fetchRfiProposals(projectId: string): Promise<RfiProposal[]> {
    const { data } = await apiClient.get<RfiProposal[]>(
      `/projects/${projectId}/rfis/proposals`,
    )
    return data
  },

  async createRfi(projectId: string, payload: RfiCreate): Promise<Rfi> {
    const { data } = await apiClient.post<Rfi>(
      `/projects/${projectId}/rfis`,
      payload,
    )
    return data
  },

  async getRfi(rfiId: string): Promise<Rfi> {
    const { data } = await apiClient.get<Rfi>(`/rfis/${rfiId}`)
    return data
  },

  async updateRfi(rfiId: string, payload: RfiUpdate): Promise<Rfi> {
    const { data } = await apiClient.patch<Rfi>(`/rfis/${rfiId}`, payload)
    return data
  },

  async deleteRfi(rfiId: string): Promise<void> {
    await apiClient.delete(`/rfis/${rfiId}`)
  },

  async createFromProposal(
    projectId: string,
    payload: RfiProposalApprove,
  ): Promise<Rfi> {
    const { data } = await apiClient.post<Rfi>(
      `/projects/${projectId}/rfis/from-proposal`,
      payload,
    )
    return data
  },

  async escalateRfi(rfiId: string): Promise<Rfi> {
    const { data } = await apiClient.post<Rfi>(`/rfis/${rfiId}/escalate`)
    return data
  },
}
