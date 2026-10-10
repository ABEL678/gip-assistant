import { CROSS_TASK_STATUS_COLORS, type CrossTask } from "@/api/matrixApi"

interface MatrixCellProps {
  crossTask: CrossTask | null
  fromSection: string
  toSection: string
  onClick: (crossTask: CrossTask | null, fromSection: string, toSection: string) => void
}

export function MatrixCell({
  crossTask,
  fromSection,
  toSection,
  onClick,
}: MatrixCellProps) {
  // Цветовая индикация
  let cellClass = "bg-background hover:bg-muted/50 cursor-pointer"
  let label = "—"
  let count = ""

  if (crossTask) {
    cellClass = `${CROSS_TASK_STATUS_COLORS[crossTask.status]} hover:opacity-80 cursor-pointer`
    label = "●"
    // Счётчик задач из description (формат: "Задач: N, просрочено: M, готово: K")
    if (crossTask.description) {
      const m = crossTask.description.match(/Задач:\s*(\d+)/)
      if (m) count = m[1]
    }
  }

  return (
        <button
      type="button"
      onClick={() => onClick(crossTask, fromSection, toSection)}
      className={`
        w-full h-12 flex items-center justify-center gap-1
        border-r border-b text-sm font-medium
        transition-colors ${cellClass}
      `}
    >
      {label}
      {count && <span className="text-xs opacity-75">{count}</span>}
    </button>
  )
}