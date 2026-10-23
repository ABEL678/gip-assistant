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
import {
  useNorms,
  useCreateNorm,
  useUpdateNorm,
  useDeleteNorm,
} from "@/hooks/useNorms"
import { NormCard } from "@/components/NormCard"
import { NormForm } from "@/components/NormForm"
import { type NormCreate, type NormUpdate } from "@/api/normApi"

export function NormsPage() {
  const { id: projectId } = useParams<{ id: string }>()

  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { data: norms, isLoading: normsLoading, isError: normsError } = useNorms(projectId!)
  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => projectsApi.getById(projectId!),
    enabled: !!projectId,
  })
  const createMutation = useCreateNorm(projectId!)
  const updateMutation = useUpdateNorm()
  const deleteMutation = useDeleteNorm(projectId!)

  const handleCreate = (data: NormCreate | NormUpdate) => {
    if (editingId) {
      updateMutation.mutate(
        { normId: editingId, payload: data as NormUpdate },
        {
          onError: (err: Error) => setError(err.message),
          onSuccess: () => {
            setEditingId(null)
            setShowForm(false)
          },
        },
      )
    } else {
      createMutation.mutate(data as NormCreate, {
        onError: (err: Error) => setError(err.message),
        onSuccess: () => setShowForm(false),
      })
    }
  }

  const handleDelete = (id: string) => {
    if (window.confirm("Удалить эту норму?")) {
      deleteMutation.mutate(id)
    }
  }

  if (normsLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (normsError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Ошибка загрузки норм</AlertDescription>
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
            Нормы{project ? ` — ${project.name}` : ""}
          </h1>
          <p className="text-sm text-muted-foreground">
            Управление нормативными документами проекта
          </p>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" /> Добавить норму
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Empty state */}
      {!normsLoading && !normsError && norms && norms.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          Пока нет норм
        </div>
      )}

      {/* Grid */}
      {!normsLoading && !normsError && norms && norms.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {norms.map((norm) => (
            <NormCard
              key={norm.id}
              norm={norm}
              onEdit={(n) => {
                setEditingId(n.id)
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
              {editingId ? "Редактировать норму" : "Добавить норму"}
            </DialogTitle>
          </DialogHeader>
          <NormForm
            projectId={projectId!}
            initialData={editingId ? (norms?.find((n) => n.id === editingId)) as NormUpdate : undefined}
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
