import { useState } from "react"
import { RefreshCw, Check, Pencil, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  type DecisionProposal,
  type DecisionProposalApprove,
} from "@/api/decisionApi"

const RULE_LABELS: Record<string, string> = {
  goal_без_решения: "Goal без решения",
  срок_из_вводных: "Срок из вводных",
}

const RULE_BADGE: Record<string, "default" | "secondary" | "outline"> = {
  goal_без_решения: "default",
  срок_из_вводных: "secondary",
}

interface DecisionProposalListProps {
  proposals: DecisionProposal[]
  onApprove: (data: DecisionProposalApprove) => void
  onReject: (proposalId: string) => void
  onEdit: (proposal: DecisionProposal) => void
  onRefresh: () => void
}

export function DecisionProposalList({
  proposals,
  onApprove,
  onReject,
  onEdit,
  onRefresh,
}: DecisionProposalListProps) {
  const [editingId, setEditingId] = useState<string | null>(null)

  if (proposals.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        Нет предложений
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">Предложенные решения</h3>
        <Button variant="outline" size="sm" onClick={onRefresh}>
          <RefreshCw className="h-4 w-4 mr-1" /> Обновить
        </Button>
      </div>

      <div className="space-y-3">
        {proposals.map((proposal) => {
          const { id, formulation, rationale, rule, premise_ids, goal_ids } = proposal
          const isEditing = editingId === id

          return (
            <div
              key={id}
              className="border rounded-lg p-4 space-y-3"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 space-y-2">
                  <div className="flex items-center gap-2">
                    <Badge variant={RULE_BADGE[rule] ?? "secondary"}>
                      {RULE_LABELS[rule] ?? rule}
                    </Badge>
                    <Badge variant="outline">Вводных: {premise_ids.length}</Badge>
                    <Badge variant="outline">Целей: {goal_ids.length}</Badge>
                  </div>

                  <p className="font-medium">{formulation}</p>

                  {rationale && (
                    <p className="text-sm text-muted-foreground">{rationale}</p>
                  )}
                </div>
              </div>

              {isEditing ? (
                <div className="pt-2 border-t">
                  <p className="text-sm text-muted-foreground mb-2">
                    Режим редактирования — откройте DecisionForm для правок
                  </p>
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      onClick={() => onEdit(proposal)}
                    >
                      <Pencil className="h-4 w-4 mr-1" /> Открыть форму
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setEditingId(null)}
                    >
                      Отмена
                    </Button>
                  </div>
                </div>
              ) : (
                <div className="flex gap-2 pt-1">
                  <Button
                    size="sm"
                    onClick={() =>
                      onApprove({
                        formulation,
                        rationale: rationale || null,
                        premise_ids,
                        goal_ids,
                      })
                    }
                  >
                    <Check className="h-4 w-4 mr-1" /> Утвердить
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setEditingId(id)}
                  >
                    <Pencil className="h-4 w-4 mr-1" /> С правками
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => onReject(id)}
                  >
                    <X className="h-4 w-4 mr-1" /> Отклонить
                  </Button>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
