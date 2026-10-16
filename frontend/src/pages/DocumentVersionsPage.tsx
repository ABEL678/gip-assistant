import { useState } from "react"
import { useParams, Link } from "react-router-dom"
import { ArrowLeft, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { useDocument } from "@/hooks/useDocuments"
import { useDocumentVersions, useCreateDocumentVersion, useSetCurrentDocumentVersion, useDeleteDocumentVersion } from "@/hooks/useDocumentVersions"
import { VersionCard } from "@/components/VersionCard"
import { VersionForm } from "@/components/VersionForm"

export function DocumentVersionsPage() {
  const { id: projectId, docId } = useParams<{ id: string; docId: string }>()
  const [showForm, setShowForm] = useState(false)

  const { data: document, isLoading: docLoading, isError: docError, error: docErrorData } = useDocument(docId!)
  const { data: versions, isLoading: versionsLoading, isError: versionsError, error: versionsErrorData } = useDocumentVersions(docId!)
  const createMutation = useCreateDocumentVersion(docId!)
  const setCurrentMutation = useSetCurrentDocumentVersion(docId!)
  const deleteMutation = useDeleteDocumentVersion(docId!)

  const handleSetCurrent = (versionId: string) => {
    if (window.confirm("Сделать эту версию текущей?")) {
      setCurrentMutation.mutate(versionId)
    }
  }

  const handleDelete = (versionId: string) => {
    if (window.confirm("Удалить эту версию?")) {
      deleteMutation.mutate(versionId)
    }
  }

  const handleFormSubmit = (payload: {
    version: string
    file_path: string
    file_name: string
    hash_sha256: string
    format_original: string
    format_archive: string | null
    size_bytes: number
    change_number: number | null
  }) => {
    createMutation.mutate(payload, {
      onSuccess: () => setShowForm(false),
    })
  }

  if (docLoading || versionsLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (docError || versionsError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Ошибка: {((docErrorData || versionsErrorData) as Error).message}</AlertDescription>
      </Alert>
    )
  }

  const sortedVersions = [...(versions || [])].sort((a, b) => {
    if (a.is_current) return -1
    if (b.is_current) return 1
    return new Date(b.uploaded_at).getTime() - new Date(a.uploaded_at).getTime()
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link to={`/projects/${projectId}/documents/${docId}/edit`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">
            Версии: {document?.document_name}
          </h1>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" />
          Добавить версию
        </Button>
      </div>

      {/* VersionForm */}
      {showForm && (
        <VersionForm
          onSubmit={handleFormSubmit}
          onCancel={() => setShowForm(false)}
          isPending={createMutation.isPending}
        />
      )}

      {/* Empty state */}
      {!showForm && sortedVersions.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          Пока нет версий
          <div className="mt-4">
            <Button onClick={() => setShowForm(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Добавить первую версию
            </Button>
          </div>
        </div>
      )}

      {/* List */}
      {sortedVersions.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sortedVersions.map((v) => (
            <VersionCard
              key={v.id}
              version={v}
              isCurrent={v.is_current}
              onSetCurrent={handleSetCurrent}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  )
}
