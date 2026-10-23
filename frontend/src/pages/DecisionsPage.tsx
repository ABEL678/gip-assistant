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
  useDecisions,
  useDecisionProposals,
  useCreateDecision,
  useUpdateDecision,
  useDeleteDecision,
  useCreateDecisionFromProposal,
} from "@/hooks/useDecisions"
import { DecisionCard } from "@/components/DecisionCard"
import { DecisionForm } from "@/components/DecisionForm"
import { DecisionProposalList } from "@/components/DecisionProposalList"
import { type DecisionProposalApprove, type DecisionCreate, type DecisionUpdate } from "@/api/decisionApi"

export function DecisionsPage() {
  const { id: projectId } = useParams<{ id: string }>()

  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { data: decisions, isLoading: decisionsLoading, isError: decisionsError } = useDecisions(projectId!)
  const { data: proposals, isLoading: proposalsLoading, refetch } = useDecisionProposals(projectId!)
  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => projectsApi.getById(projectId!),
    enabled: !!projectId,
  })
  const createMutation = useCreateDecision(projectId!)
  const updateMutation = useUpdateDecision()
  const deleteMutation = useDeleteDecision(projectId!)
  const createFromProposalMutation = useCreateDecisionFromProposal(projectId!)

  const handleCreate = (data: DecisionCreate | DecisionUpdate) => {
    if (editingId) {
      updateMutation.mutate(
        { decisionId: editingId, payload: data as DecisionUpdate },
        {
          onError: (err: Error) => setError(err.message),
          onSuccess: () => {
            setEditingId(null)
            setShowForm(false)
          },
        },
      )
    } else {
      createMutation.mutate(data as DecisionCreate, {
        onError: (err: Error) => setError(err.message),
        onSuccess: () => setShowForm(false),
      })
    }
  }

  const handleDelete = (id: string) => {
    if (window.confirm("Удалить это решение?")) {
      deleteMutation.mutate(id)
    }
  }

  const handleApprove = (data: DecisionProposalApprove) => {
    createFromProposalMutation.mutate(data, {
      onError: (err: Error) => setError(err.message),
      onSuccess: () => refetch(),
    })
  }

  const handleReject = (_proposalId: string) => {
    // Remove from local list only (not saved)
  }

  const handleEditProposal = (proposal: { id: string }) => {
    setEditingId(proposal.id)
    setShowForm(true)
  }

  if (decisionsLoading || proposalsLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (decisionsError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Ошибка загрузки решений</AlertDescription>
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
            Решения{project ? ` — ${project.name}` : ""}
          </h1>
          <p className="text-sm text-muted-foreground">
            Управление решениями проекта
          </p>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" /> Добавить решение
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Proposed Decisions */}
      <div className="border rounded-lg p-4">
        <DecisionProposalList
          proposals={proposals ?? []}
          onApprove={handleApprove}
          onReject={handleReject}
          onEdit={handleEditProposal}
          onRefresh={() => refetch()}
        />
      </div>

      {/* Empty state */}
      {!decisionsLoading && !decisionsError && decisions && decisions.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          Пока нет решений
        </div>
      )}

      {/* Grid */}
      {!decisionsLoading && !decisionsError && decisions && decisions.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {decisions.map((decision) => (
            <DecisionCard
              key={decision.id}
              decision={decision}
              onEdit={(d) => {
                setEditingId(d.id)
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
              {editingId ? "Редактировать решение" : "Добавить решение"}
            </DialogTitle>
          </DialogHeader>
          <DecisionForm
            projectId={projectId!}
            initialData={editingId ? (decisions?.find((d) => d.id === editingId)) as DecisionUpdate : undefined}
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
