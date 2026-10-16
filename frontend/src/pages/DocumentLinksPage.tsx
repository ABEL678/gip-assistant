import { useState } from "react"
import { useParams, Link } from "react-router-dom"
import { ArrowLeft, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { useDocument, useDocumentsByProject } from "@/hooks/useDocuments"
import { type DocumentLinkType } from "@/api/documentEnums"
import { useDocumentLinks, useIncomingDocumentLinks, useCreateDocumentLink, useDeleteDocumentLink } from "@/hooks/useDocumentLinks"
import { LinkCard } from "@/components/LinkCard"
import { LinkForm } from "@/components/LinkForm"

export function DocumentLinksPage() {
  const { id: projectId, docId } = useParams<{ id: string; docId: string }>()
  const [showForm, setShowForm] = useState(false)

  const { data: document, isLoading: docLoading, isError: docError, error: docErrorData } = useDocument(docId!)
  const { data: documents } = useDocumentsByProject(projectId!)
  const { data: outgoing, isLoading: outgoingLoading, isError: outgoingError, error: outgoingErrorData } = useDocumentLinks(docId!)
  const { data: incoming, isLoading: incomingLoading, isError: incomingError, error: incomingErrorData } = useIncomingDocumentLinks(docId!)
  const createMutation = useCreateDocumentLink(docId!)
  const deleteMutation = useDeleteDocumentLink(docId!)

  // Lookup map для имён документов
  const docMap = documents
    ? Object.fromEntries(documents.map((d) => [d.id, d]))
    : {}

  const handleDelete = (linkId: string) => {
    if (window.confirm("Удалить эту связь?")) {
      deleteMutation.mutate(linkId)
    }
  }

  const handleFormSubmit = (payload: {
    target_document_id: string
    link_type: DocumentLinkType
  }) => {
    createMutation.mutate(payload, {
      onSuccess: () => setShowForm(false),
    })
  }

  if (docLoading || outgoingLoading || incomingLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (docError || outgoingError || incomingError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Ошибка: {((docErrorData || outgoingErrorData || incomingErrorData) as Error).message}</AlertDescription>
      </Alert>
    )
  }

  // Сортировка по created_at DESC
  const sortedOutgoing = [...(outgoing || [])].sort((a, b) =>
    new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  )
  const sortedIncoming = [...(incoming || [])].sort((a, b) =>
    new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  )

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
            Связи: {document?.document_name}
          </h1>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" />
          Добавить связь
        </Button>
      </div>

      {/* LinkForm */}
      {showForm && (
        <LinkForm
          projectId={projectId!}
          currentDocumentId={docId!}
          onSubmit={handleFormSubmit}
          onCancel={() => setShowForm(false)}
          isPending={createMutation.isPending}
        />
      )}

      {/* Outgoing */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Исходящие связи</h2>
        {sortedOutgoing.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">
            Нет исходящих связей
          </div>
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sortedOutgoing.map((link) => (
            <LinkCard
              key={link.id}
              link={link}
              direction="outgoing"
              targetDocument={docMap[link.target_document_id]}
              onDelete={handleDelete}
            />
          ))}
        </div>
      </div>

      {/* Incoming */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Входящие связи</h2>
        {sortedIncoming.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">
            Нет входящих связей
          </div>
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sortedIncoming.map((link) => (
            <LinkCard
              key={link.id}
              link={link}
              direction="incoming"
              sourceDocument={docMap[link.source_document_id]}
              onDelete={handleDelete}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
