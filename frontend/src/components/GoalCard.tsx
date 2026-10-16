import { type Goal, type GoalState } from "@/api/goalApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Pencil, Trash2 } from "lucide-react"

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

interface GoalCardProps {
  goal: Goal
  premiseNames?: string[]
  onEdit: (id: string) => void
  onDelete: (id: string) => void
}

export function GoalCard({ goal, premiseNames = [], onEdit, onDelete }: GoalCardProps) {
  const { id, formulation, deadline, priority, state, premise_ids } = goal

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <CardTitle className="text-base flex-1">{formulation}</CardTitle>
        <Badge variant={STATE_BADGE[state] ?? "default"}>
          {STATE_LABELS[state]}
        </Badge>
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

      <CardFooter className="gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={(e) => {
            e.stopPropagation()
            onEdit(id)
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
