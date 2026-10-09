import { apiClient } from "./client"

export interface ImportPreviewResponse {
  filename: string
  columns: string[]
  rows: Record<string, unknown>[]
  total_rows: number
  suggested_mapping: Record<string, string>
  header_row_index: number
  preview_rows_raw: unknown[][]
  sheet_name: string
}

export interface ImportConfirmResponse {
  log_id: string
  tasks_created: number
  errors: { row: number; message: string }[]
}

export interface ImportLog {
  id: string
  project_id: string
  filename: string | null
  rows_imported: number
  rows_failed: number
  status: string
  column_mapping: Record<string, string> | null
  error_details: Record<string, unknown> | null
  imported_at: string
}

export interface ColumnMappingPayload {
  task_title: string
  description?: string | null
  deadline?: string | null
  section?: string | null
  assignee?: string | null
}

export const importApi = {
    async preview(
    projectId: string,
    file: File,
    headerRow?: number,
  ): Promise<ImportPreviewResponse> {
    const formData = new FormData()
    formData.append("file", file)

    // Передаём params ТОЛЬКО если headerRow — валидное число
    const config =
      typeof headerRow === "number" && Number.isInteger(headerRow) && headerRow >= 0
        ? { params: { header_row: headerRow } }
        : {}

    const { data } = await apiClient.post<ImportPreviewResponse>(
      `/projects/${projectId}/import-excel`,
      formData,
      config,
    )
    return data
  },

  async confirm(
    projectId: string,
    file: File,
    columnMapping: ColumnMappingPayload,
    headerRow?: number,
  ): Promise<ImportConfirmResponse> {
    const formData = new FormData()
    formData.append("file", file)
    formData.append("payload", JSON.stringify({ column_mapping: columnMapping }))

    const config =
      typeof headerRow === "number" && Number.isInteger(headerRow) && headerRow >= 0
        ? { params: { header_row: headerRow } }
        : {}

    const { data } = await apiClient.post<ImportConfirmResponse>(
      `/projects/${projectId}/import-confirm`,
      formData,
      config,
    )
    return data
  },

  async getLogs(projectId: string): Promise<ImportLog[]> {
    const { data } = await apiClient.get<ImportLog[]>(
      `/projects/${projectId}/import-logs`,
    )
    return data
  },
}