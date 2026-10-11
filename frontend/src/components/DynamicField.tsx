import { type FieldDefinition } from "@/api/entityApi"
import { Badge } from "@/components/ui/badge"

export interface DynamicFieldProps {
  field: FieldDefinition
  value: unknown
}

function isEmpty(value: unknown): boolean {
  return value === null || value === undefined || value === ""
}

export function DynamicField({ field, value }: DynamicFieldProps) {
  if (isEmpty(value)) {
    return <span className="text-muted-foreground">—</span>
  }

  switch (field.type) {
    case "text":
    case "textarea":
    case "url":
    case "email":
      return <span>{String(value)}</span>

    case "number":
      return <span>{value as number}</span>

    case "date": {
      const dateStr = String(value)
      const parsed = new Date(dateStr)
      const formatted = isNaN(parsed.getTime()) ? dateStr : parsed.toLocaleDateString("ru-RU")
      return <span>{formatted}</span>
    }

    case "select":
      return <Badge variant="secondary">{String(value)}</Badge>

    case "multiselect": {
      const values = value as string[]
      return (
        <div className="flex flex-wrap gap-1">
          {values.map((v) => (
            <Badge key={v} variant="secondary">
              {v}
            </Badge>
          ))}
        </div>
      )
    }

    case "boolean":
      return <span>{value ? "Да" : "Нет"}</span>

    default:
      return <span className="text-muted-foreground">{String(value)}</span>
  }
}
