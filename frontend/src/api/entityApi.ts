import { apiClient } from "./client"

// ====== Типы ======

export interface FieldDefinition {
  key: string
  label: string
  type: string
  required?: boolean
  options?: string[]
  default?: unknown
  description?: string
}

export interface EntityTypeSchema {
  fields: FieldDefinition[]
}

export interface EntityType {
  id: string
  project_id: string
  name: string
  icon: string
  color: string
  description: string | null
  schema: EntityTypeSchema
  sort_order: number
  is_system: boolean
  created_at: string
  updated_at: string
}

export interface Entity {
  id: string
  project_id: string
  entity_type_id: string
  data: Record<string, unknown>
  sort_order: number
  created_at: string
  updated_at: string
}

// ====== API-клиент ======

export const entityApi = {
  // ---------- EntityType ----------

  async getTypesByProject(projectId: string): Promise<EntityType[]> {
    const { data } = await apiClient.get<EntityType[]>(
      `/projects/${projectId}/entity-types`,
    )
    return data
  },

  async getType(entityTypeId: string): Promise<EntityType> {
    const { data } = await apiClient.get<EntityType>(`/entity-types/${entityTypeId}`)
    return data
  },

  async createType(
    projectId: string,
    payload: {
      name: string
      icon?: string
      color?: string
      description?: string | null
      schema: EntityTypeSchema
      sort_order?: number
    },
  ): Promise<EntityType> {
    const { data } = await apiClient.post<EntityType>(
      `/projects/${projectId}/entity-types`,
      payload,
    )
    return data
  },

  async updateType(
    entityTypeId: string,
    payload: Partial<
      Pick<EntityType, "name" | "icon" | "color" | "description" | "schema" | "sort_order">
    >,
  ): Promise<EntityType> {
    const { data } = await apiClient.patch<EntityType>(
      `/entity-types/${entityTypeId}`,
      payload,
    )
    return data
  },

  async deleteType(entityTypeId: string): Promise<void> {
    await apiClient.delete(`/entity-types/${entityTypeId}`)
  },

  // ---------- Entity ----------

  async getEntitiesByType(entityTypeId: string): Promise<Entity[]> {
    const { data } = await apiClient.get<Entity[]>(
      `/entity-types/${entityTypeId}/entities`,
    )
    return data
  },

  async getEntity(entityId: string): Promise<Entity> {
    const { data } = await apiClient.get<Entity>(`/entities/${entityId}`)
    return data
  },

  async createEntity(
    entityTypeId: string,
    payload: {
      project_id: string
      data?: Record<string, unknown>
      sort_order?: number
    },
  ): Promise<Entity> {
    const { data } = await apiClient.post<Entity>(
      `/entity-types/${entityTypeId}/entities`,
      payload,
    )
    return data
  },

  async updateEntity(
    entityId: string,
    payload: Partial<Pick<Entity, "data" | "sort_order">>,
  ): Promise<Entity> {
    const { data } = await apiClient.patch<Entity>(
      `/entities/${entityId}`,
      payload,
    )
    return data
  },

  async deleteEntity(entityId: string): Promise<void> {
    await apiClient.delete(`/entities/${entityId}`)
  },
}
