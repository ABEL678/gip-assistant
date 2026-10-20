import { useState } from "react"
import { useParams, Link } from "react-router-dom"
import { ArrowLeft, Plus } from "lucide-react"
import { useQuery } from "@tanstack/react-query"
import { documentsApi } from "@/api/documentsApi"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { useRevisions, useCreateRevision, useDeleteRevision } from "@/hooks/useRevisions"
import { RevisionCard } from "@/components/RevisionCard"
import { RevisionForm } from "@/components/RevisionForm"
import { type RevisionCreate } from "@/api/revisionApi"

export function RevisionsPage() {
  const { id: projectId, docId } = useParams<{ id: string; docId: string }>()

  const [showForm, setShowForm] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const { data: revisions, isLoading, isError } = useRevisions(docId!)
  const { data: document } = useQuery({
    queryKey: ["document", docId],
    queryFn: () => documentsApi.getById(docId!),
    enabled: !!docId,
  })
  const createMutation = useCreateRevision(docId!)
  const deleteMutation = useDeleteRevision(docId!)

  const handleCreate = (data: RevisionCreate) => {
    createMutation.mutate(data, {
      onError: (err: Error) => setError(err.message),
      onSuccess: () => setShowForm(false),
    })
  }

  const handleDelete = (id: string) => {
    if (window.confirm("Удалить эту ревизию?")) {
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
        <Link to={`/projects/${projectId}/documents`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">
            Ревизии{document ? ` — ${document.document_name}` : ""}
          </h1>
          <p className="text-sm text-muted-foreground">
            Управление ревизиями документа
          </p>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" /> Добавить ревизию
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Empty state */}
      {!isLoading && !isError && revisions && revisions.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          Пока нет ревизий
        </div>
      )}

      {/* Grid */}
      {!isLoading && !isError && revisions && revisions.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {revisions.map((revision) => (
            <RevisionCard
              key={revision.id}
              revision={revision}
              onOpen={(rev) => {
                window.location.href = `/projects/${projectId}/documents/${docId}/revisions/${rev.id}`
              }}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      {/* Form Modal */}
      <Dialog open={showForm} onOpenChange={(open) => {
        if (!open) setShowForm(false)
      }}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Добавить ревизию</DialogTitle>
          </DialogHeader>
          <RevisionForm
            onSubmit={handleCreate}
            onCancel={() => setShowForm(false)}
            isPending={createMutation.isPending}
          />
        </DialogContent>
      </Dialog>
    </div>
  )
}
