import { type Entity, type FieldDefinition } from "@/api/entityApi"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Button } from "@/components/ui/button"
import { Trash2 } from "lucide-react"
import { DynamicField } from "./DynamicField"

export interface DynamicTableProps {
  fields: FieldDefinition[]
  entities: Entity[]
  onDelete?: (entityId: string) => void
}

export function DynamicTable({ fields, entities, onDelete }: DynamicTableProps) {
  if (entities.length === 0) {
    return <p className="text-muted-foreground p-4">Пока нет записей</p>
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          {fields.map((f) => (
            <TableHead key={f.key}>{f.label}</TableHead>
          ))}
          {onDelete && <TableHead className="w-[60px]"></TableHead>}
        </TableRow>
      </TableHeader>
      <TableBody>
        {entities.map((entity) => (
          <TableRow key={entity.id}>
            {fields.map((field) => (
              <TableCell key={field.key}>
                <DynamicField field={field} value={entity.data[field.key]} />
              </TableCell>
            ))}
            {onDelete && (
              <TableCell>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => onDelete(entity.id)}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </TableCell>
            )}
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
