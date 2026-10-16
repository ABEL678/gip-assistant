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
  useGoals,
  useGoalProposals,
  useCreateGoal,
  useDeleteGoal,
  useApproveProposal,
} from "@/hooks/useGoals"
import { usePremises } from "@/hooks/usePremises"
import { GoalCard } from "@/components/GoalCard"
import { GoalForm } from "@/components/GoalForm"
import { GoalProposalList } from "@/components/GoalProposalList"
import { type GoalProposalApprove, type GoalProposal } from "@/api/goalApi"
import { type GoalCreate, type GoalUpdate } from "@/api/goalApi"
import { goalApi } from "@/api/goalApi"

export function GoalsPage() {
  const { id: projectId } = useParams<{ id: string }>()

  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { data: goals, isLoading: goalsLoading, isError: goalsError } = useGoals(projectId!)
  const { data: proposals, isLoading: proposalsLoading, refetch } = useGoalProposals(projectId!)
  const { data: allPremises } = usePremises(projectId!)
  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => projectsApi.getById(projectId!),
    enabled: !!projectId,
  })
  const createMutation = useCreateGoal(projectId!)
  const deleteMutation = useDeleteGoal(projectId!)
  const approveMutation = useApproveProposal(projectId!)

  // Build premise name map from all project premises
  const premiseNameMap = new Map<string, string>()
  allPremises?.forEach((p) => {
    premiseNameMap.set(p.id, p.name)
  })

  const handleCreate = (data: GoalCreate | GoalUpdate) => {
    if (editingId) {
      // Update existing goal
      goalApi.updateGoal(editingId, data as GoalUpdate).then(() => {
        setEditingId(null)
        setShowForm(false)
      }).catch((err: Error) => setError(err.message))
    } else {
      createMutation.mutate(data as never, {
        onError: (err: Error) => setError(err.message),
        onSuccess: () => setShowForm(false),
      })
    }
  }

  const handleDelete = (id: string) => {
    if (window.confirm("Удалить эту цель?")) {
      deleteMutation.mutate(id)
    }
  }

  const handleApprove = (data: GoalProposalApprove) => {
    approveMutation.mutate(data as never, {
      onError: (err: Error) => setError(err.message),
    })
  }

  const handleReject = (_premiseId: string) => {
    // Remove from local list only (not saved)
  }

  const handleEditProposal = (proposal: GoalProposal) => {
    setEditingId(proposal.premise.id)
    setShowForm(true)
  }

  if (goalsLoading || proposalsLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (goalsError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Ошибка загрузки целей</AlertDescription>
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
            Цели{project ? ` — ${project.name}` : ""}
          </h1>
          <p className="text-sm text-muted-foreground">
            Управление целями проекта
          </p>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" /> Добавить цель
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Proposed Goals */}
      <div className="border rounded-lg p-4">
        <GoalProposalList
          proposals={proposals ?? []}
          premiseNames={premiseNameMap}
          onApprove={handleApprove}
          onReject={handleReject}
          onEdit={handleEditProposal}
          onRefresh={() => refetch()}
        />
      </div>

      {/* Empty state */}
      {!goalsLoading && !goalsError && goals && goals.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          Пока нет целей
        </div>
      )}

      {/* Grid */}
      {!goalsLoading && !goalsError && goals && goals.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {goals.map((goal) => (
            <GoalCard
              key={goal.id}
              goal={goal}
              premiseNames={goal.premise_ids?.map((pid) => premiseNameMap.get(pid) ?? "Вводная") ?? []}
              onEdit={(g) => {
                setEditingId(g.id)
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
              {editingId ? "Редактировать цель" : "Добавить цель"}
            </DialogTitle>
          </DialogHeader>
          <GoalForm
            initialData={editingId ? (goals?.find((g) => g.id === editingId)) as GoalUpdate : undefined}
            premiseNames={premiseNameMap}
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
