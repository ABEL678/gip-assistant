import { type EntityType } from "@/api/entityApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Pencil, Trash2 } from "lucide-react"

function pluralize(one: string, few: string, many: string, n: number): string {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod10 === 1 && mod100 !== 11) return one
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return few
  return many
}

interface EntityTypeCardProps {
  entityType: EntityType
  onEdit: (id: string) => void
  onDelete: (id: string) => void
}

export function EntityTypeCard({ entityType, onEdit, onDelete }: EntityTypeCardProps) {
  const { id, name, icon, description, schema, is_system, color } = entityType

  return (
    <Card
      className="hover:shadow-md cursor-pointer transition-shadow"
      style={{ borderColor: color || undefined }}
    >
      <CardHeader className="flex flex-row items-start gap-3">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{icon}</span>
          <CardTitle>{name}</CardTitle>
        </div>
      </CardHeader>

      <CardContent>
        <Badge variant="secondary">
          {schema.fields.length} {pluralize("поле", "поля", "полей", schema.fields.length)}
        </Badge>
        {description && (
          <p className="mt-2 text-sm text-muted-foreground line-clamp-2">
            {description}
          </p>
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
          <Pencil className="h-4 w-4" /> Редактировать
        </Button>
        {!is_system && (
          <Button
            variant="destructive"
            size="sm"
            onClick={(e) => {
              e.stopPropagation()
              onDelete(id)
            }}
          >
            <Trash2 className="h-4 w-4" /> Удалить
          </Button>
        )}
      </CardFooter>
    </Card>
  )
}
