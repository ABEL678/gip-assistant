import { type Goal, type GoalState, type VerificationStatus } from "@/api/goalApi"
import { type ValidationResult } from "@/api/goalApi"
import { goalApi } from "@/api/goalApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ChevronDown, Pencil, Trash2, ShieldCheck } from "lucide-react"
import { useState } from "react"

const STATE_LABELS: Record<GoalState, string> = {
  plan: "В плане",
  in_progress: "В работе",
  achieved: "Достигнута",
  cancelled: "Отменена",
}

const STATE_BADGE: Record<GoalState, "default" | "secondary" | "destructive" | "outline"> = {
  plan: "default",
  in_progress: "secondary",
  achieved: "outline",
  cancelled: "destructive",
}

const VERIFICATION_LABELS: Record<VerificationStatus, string> = {
  confirmed: "Подтверждена",
  requires_check: "Требуется проверка",
  no_data: "Нет данных",
  not_confirmed: "Не подтверждена",
}

const VERIFICATION_BADGE: Record<VerificationStatus, "default" | "secondary" | "destructive" | "outline"> = {
  confirmed: "default",
  requires_check: "secondary",
  no_data: "outline",
  not_confirmed: "destructive",
}

interface GoalCardProps {
  goal: Goal
  premiseNames?: string[]
  onEdit: (goal: Goal) => void
  onDelete: (id: string) => void
  onValidate?: (goalId: string) => void
}

export function GoalCard({ goal, premiseNames = [], onEdit, onDelete, onValidate }: GoalCardProps) {
  const { id, formulation, deadline, priority, state, premise_ids, verification_status } = goal
  const [evidence, setEvidence] = useState<ValidationResult | null>(null)
  const [showEvidence, setShowEvidence] = useState(false)
  const [validating, setValidating] = useState(false)

  const handleValidate = async () => {
    if (onValidate) {
      onValidate(id)
      return
    }
    setValidating(true)
    try {
      const result = await goalApi.validateGoal(id)
      setEvidence(result)
      setShowEvidence(true)
    } finally {
      setValidating(false)
    }
  }

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <CardTitle className="text-base flex-1">{formulation}</CardTitle>
        <div className="flex gap-1">
          <Badge variant={STATE_BADGE[state] ?? "default"}>
            {STATE_LABELS[state]}
          </Badge>
          <Badge variant={VERIFICATION_BADGE[verification_status] ?? "outline"}>
            {VERIFICATION_LABELS[verification_status]}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-2 text-sm">
        {deadline && (
          <p className="text-muted-foreground">Срок: {deadline}</p>
        )}
        {priority !== null && (
          <p className="text-muted-foreground">Приоритет: {priority}</p>
        )}
        {premiseNames.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-2">
            {premiseNames.slice(0, 3).map((name) => (
              <Badge key={name} variant="outline" className="text-xs">
                {name}
              </Badge>
            ))}
            {premise_ids.length > 3 && (
              <Badge variant="outline" className="text-xs">
                +{premise_ids.length - 3}
              </Badge>
            )}
          </div>
        )}
      </CardContent>

      {showEvidence && evidence && (
        <div className="px-6 pb-2 space-y-2 border-t pt-2">
          <div className="flex items-center justify-between">
            <p className="text-xs font-semibold text-muted-foreground">Результат проверки:</p>
            <Button
              variant="ghost"
              size="sm"
              className="h-5 px-1 text-xs"
              onClick={() => setShowEvidence(false)}
            >
              <ChevronDown className="h-3 w-3" />
            </Button>
          </div>
          {evidence.evidence.length > 0 && (
            <div>
              <p className="text-xs font-medium">Доказательства:</p>
              {evidence.evidence.map((ev, i) => (
                <div key={i} className="text-xs text-muted-foreground ml-2">
                  {ev.field}: {String(ev.value)}{" "}
                  <Badge variant="secondary" className="text-[9px]">{ev.owner}</Badge>
                </div>
              ))}
            </div>
          )}
          {evidence.missing.length > 0 && (
            <div>
              <p className="text-xs font-medium text-amber-600">Не подтверждено:</p>
              {evidence.missing.map((m, i) => (
                <p key={i} className="text-xs text-muted-foreground ml-2">– {m}</p>
              ))}
            </div>
          )}
          {evidence.contradictions.length > 0 && (
            <div>
              <p className="text-xs font-medium text-destructive">Противоречия:</p>
              {evidence.contradictions.map((c, i) => (
                <p key={i} className="text-xs text-muted-foreground ml-2">– {c}</p>
              ))}
            </div>
          )}
        </div>
      )}

      <CardFooter className="gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={handleValidate}
          disabled={validating}
          className="h-7 text-xs"
        >
          {validating ? (
            "Проверка..."
          ) : (
            <>
              <ShieldCheck className="h-3 w-3 mr-1" /> Проверить
            </>
          )}
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={(e) => {
            e.stopPropagation()
            onEdit(goal)
          }}
        >
          <Pencil className="h-4 w-4 mr-1" /> Изменить
        </Button>
        <Button
          variant="destructive"
          size="sm"
          onClick={(e) => {
            e.stopPropagation()
            onDelete(id)
          }}
        >
          <Trash2 className="h-4 w-4 mr-1" /> Удалить
        </Button>
      </CardFooter>
    </Card>
  )
}
