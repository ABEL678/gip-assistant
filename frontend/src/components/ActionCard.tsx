import { type Action, ACTION_STATE_LABELS } from "@/api/actionApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Pencil, Trash2 } from "lucide-react"

interface ActionCardProps {
  action: Action
  onEdit: (action: Action) => void
  onDelete: (id: string) => void
}

const STATE_BADGE_VARIANTS: Record<string, string> = {
  plan: "bg-gray-100 text-gray-800",
  in_progress: "bg-blue-100 text-blue-800",
  done: "bg-green-100 text-green-800",
  overdue: "bg-red-100 text-red-800",
  cancelled: "bg-zinc-200 text-zinc-800",
}

export function ActionCard({ action, onEdit, onDelete }: ActionCardProps) {
  const { id, formulation, measurable_result, deadline, state, created_at } = action

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <CardTitle className="text-base flex-1">{formulation}</CardTitle>
        <Badge className={STATE_BADGE_VARIANTS[state] ?? ""}>
          {ACTION_STATE_LABELS[state]}
        </Badge>
      </CardHeader>

      <CardContent className="space-y-2 text-sm">
        {measurable_result && (
          <p className="text-muted-foreground">Результат: {measurable_result}</p>
        )}
        {deadline && (
          <p className="text-xs text-muted-foreground">
            Дедлайн: {new Date(deadline).toLocaleDateString("ru-RU")}
          </p>
        )}
        <p className="text-xs text-muted-foreground">
          Создан: {new Date(created_at).toLocaleDateString("ru-RU")}
        </p>
      </CardContent>

      <CardFooter className="gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={(e) => {
            e.stopPropagation()
            onEdit(action)
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
