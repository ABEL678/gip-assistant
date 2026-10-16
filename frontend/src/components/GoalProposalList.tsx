import { useState } from "react"
import { RefreshCw, Check, Pencil, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  type GoalProposal,
  type GoalProposalApprove,
} from "@/api/goalApi"

const RULE_LABELS: Record<string, string> = {
  договор_срок: "Договор + срок",
  тз_требование: "ТЗ + требование",
  требование_заказчика: "Требование заказчика",
  просроченный_ид: "Просроченные ИД",
}

const RULE_BADGE: Record<string, "default" | "secondary" | "outline"> = {
  договор_срок: "default",
  тз_требование: "default",
  требование_заказчика: "secondary",
  просроченный_ид: "outline",
}

interface GoalProposalListProps {
  proposals: GoalProposal[]
  premiseNames: Map<string, string>
  onApprove: (data: GoalProposalApprove) => void
  onReject: (premiseId: string) => void
  onEdit: (proposal: GoalProposal) => void
  onRefresh: () => void
}

export function GoalProposalList({
  proposals,
  premiseNames,
  onApprove,
  onReject,
  onEdit,
  onRefresh,
}: GoalProposalListProps) {
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
        <h3 className="text-lg font-semibold">Предложенные цели</h3>
        <Button variant="outline" size="sm" onClick={onRefresh}>
          <RefreshCw className="h-4 w-4 mr-1" /> Обновить
        </Button>
      </div>

      <div className="space-y-3">
        {proposals.map((proposal) => {
          const { id, premise, formulation, deadline, priority, rule, premise_ids } = proposal
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
                    {deadline && (
                      <Badge variant="outline">Срок: {deadline}</Badge>
                    )}
                    {priority !== null && (
                      <Badge variant="outline">Приоритет: {priority}</Badge>
                    )}
                  </div>

                  <p className="font-medium">{formulation}</p>

                  {premise_ids.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {premise_ids.map((pid) => (
                        <Badge key={pid} variant="outline" className="text-xs">
                          {premiseNames.get(pid) ?? "Вводная"}
                        </Badge>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {isEditing ? (
                <div className="pt-2 border-t">
                  <p className="text-sm text-muted-foreground mb-2">
                    Режим редактирования — откройте GoalForm для правок
                  </p>
                  <div className="flex gap-2">
                    <Button
                      size="sm"
                      onClick={() => {
                        onEdit(proposal)
                      }}
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
                        deadline: deadline || null,
                        priority: priority ?? null,
                        premise_ids,
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
                    onClick={() => onReject(premise.id)}
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
