import { useState } from "react"
import { useParams, Link } from "react-router-dom"
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
import { useResults, useCreateResult, useUpdateResult, useDeleteResult } from "@/hooks/useResults"
import { ResultCard } from "@/components/ResultCard"
import { ResultForm } from "@/components/ResultForm"
import { type ResultCreate, type ResultUpdate } from "@/api/resultApi"

export function ResultsPage() {
  const { id: projectId } = useParams<{ id: string }>()

  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { data, isLoading, isError } = useResults(projectId!)
  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => projectsApi.getById(projectId!),
    enabled: !!projectId,
  })
  const createMutation = useCreateResult(projectId!)
  const updateMutation = useUpdateResult(projectId!)
  const deleteMutation = useDeleteResult(projectId!)

  const handleCreate = (data: ResultCreate | ResultUpdate) => {
    if (editingId) {
      updateMutation.mutate(
        { resultId: editingId, payload: data as ResultUpdate },
        {
          onError: (err: Error) => setError(err.message),
          onSuccess: () => {
            setEditingId(null)
            setShowForm(false)
          },
        },
      )
    } else {
      createMutation.mutate(data as ResultCreate, {
        onError: (err: Error) => setError(err.message),
        onSuccess: () => setShowForm(false),
      })
    }
  }

  const handleDelete = (id: string) => {
    if (window.confirm("Удалить этот результат?")) {
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
            Результаты{project ? ` — ${project.name}` : ""}
          </h1>
          <p className="text-sm text-muted-foreground">
            Управление результатами проекта
          </p>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" /> Добавить результат
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Empty state */}
      {!isLoading && !isError && data && data.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          Пока нет результатов
        </div>
      )}

      {/* Grid */}
      {!isLoading && !isError && data && data.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.map((result) => (
            <ResultCard
              key={result.id}
              result={result}
              onEdit={(r) => {
                setEditingId(r.id)
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
              {editingId ? "Редактировать результат" : "Добавить результат"}
            </DialogTitle>
          </DialogHeader>
          <ResultForm
            initialData={editingId ? (data?.find((r) => r.id === editingId)) as ResultUpdate : undefined}
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
