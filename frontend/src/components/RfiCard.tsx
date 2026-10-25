import {
  type Rfi,
  RFI_STATE_COLORS,
  RFI_STATE_LABELS,
  formatIsoDate,
} from "@/api/rfiApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Pencil, Trash2 } from "lucide-react"

interface RfiCardProps {
  rfi: Rfi
  causeLabel: string | null
  premiseLabels: string[]
  onEdit: (rfi: Rfi) => void
  onDelete: (rfiId: string) => void
}

function todayISO(): string {
  const now = new Date()
  const month = String(now.getMonth() + 1).padStart(2, "0")
  const day = String(now.getDate()).padStart(2, "0")
  return `${now.getFullYear()}-${month}-${day}`
}

export function RfiCard({ rfi, causeLabel, premiseLabels, onEdit, onDelete }: RfiCardProps) {
  const { id, title, rfi_due_date, rfi_state, created_at } = rfi

  // Сравнение ISO-строк YYYY-MM-DD с локальной датой — без TZ-сдвигов.
  const overdue =
    rfi_due_date !== null &&
    rfi_due_date < todayISO() &&
    !["closed", "registered"].includes(rfi_state)

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <CardTitle className="text-base flex-1 line-clamp-2">{title}</CardTitle>
        <Badge className={RFI_STATE_COLORS[rfi_state]}>
          {RFI_STATE_LABELS[rfi_state]}
        </Badge>
      </CardHeader>

      <CardContent className="space-y-2 text-sm">
        <p>
          <span className="text-muted-foreground">Причина: </span>
          {causeLabel ?? "—"}
        </p>

        <p>
          <span className="text-muted-foreground">Срок: </span>
          {rfi_due_date ? (
            <span className={overdue ? "text-red-600 font-medium" : undefined}>
              {formatIsoDate(rfi_due_date)}
              {overdue && " — просрочен"}
            </span>
          ) : (
            "—"
          )}
        </p>

        <div className="flex flex-wrap items-center gap-1">
          <span className="text-muted-foreground">Связи: </span>
          {premiseLabels.length === 0 ? (
            "—"
          ) : (
            <>
              {premiseLabels.slice(0, 3).map((label, index) => (
                <Badge key={`${label}-${index}`} variant="secondary">
                  {label}
                </Badge>
              ))}
              {premiseLabels.length > 3 && (
                <Badge variant="outline">+{premiseLabels.length - 3}</Badge>
              )}
            </>
          )}
        </div>

        <p className="text-xs text-muted-foreground">
          Создан: {created_at ? new Date(created_at).toLocaleDateString("ru-RU") : "—"}
        </p>
      </CardContent>

      <CardFooter className="gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={(e) => {
            e.stopPropagation()
            onEdit(rfi)
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
