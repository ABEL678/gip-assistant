import { useState } from "react"
import { useParams, Link } from "react-router-dom"
import { ArrowLeft, Plus } from "lucide-react"
import { useQuery } from "@tanstack/react-query"
import { projectsApi } from "@/api/projectsApi"
import { premiseApi } from "@/api/premiseApi"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { useCreateStandard, useUpdateStandard, useDeleteStandard } from "@/hooks/useProjectStandards"
import { ProjectStandardCard } from "@/components/ProjectStandardCard"
import { ProjectStandardForm } from "@/components/ProjectStandardForm"
import { type ProjectStandardCreate, type ProjectStandardUpdate } from "@/api/projectStandardApi"
import { projectStandardApi } from "@/api/projectStandardApi"

export function ProjectStandardsPage() {
  const { id: projectId } = useParams<{ id: string }>()

  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => projectsApi.getById(projectId!),
    enabled: !!projectId,
  })

  const { data: premises } = useQuery({
    queryKey: ["premises", projectId],
    queryFn: () => premiseApi.fetchPremises(projectId!),
    enabled: !!projectId,
  })

  // Fetch standards for all premises
  const { data: allStandards, isLoading, isError } = useQuery({
    queryKey: ["all-standards", projectId],
    queryFn: async () => {
      if (!premises) return []
      const all: Awaited<ReturnType<typeof projectStandardApi.fetchStandards>>[] =
        await Promise.all(premises.map((p) => projectStandardApi.fetchStandards(p.id)))
      return all.flat()
    },
    enabled: !!premises,
  })

  const createMutation = useCreateStandard(projectId!)
  const updateMutation = useUpdateStandard(projectId!)
  const deleteMutation = useDeleteStandard(projectId!)

  const handleCreate = (data: ProjectStandardCreate | ProjectStandardUpdate) => {
    if (editingId) {
      updateMutation.mutate(
        { standardId: editingId, payload: data as ProjectStandardUpdate },
        {
          onError: (err: Error) => setError(err.message),
          onSuccess: () => {
            setEditingId(null)
            setShowForm(false)
          },
        },
      )
    } else {
      // Use first premise if none specified
      const premise_id = (data as ProjectStandardCreate).premise_id ?? premises?.[0]?.id
      if (!premise_id) {
        setError("Нет доступных вводных для привязки стандарта")
        return
      }
      const createPayload: ProjectStandardCreate = {
        premise_id,
        type: (data as ProjectStandardCreate).type,
        value: (data as ProjectStandardCreate).value,
      }
      createMutation.mutate(createPayload, {
        onError: (err: Error) => setError(err.message),
        onSuccess: () => setShowForm(false),
      })
    }
  }

  const handleDelete = (id: string) => {
    if (window.confirm("Удалить этот стандарт?")) {
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
            Стандарты проекта{project ? ` — ${project.name}` : ""}
          </h1>
          <p className="text-sm text-muted-foreground">
            Управление стандартами проекта
          </p>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" /> Добавить стандарт
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Empty state */}
      {!isLoading && !isError && allStandards && allStandards.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          Пока нет стандартов
        </div>
      )}

      {/* Grid */}
      {!isLoading && !isError && allStandards && allStandards.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {allStandards.map((standard) => (
            <ProjectStandardCard
              key={standard.id}
              standard={standard}
              onEdit={(s) => {
                setEditingId(s.id)
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
              {editingId ? "Редактировать стандарт" : "Добавить стандарт"}
            </DialogTitle>
          </DialogHeader>
          <ProjectStandardForm
            initialData={editingId ? (allStandards?.find((s) => s.id === editingId)) as ProjectStandardUpdate : undefined}
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
