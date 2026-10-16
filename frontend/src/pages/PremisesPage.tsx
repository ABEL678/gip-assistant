import { useState } from "react"
import { useParams, Link } from "react-router-dom"
import { ArrowLeft, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { usePremises, useCreatePremise, useDeletePremise } from "@/hooks/usePremises"
import { PremiseCard } from "@/components/PremiseCard"
import { PremiseForm } from "@/components/PremiseForm"
import { type PremiseCreate, type PremiseUpdate } from "@/api/premiseApi"

export function PremisesPage() {
  const { id: projectId } = useParams<{ id: string }>()

  const [showForm, setShowForm] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const { data, isLoading, isError } = usePremises(projectId!)
  const createMutation = useCreatePremise(projectId!)
  const deleteMutation = useDeletePremise(projectId!)

  const handleCreate = (data: PremiseCreate | PremiseUpdate) => {
    createMutation.mutate(data as never, {
      onError: (err: Error) => setError(err.message),
      onSuccess: () => setShowForm(false),
    })
  }

  const handleDelete = (id: string) => {
    if (window.confirm("Удалить эту вводную?")) {
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
          <h1 className="text-2xl font-bold">Вводные</h1>
          <p className="text-sm text-muted-foreground">
            Управление вводными проекта
          </p>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" /> Добавить вводную
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
          Пока нет вводных
        </div>
      )}

      {/* Grid */}
      {!isLoading && !isError && data && data.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {data.map((premise) => (
            <PremiseCard
              key={premise.id}
              premise={premise}
              onEdit={() => setShowForm(true)}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      {/* Form Modal */}
      <Dialog open={showForm} onOpenChange={setShowForm}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>
              Добавить вводную
            </DialogTitle>
          </DialogHeader>
          <PremiseForm
            onSubmit={handleCreate}
            onCancel={() => setShowForm(false)}
            submitLabel="Сохранить"
          />
        </DialogContent>
      </Dialog>
    </div>
  )
}
