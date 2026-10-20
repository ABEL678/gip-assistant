import { type Revision } from "@/api/revisionApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Eye, Trash2 } from "lucide-react"

interface RevisionCardProps {
  revision: Revision
  onOpen: (revision: Revision) => void
  onDelete: (id: string) => void
}

export function RevisionCard({ revision, onOpen, onDelete }: RevisionCardProps) {
  const { id, version, date, source, notified, stop_flag, created_at } = revision

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <CardTitle className="text-base">
          Ревизия v{version}
        </CardTitle>
        <div className="flex gap-1">
          {notified && (
            <Badge variant="secondary">Уведомил</Badge>
          )}
          {stop_flag && (
            <Badge variant="destructive">⚠ Стоп</Badge>
          )}
        </div>
      </CardHeader>

      <CardContent className="space-y-2 text-sm">
        {date && (
          <p className="text-muted-foreground">
            Дата: {new Date(date).toLocaleDateString("ru-RU")}
          </p>
        )}
        {source && (
          <p className="text-muted-foreground">
            Источник: {source}
          </p>
        )}
        <p className="text-xs text-muted-foreground">
          Создана: {new Date(created_at).toLocaleDateString("ru-RU")}
        </p>
      </CardContent>

      <CardFooter className="gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={(e) => {
            e.stopPropagation()
            onOpen(revision)
          }}
        >
          <Eye className="h-4 w-4 mr-1" /> Открыть
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
