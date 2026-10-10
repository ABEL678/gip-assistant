import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import type { ColumnMappingPayload } from "@/api/importApi"

const FIELD_LABELS: Record<keyof ColumnMappingPayload, string> = {
  task_title: "Название задачи *",
  description: "Описание",
  deadline: "Дедлайн",
  section: "Раздел (от кого)",
  to_section: "Получатель (кому)",
  assignee: "Исполнитель",
}

const SKIP_VALUE = "__skip__"

interface ColumnMappingTableProps {
  columns: string[]
  mapping: Partial<ColumnMappingPayload>
  onChange: (mapping: Partial<ColumnMappingPayload>) => void
}

export function ColumnMappingTable({
  columns,
  mapping,
  onChange,
}: ColumnMappingTableProps) {
  // Обратный маппинг: колонка → поле
  const columnToField: Record<string, keyof ColumnMappingPayload | ""> = {}
  for (const [field, col] of Object.entries(mapping)) {
    if (col) columnToField[col as string] = field as keyof ColumnMappingPayload
  }

  const handleChange = (column: string, fieldName: string) => {
    const next: Partial<ColumnMappingPayload> = { ...mapping }

    // Удаляем старую привязку этой колонки
    for (const key of Object.keys(next) as (keyof ColumnMappingPayload)[]) {
      if (next[key] === column) delete next[key]
    }

    // Удаляем это поле из других колонок
    if (fieldName !== SKIP_VALUE) {
      const field = fieldName as keyof ColumnMappingPayload
      next[field] = column
    }

    onChange(next)
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-1/3">Колонка Excel</TableHead>
          <TableHead>Поле задачи</TableHead>
          <TableHead className="w-1/3">Пример значения</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {columns.map((column) => {
          const currentField = columnToField[column] || SKIP_VALUE
          return (
            <TableRow key={column}>
              <TableCell className="font-medium">{column}</TableCell>
              <TableCell>
                <Select
                  value={currentField}
                  onValueChange={(v) => handleChange(column, v)}
                >
                  <SelectTrigger className="w-full">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value={SKIP_VALUE}>— не импортировать —</SelectItem>
                    {Object.entries(FIELD_LABELS).map(([field, label]) => (
                      <SelectItem key={field} value={field}>
                        {label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </TableCell>
              <TableCell className="text-sm text-muted-foreground">
                —
              </TableCell>
            </TableRow>
          )
        })}
      </TableBody>
    </Table>
  )
}