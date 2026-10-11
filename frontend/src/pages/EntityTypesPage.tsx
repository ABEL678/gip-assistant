import { useParams, Link, useNavigate } from "react-router-dom"
import { ArrowLeft, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { useEntityTypes, useDeleteEntityType } from "@/hooks/useEntityTypes"
import { EntityTypeCard } from "@/components/EntityTypeCard"

export function EntityTypesPage() {
  const { id: projectId } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const { data, isLoading, isError, error } = useEntityTypes(projectId!)
  const deleteMutation = useDeleteEntityType(projectId!)

  const handleDelete = (id: string) => {
    if (window.confirm("Удалить этот тип сущности?")) {
      deleteMutation.mutate(id)
    }
  }

  if (isLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (isError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Ошибка: {(error as Error).message}</AlertDescription>
      </Alert>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link to={`/projects/${projectId}`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">Типы сущностей</h1>
          <p className="text-sm text-muted-foreground">
            Управление типами сущностей проекта
          </p>
        </div>
        <Button
          onClick={() => navigate(`/projects/${projectId}/entity-types/new`)}
        >
          <Plus className="h-4 w-4 mr-2" />
          Создать тип
        </Button>
      </div>

      {/* Empty state */}
      {!isLoading && !isError && data && data.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          Пока нет типов
        </div>
      )}

      {/* Grid */}
      {!isLoading && !isError && data && data.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.map((type) => (
            <EntityTypeCard
              key={type.id}
              entityType={type}
              onEdit={(id) =>
                navigate(`/projects/${projectId}/entity-types/${id}/edit`)
              }
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  )
}
