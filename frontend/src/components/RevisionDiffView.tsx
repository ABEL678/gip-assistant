import { type Change } from "@/api/revisionApi"
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card"
import { Table, TableHeader, TableBody, TableRow, TableHead } from "@/components/ui/table"
import { ChangeRow } from "./ChangeRow"

interface RevisionDiffViewProps {
  changes: Change[]
  isLoading: boolean
  onDecideChange?: (change: Change) => void
}

export function RevisionDiffView({
  changes,
  isLoading,
  onDecideChange,
}: RevisionDiffViewProps) {
  if (isLoading) {
    return <div className="text-muted-foreground">Загрузка изменений...</div>
  }

  if (!changes || changes.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        Изменений нет
      </div>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Изменения ревизии</CardTitle>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[200px]">Поле</TableHead>
              <TableHead className="w-[200px]">Было</TableHead>
              <TableHead className="w-[200px]">Стало</TableHead>
              <TableHead className="w-[150px]">Статус</TableHead>
              <TableHead className="w-[180px]">Решение</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {changes.map((change) => (
              <ChangeRow
                key={change.id}
                change={change}
                onDecide={onDecideChange}
              />
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}
