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
  useRfis,
  useRfiProposals,
  useCreateRfi,
  useUpdateRfi,
  useDeleteRfi,
  useEscalateRfi,
  useCreateRfiFromProposal,
} from "@/hooks/useRfis"
import { useDecisions } from "@/hooks/useDecisions"
import { useGoals } from "@/hooks/useGoals"
import { usePremises } from "@/hooks/usePremises"
import { RfiCard } from "@/components/RfiCard"
import { RfiForm } from "@/components/RfiForm"
import { RfiProposalList } from "@/components/RfiProposalList"
import {
  type Rfi,
  type RfiProposal,
  type RfiProposalApprove,
  type RfiUpdate,
  proposalKey,
} from "@/api/rfiApi"

export function RfiPage() {
  const { id: projectId } = useParams<{ id: string }>()

  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [handledProposals, setHandledProposals] = useState<Set<string>>(new Set())

  const {
    data: rfis,
    isLoading: rfisLoading,
    isError: rfisError,
  } = useRfis(projectId!)
  const {
    data: proposals,
    isLoading: proposalsLoading,
    isError: proposalsError,
    refetch: refetchProposals,
  } = useRfiProposals(projectId!)
  const { data: decisions } = useDecisions(projectId!)
  const { data: goals } = useGoals(projectId!)
  const { data: premises } = usePremises(projectId!)
  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => projectsApi.getById(projectId!),
    enabled: !!projectId,
  })

  const createMutation = useCreateRfi(projectId!)
  const updateMutation = useUpdateRfi(projectId!)
  const deleteMutation = useDeleteRfi(projectId!)
  const escalateMutation = useEscalateRfi(projectId!)
  const createFromProposalMutation = useCreateRfiFromProposal(projectId!)

  const decisionLabels = new Map((decisions ?? []).map((d) => [d.id, d.formulation]))
  const goalLabels = new Map((goals ?? []).map((g) => [g.id, g.formulation]))
  const premiseNames = new Map((premises ?? []).map((p) => [p.id, p.name]))

  const getCauseLabel = (rfi: Rfi): string | null => {
    if (rfi.rfi_cause_decision_id) {
      return decisionLabels.get(rfi.rfi_cause_decision_id) ?? null
    }
    if (rfi.rfi_cause_goal_id) {
      return goalLabels.get(rfi.rfi_cause_goal_id) ?? null
    }
    return null
  }

  const getPremiseLabels = (rfi: Rfi): string[] =>
    rfi.premise_ids.map((premiseId) => premiseNames.get(premiseId) ?? "—")

  const causeOptions = {
    decisions: (decisions ?? []).map((d) => ({ id: d.id, label: d.formulation })),
    goals: (goals ?? []).map((g) => ({ id: g.id, label: g.formulation })),
  }

  const visibleProposals = (proposals ?? []).filter(
    (proposal) => !handledProposals.has(proposalKey(proposal)),
  )

  const approving =
    createFromProposalMutation.isPending || escalateMutation.isPending

  const editingRfi = editingId
    ? (rfis?.find((rfi) => rfi.id === editingId) ?? null)
    : null

  const handleSubmit = (payload: RfiUpdate) => {
    if (editingId) {
      setError(null)
      updateMutation.mutate(
        { rfiId: editingId, payload },
        {
          onError: (err: Error) => setError(`Не удалось изменить RFI: ${err.message}`),
          onSuccess: () => {
            setError(null)
            setEditingId(null)
            setShowForm(false)
          },
        },
      )
      return
    }

    const { title, ...rest } = payload
    if (!title) return
    setError(null)
    createMutation.mutate(
      { title, ...rest },
      {
        onError: (err: Error) => setError(`Не удалось создать RFI: ${err.message}`),
        onSuccess: () => {
          setError(null)
          setShowForm(false)
        },
      },
    )
  }

  const handleDelete = (rfiId: string) => {
    if (!window.confirm("Удалить этот RFI?")) return
    setError(null)
    deleteMutation.mutate(rfiId, {
      onError: (err: Error) => setError(`Не удалось удалить RFI: ${err.message}`),
      onSuccess: () => setError(null),
    })
  }

  const handleCreateFromProposal = (proposal: RfiProposal) => {
    if (!proposal.reason_decision_id || !proposal.rfi_due_date) return
    const payload: RfiProposalApprove = {
      formulation: proposal.formulation,
      rationale: proposal.rationale,
      rfi_cause_decision_id: proposal.reason_decision_id,
      rfi_due_date: proposal.rfi_due_date,
      rfi_state: "open",
    }
    setError(null)
    createFromProposalMutation.mutate(payload, {
      onError: (err: Error) =>
        setError(`Не удалось создать RFI из предложения: ${err.message}`),
      onSuccess: () => {
        setError(null)
        setHandledProposals((prev) => new Set(prev).add(proposalKey(proposal)))
      },
    })
  }

  const handleEscalate = (proposal: RfiProposal) => {
    if (!proposal.existing_rfi_id) return
    setError(null)
    escalateMutation.mutate(proposal.existing_rfi_id, {
      onError: (err: Error) => setError(`Не удалось эскалировать RFI: ${err.message}`),
      onSuccess: () => {
        setError(null)
        setHandledProposals((prev) => new Set(prev).add(proposalKey(proposal)))
      },
    })
  }

  const handleRefreshProposals = () => {
    setHandledProposals(new Set())
    refetchProposals()
  }

  if (rfisLoading || proposalsLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (rfisError || proposalsError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Ошибка загрузки RFI</AlertDescription>
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
            RFI{project ? ` — ${project.name}` : ""}
          </h1>
          <p className="text-sm text-muted-foreground">
            Запросы информации по проекту
          </p>
        </div>
        <Button
          onClick={() => {
            setEditingId(null)
            setShowForm(true)
          }}
        >
          <Plus className="h-4 w-4 mr-2" /> Добавить RFI
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Proposed RFIs */}
      <div className="border rounded-lg p-4">
        <RfiProposalList
          proposals={visibleProposals}
          onCreateFromProposal={handleCreateFromProposal}
          onEscalate={handleEscalate}
          onRefresh={handleRefreshProposals}
          approving={approving}
        />
      </div>

      {/* Empty state */}
      {!rfisLoading && !rfisError && rfis && rfis.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          Пока нет RFI
          <div className="mt-4">
            <Button
              onClick={() => {
                setEditingId(null)
                setShowForm(true)
              }}
            >
              <Plus className="h-4 w-4 mr-2" /> Добавить RFI
            </Button>
          </div>
        </div>
      )}

      {/* Grid */}
      {!rfisLoading && !rfisError && rfis && rfis.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {rfis.map((rfi) => (
            <RfiCard
              key={rfi.id}
              rfi={rfi}
              causeLabel={getCauseLabel(rfi)}
              premiseLabels={getPremiseLabels(rfi)}
              onEdit={(item) => {
                setEditingId(item.id)
                setShowForm(true)
              }}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      {/* Form Modal */}
      <Dialog
        open={showForm}
        onOpenChange={(open) => {
          if (!open) {
            setShowForm(false)
            setEditingId(null)
          }
        }}
      >
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>
              {editingId ? "Редактировать RFI" : "Добавить RFI"}
            </DialogTitle>
          </DialogHeader>
          <RfiForm
            initialData={editingRfi}
            causeOptions={causeOptions}
            onSubmit={handleSubmit}
            onCancel={() => {
              setShowForm(false)
              setEditingId(null)
            }}
            submitting={createMutation.isPending || updateMutation.isPending}
          />
        </DialogContent>
      </Dialog>
    </div>
  )
}
