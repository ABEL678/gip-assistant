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
  useDecisionLinks,
  useCreateDecisionLink,
  useDeleteDecisionLink,
} from "@/hooks/useDecisionLinks"
import { useDecisions } from "@/hooks/useDecisions"
import { DecisionLinkCard } from "@/components/DecisionLinkCard"
import { DecisionLinkForm } from "@/components/DecisionLinkForm"
import { type DecisionLinkCreate } from "@/api/decisionLinkApi"

export function DecisionLinkPage() {
  const { id: projectId } = useParams<{ id: string }>()

  const [showForm, setShowForm] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const { data: links, isLoading: linksLoading, isError: linksError } = useDecisionLinks(projectId!)
  const { data: decisions } = useDecisions(projectId!)
  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => projectsApi.getById(projectId!),
    enabled: !!projectId,
  })
  const createMutation = useCreateDecisionLink(projectId!)
  const deleteMutation = useDeleteDecisionLink(projectId!)

  const handleCreate = (data: DecisionLinkCreate) => {
    createMutation.mutate(data, {
      onError: (err: Error) => setError(err.message),
      onSuccess: () => setShowForm(false),
    })
  }

  const handleDelete = (id: string) => {
    if (window.confirm("Удалить эту связь?")) {
      deleteMutation.mutate(id)
    }
  }

  // Build decision ID → formulation map for card display
  const decisionMap = new Map<string, string>()
  decisions?.forEach((d) => {
    decisionMap.set(d.id, d.formulation)
  })

  if (linksLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (linksError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Ошибка загрузки связей</AlertDescription>
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
            Связи решений{project ? ` — ${project.name}` : ""}
          </h1>
          <p className="text-sm text-muted-foreground">
            Управление связями между решениями проекта
          </p>
        </div>
        <Button onClick={() => setShowForm(true)}>
          <Plus className="h-4 w-4 mr-2" /> Добавить связь
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Empty state */}
      {!linksLoading && !linksError && links && links.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          Пока нет связей
        </div>
      )}

      {/* Grid */}
      {!linksLoading && !linksError && links && links.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {links.map((link) => (
            <DecisionLinkCard
              key={link.id}
              link={link}
              fromFormulation={decisionMap.get(link.from_decision_id)}
              toFormulation={decisionMap.get(link.to_decision_id)}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}

      {/* Form Modal */}
      <Dialog open={showForm} onOpenChange={(open) => {
        if (!open) {
          setShowForm(false)
        }
      }}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Добавить связь</DialogTitle>
          </DialogHeader>
          <DecisionLinkForm
            decisions={decisions ?? []}
            onSubmit={handleCreate}
            onCancel={() => setShowForm(false)}
          />
        </DialogContent>
      </Dialog>
    </div>
  )
}
