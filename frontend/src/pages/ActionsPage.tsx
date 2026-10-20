import { useState, useMemo } from "react"
import { useParams, Link, useSearchParams } from "react-router-dom"
import { ArrowLeft, Plus } from "lucide-react"
import { useQuery } from "@tanstack/react-query"
import { projectsApi } from "@/api/projectsApi"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { useActions, useCreateAction, useUpdateAction, useDeleteAction } from "@/hooks/useActions"
import { ActionCard } from "@/components/ActionCard"
import { ActionForm } from "@/components/ActionForm"
import { type ActionCreate, type ActionUpdate } from "@/api/actionApi"

export function ActionsPage() {
  const { id: projectId } = useParams<{ id: string }>()
  const [searchParams] = useSearchParams()
  const taskFilter = searchParams.get("task")

  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { data, isLoading, isError } = useActions(projectId!)
  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => projectsApi.getById(projectId!),
    enabled: !!projectId,
  })
  const createMutation = useCreateAction(projectId!)
  const updateMutation = useUpdateAction(projectId!)
  const deleteMutation = useDeleteAction(projectId!)

  // Filter by task_id if ?task=... is present
  const filteredData = useMemo(() => {
    if (!taskFilter || !data) return data
    return data.filter((a) => a.task_id === taskFilter)
  }, [data, taskFilter])

  const handleCreate = (data: ActionCreate | ActionUpdate) => {
    if (editingId) {
      updateMutation.mutate(
        { actionId: editingId, payload: data as ActionUpdate },
        {
          onError: (err: Error) => setError(err.message),
          onSuccess: () => {
            setEditingId(null)
            setShowForm(false)
          },
        },
      )
    } else {
      createMutation.mutate(data as ActionCreate, {
        onError: (err: Error) => setError(err.message),
        onSuccess: () => setShowForm(false),
      })
    }
  }

  const handleDelete = (id: string) => {
    if (window.confirm("Удалить это действие?")) {
      deleteMutation.mutate(id)
    }
  }

  if (isLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (isError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Ошибка загрузки</AlertDescription>
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
          <h1 className="text-2xl font-bold">
            Действия{project ? ` — ${project.name}` : ""}
          </h1>
          <p className="text-sm text-muted-foreground">
            Управление действиями проекта
          </p>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" /> Добавить действие
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Empty state */}
      {!isLoading && !isError && filteredData && filteredData.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          Пока нет действий
        </div>
      )}

      {/* Grid */}
      {!isLoading && !isError && filteredData && filteredData.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredData.map((action) => (
            <ActionCard
              key={action.id}
              action={action}
              onEdit={(a) => {
                setEditingId(a.id)
                setShowForm(true)
              }}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      {/* Form Modal */}
      <Dialog open={showForm} onOpenChange={(open) => {
        if (!open) {
          setShowForm(false)
          setEditingId(null)
        }
      }}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>
              {editingId ? "Редактировать действие" : "Добавить действие"}
            </DialogTitle>
          </DialogHeader>
          <ActionForm
            projectId={projectId!}
            initialData={editingId ? (filteredData?.find((a) => a.id === editingId)) as ActionUpdate : undefined}
            onSubmit={handleCreate}
            onCancel={() => {
              setShowForm(false)
              setEditingId(null)
            }}
            submitLabel="Сохранить"
          />
        </DialogContent>
      </Dialog>
    </div>
  )
}
