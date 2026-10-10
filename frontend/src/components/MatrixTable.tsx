import { useMemo } from "react"
import type { CrossTask } from "@/api/matrixApi"
import { MatrixCell } from "./MatrixCell"

interface MatrixTableProps {
  crossTasks: CrossTask[]
  onCellClick: (
    crossTask: CrossTask | null,
    fromSection: string,
    toSection: string,
  ) => void
}

export function MatrixTable({ crossTasks, onCellClick }: MatrixTableProps) {
  // Собираем все разделы из cross_tasks
  const sections = useMemo(() => {
    const set = new Set<string>()
    crossTasks.forEach((ct) => {
      set.add(ct.from_section_code)
      set.add(ct.to_section_code)
    })
    return Array.from(set).sort()
  }, [crossTasks])

  // Индексируем по (from, to)
  const matrixMap = useMemo(() => {
    const map = new Map<string, CrossTask>()
    crossTasks.forEach((ct) => {
      map.set(`${ct.from_section_code}|${ct.to_section_code}`, ct)
    })
    return map
  }, [crossTasks])

  if (sections.length === 0) {
    return (
      <div className="text-muted-foreground py-8 text-center">
        Матрица пуста. Импортируйте задачи с заполненными полями «Раздел (от кого)»
        и «Получатель (кому)», затем нажмите «Сгенерировать матрицу».
      </div>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="border-collapse">
        <thead>
          <tr>
            <th className="sticky left-0 bg-background z-10 p-2 border-r border-b text-xs font-medium text-muted-foreground min-w-[80px] text-left">
              от кого ↓ / кому →
            </th>
            {sections.map((to) => (
              <th
                key={to}
                className="p-2 border-r border-b text-xs font-semibold min-w-[80px] text-center bg-muted/30"
              >
                {to}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sections.map((from) => (
            <tr key={from}>
              <th className="sticky left-0 bg-muted/30 z-10 p-2 border-r border-b text-xs font-semibold text-left min-w-[80px]">
                {from}
              </th>
              {sections.map((to) => {
                const ct = matrixMap.get(`${from}|${to}`) || null
                const isDiagonal = from === to
                if (isDiagonal) {
                  return (
                    <td
                      key={to}
                      className="border-r border-b bg-muted/50 w-20"
                      title="Диагональ"
                    />
                  )
                }
                return (
                  <td key={to} className="p-0 w-20">
                    <MatrixCell
                      crossTask={ct}
                      fromSection={from}
                      toSection={to}
                      onClick={onCellClick}
                    />
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}