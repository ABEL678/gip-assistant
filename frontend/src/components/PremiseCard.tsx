import { type Premise } from "@/api/premiseApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Pencil, Trash2 } from "lucide-react"

const CATEGORY_LABELS: Record<string, string> = {
  contract: "Договор",
  tz: "ТЗ",
  customer_requirement: "Требование заказчика",
  source_data: "Исходные данные",
  norm: "Нормативные",
  npa: "НПА",
  bureaucracy: "Бюрократия",
  internal: "Внутренние",
}

const CATEGORY_BADGE: Record<string, "default" | "secondary" | "outline"> = {
  contract: "default",
  tz: "default",
  customer_requirement: "secondary",
  source_data: "secondary",
  norm: "outline",
  npa: "outline",
  bureaucracy: "outline",
  internal: "default",
}

interface PremiseCardProps {
  premise: Premise
  onEdit: (id: string) => void
  onDelete: (id: string) => void
}

export function PremiseCard({ premise, onEdit, onDelete }: PremiseCardProps) {
  const { id, name, category, source, date, link, valid_until, actual, mandatory } = premise

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <CardTitle className="text-base flex-1">{name}</CardTitle>
        <Badge variant={CATEGORY_BADGE[category] ?? "secondary"}>
          {CATEGORY_LABELS[category] ?? category}
        </Badge>
      </CardHeader>

      <CardContent className="space-y-2 text-sm">
        {source && (
          <p className="text-muted-foreground">Источник: {source}</p>
        )}
        {date && (
          <p className="text-muted-foreground">Вступила: {date}</p>
        )}
        {valid_until && (
          <p className="text-muted-foreground">Действует до: {valid_until}</p>
        )}
        {link && (
          <a
            href={link}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline text-sm"
          >
            Ссылка на документ
          </a>
        )}
        <div className="flex gap-2 pt-1">
          {!actual && <Badge variant="destructive">Не актуальна</Badge>}
          {!mandatory && <Badge variant="outline">Не обязательна</Badge>}
        </div>
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
