import { type Result } from "@/api/resultApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Pencil, Trash2 } from "lucide-react"

interface ResultCardProps {
  result: Result
  onEdit: (result: Result) => void
  onDelete: (id: string) => void
}

export function ResultCard({ result, onEdit, onDelete }: ResultCardProps) {
  const { id, formulation, source, created_at } = result

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <CardTitle className="text-base flex-1">{formulation}</CardTitle>
      </CardHeader>

      <CardContent className="space-y-2 text-sm">
        {source && (
          <p className="text-muted-foreground">Источник: {source}</p>
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
            onEdit(result)
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
