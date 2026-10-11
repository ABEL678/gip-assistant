import { type FieldDefinition } from "@/api/entityApi"
import { FieldEditor } from "./FieldEditor"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"

interface FieldListProps {
  fields: FieldDefinition[]
  onChange: (fields: FieldDefinition[]) => void
}

function generateNextKey(fields: FieldDefinition[]): string {
  let maxIndex = 0
  const regex = /^field_(\d+)$/
  for (const f of fields) {
    const match = f.key.match(regex)
    if (match) {
      const num = parseInt(match[1], 10)
      if (num > maxIndex) {
        maxIndex = num
      }
    }
  }
  return `field_${maxIndex + 1}`
}

export function FieldList({ fields, onChange }: FieldListProps) {
  const handleUpdate = (index: number, newField: FieldDefinition) => {
    onChange(fields.map((f, i) => (i === index ? newField : f)))
  }

  const handleDelete = (index: number) => {
    onChange(fields.filter((_, i) => i !== index))
  }

  const handleMove = (from: number, to: number) => {
    if (to < 0 || to >= fields.length) return
    const next = [...fields]
    const [moved] = next.splice(from, 1)
    next.splice(to, 0, moved)
    onChange(next)
  }

  const handleAdd = () => {
    const newField: FieldDefinition = {
      key: generateNextKey(fields),
      label: "Новое поле",
      type: "text",
      required: false,
    }
    onChange([...fields, newField])
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Поля</CardTitle>
      </CardHeader>

      <CardContent className="space-y-4">
        {fields.map((field, index) => (
          <FieldEditor
            key={field.key + "-" + index}
            field={field}
            index={index}
            onChange={(newField) => handleUpdate(index, newField)}
            onDelete={() => handleDelete(index)}
            onMoveUp={() => handleMove(index, index - 1)}
            onMoveDown={() => handleMove(index, index + 1)}
            canMoveUp={index > 0}
            canMoveDown={index < fields.length - 1}
          />
        ))}
      </CardContent>

      <CardFooter>
        <Button variant="outline" onClick={handleAdd}>
          <Plus className="h-4 w-4" /> Добавить поле
        </Button>
      </CardFooter>
    </Card>
  )
}
