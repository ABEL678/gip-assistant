import { apiClient } from "./client"

export interface Project {
  id: string
  name: string
  code: string
  stage: string
  client: string | null
  contract_number: string | null
  created_at: string
  updated_at: string
}

export const projectsApi = {
  async getAll(): Promise<Project[]> {
    const { data } = await apiClient.get<Project[]>("/projects")
    return data
  },

  async getById(id: string): Promise<Project> {
    const { data } = await apiClient.get<Project>(`/projects/${id}`)
    return data
  },
}