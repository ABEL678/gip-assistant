import { useState } from "react"
import { useParams, Link } from "react-router-dom"
import { ArrowLeft } from "lucide-react"
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
import { useRevision, useChanges, useCreateDecision } from "@/hooks/useRevisions"
import { RevisionCard } from "@/components/RevisionCard"
import { RevisionDiffView } from "@/components/RevisionDiffView"
import { RevisionDecisionForm } from "@/components/RevisionDecisionForm"
import { StopFlagList } from "@/components/StopFlagList"
import { type Change, type RevisionDecisionCreate, type StopFlagCreate, revisionApi } from "@/api/revisionApi"

export function RevisionDiffPage() {
  const { id: projectId, docId, revisionId } = useParams<{
    id: string
    docId: string
    revisionId: string
  }>()

  const [showDecisionForm, setShowDecisionForm] = useState(false)
  const [selectedChange, setSelectedChange] = useState<Change | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { data: revision, isLoading: isLoadingRevision, isError: isErrorRevision } = useRevision(revisionId!)
  const { data: changes, isLoading: isLoadingChanges, isError: isErrorChanges } = useChanges(revisionId!)
  const { data: document } = useQuery({
    queryKey: ["document", docId],
    queryFn: () => documentsApi.getById(docId!),
    enabled: !!docId,
  })
  const createDecisionMutation = useCreateDecision()

  const handleDecideChange = (change: Change) => {
    setSelectedChange(change)
    setShowDecisionForm(true)
  }

  const handleDecisionSubmit = (payload: RevisionDecisionCreate) => {
    if (!selectedChange) return
    createDecisionMutation.mutate(
      { changeId: selectedChange.id, payload },
      {
        onError: (err: Error) => setError(err.message),
        onSuccess: () => {
          setShowDecisionForm(false)
          setSelectedChange(null)
        },
      },
    )
  }

  const handleStopFlag = (payload: StopFlagCreate) => {
    revisionApi.createStopFlag(revisionId!, payload).catch((err: Error) => {
      setError(err.message)
    })
  }

  if (isLoadingRevision || isLoadingChanges) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (isErrorRevision || isErrorChanges) {
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
        <Link to={`/projects/${projectId}/documents/${docId}/revisions`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">
            Ревизия v{revision?.version}{document ? ` — ${document.document_name}` : ""}
          </h1>
          <p className="text-sm text-muted-foreground">
            Просмотр изменений
          </p>
        </div>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Revision info */}
      {revision && (
        <RevisionCard
          revision={revision}
          onOpen={() => {}}
          onDelete={() => {}}
        />
      )}

      {/* Changes table */}
      {changes && (
        <RevisionDiffView
          changes={changes}
          isLoading={false}
          onDecideChange={handleDecideChange}
        />
      )}

      {/* Stop flags */}
      <StopFlagList
        onStopFlag={handleStopFlag}
        isPending={false}
      />

      {/* Decision Modal */}
      <Dialog open={showDecisionForm} onOpenChange={(open) => {
        if (!open) {
          setShowDecisionForm(false)
          setSelectedChange(null)
        }
      }}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Принять решение по изменению</DialogTitle>
          </DialogHeader>
          {selectedChange && (
            <RevisionDecisionForm
              change={selectedChange}
              onSubmit={handleDecisionSubmit}
              onCancel={() => {
                setShowDecisionForm(false)
                setSelectedChange(null)
              }}
              isPending={createDecisionMutation.isPending}
            />
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}
