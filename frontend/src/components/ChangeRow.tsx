import { type Change } from "@/api/revisionApi"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Check } from "lucide-react"

interface ChangeRowProps {
  change: Change
  onDecide?: (change: Change) => void
}

const STATUS_CONFIG: Record<
  Change["status"],
  { label: string; variant: "default" | "secondary" | "destructive" | "outline" }
> = {
  added: { label: "Добавлено", variant: "default" },
  removed: { label: "Удалено", variant: "destructive" },
  changed: { label: "Изменено", variant: "outline" },
  unchanged: { label: "Без изменений", variant: "secondary" },
}

export function ChangeRow({ change, onDecide }: ChangeRowProps) {
  const statusConfig = STATUS_CONFIG[change.status]
  const showDecideButton = change.status !== "unchanged" && !!onDecide

  return (
    <tr className="border-b hover:bg-muted/50">
      <td className="py-3 px-4 font-medium text-sm">{change.field}</td>
      <td className="py-3 px-4 text-sm text-muted-foreground max-w-[200px] truncate">
        {change.old_value ?? "—"}
      </td>
      <td className="py-3 px-4 text-sm max-w-[200px] truncate">
        {change.new_value ?? "—"}
      </td>
      <td className="py-3 px-4">
        <Badge variant={statusConfig.variant}>
          {statusConfig.label}
        </Badge>
      </td>
      <td className="py-3 px-4">
        {showDecideButton && (
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation()
              onDecide?.(change)
            }}
          >
            <Check className="h-4 w-4 mr-1" />
            Принять решение
          </Button>
        )}
        {!showDecideButton && <span className="text-xs text-muted-foreground">—</span>}
      </td>
    </tr>
  )
}
