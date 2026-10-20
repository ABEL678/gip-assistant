import { type ProjectStandard, type ProjectStandardType } from "@/api/projectStandardApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Pencil, Trash2 } from "lucide-react"

const TYPE_LABELS: Record<ProjectStandardType, string> = {
  deadline: "Срок",
  composition: "Состав",
  format: "Формат",
}

const TYPE_BADGE: Record<ProjectStandardType, "default" | "secondary" | "outline"> = {
  deadline: "default",
  composition: "secondary",
  format: "outline",
}

interface ProjectStandardCardProps {
  standard: ProjectStandard
  onEdit: (standard: ProjectStandard) => void
  onDelete: (id: string) => void
}

export function ProjectStandardCard({ standard, onEdit, onDelete }: ProjectStandardCardProps) {
  const { id, type, value, premise_id, created_at } = standard

  const valuePreview = value
    ? JSON.stringify(value).replace(/\n/g, " ").slice(0, 120) + (JSON.stringify(value).length > 120 ? "…" : "")
    : "—"

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <CardTitle className="text-base flex-1">
          Стандарт: {premise_id.slice(0, 8)}…
        </CardTitle>
        <Badge variant={TYPE_BADGE[type]}>
          {TYPE_LABELS[type]}
        </Badge>
      </CardHeader>

      <CardContent className="space-y-2 text-sm">
        <p className="text-muted-foreground font-mono text-xs break-all">
          {valuePreview}
        </p>
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
            onEdit(standard)
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
