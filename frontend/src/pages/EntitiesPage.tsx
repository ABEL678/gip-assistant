import { useParams, Link } from "react-router-dom"
import { ArrowLeft, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { useEntityType } from "@/hooks/useEntityTypes"
import { useEntities, useCreateEntity, useDeleteEntity } from "@/hooks/useEntities"
import { DynamicTable } from "@/components/DynamicTable"

export function EntitiesPage() {
  const { id: projectId, entityTypeId } = useParams<{ id: string; entityTypeId: string }>()

  const { data: entityType, isLoading: typeLoading, isError: typeError, error } = useEntityType(entityTypeId!)
  const { data: entities, isLoading: entitiesLoading } = useEntities(entityTypeId!)
  const createMutation = useCreateEntity(entityTypeId!)
  const deleteMutation = useDeleteEntity(entityTypeId!)

  const handleCreate = () => {
    createMutation.mutate({ project_id: projectId!, data: {}, sort_order: 0 })
  }

  if (typeLoading || entitiesLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (typeError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Ошибка: {(error as Error).message}</AlertDescription>
      </Alert>
    )
  }

  if (!entityType || !entities) {
    return null
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link to={`/projects/${projectId}/entity-types`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">{entityType.name}</h1>
          <p className="text-sm text-muted-foreground">{entities.length} записей</p>
        </div>
        <Button onClick={handleCreate}>
          <Plus className="h-4 w-4 mr-2" />
          Добавить запись
        </Button>
      </div>

      <DynamicTable
        fields={entityType.schema.fields}
        entities={entities}
        onDelete={(id) => {
          if (window.confirm("Удалить запись?")) {
            deleteMutation.mutate(id)
          }
        }}
      />
    </div>
  )
}
