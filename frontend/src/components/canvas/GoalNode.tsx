import { Handle, Position } from "@xyflow/react"
import type { Goal } from "@/api/goalApi"
import { Trash2 } from "lucide-react"

const STATE_LABELS: Record<string, string> = {
  plan: "План",
  in_progress: "В работе",
  achieved: "Достигнуто",
  cancelled: "Отменено",
}

const STATE_COLORS: Record<string, string> = {
  plan: "bg-gray-100 border-gray-300",
  in_progress: "bg-blue-100 border-blue-300",
  achieved: "bg-green-100 border-green-300",
  cancelled: "bg-red-100 border-red-300",
}

export function GoalNode({ data }: { data: { goal: Goal; onDelete?: (id: string) => void } }) {
  const g = data.goal
  return (
    <div
      className={`rounded-lg border-2 p-3 min-w-[220px] max-w-[300px] relative group ${
        STATE_COLORS[g.state] || "bg-blue-100 border-blue-300"
      }`}
    >
      {data.onDelete && (
        <button
          onClick={() => data.onDelete?.(g.id)}
          className="absolute top-1 right-1 opacity-0 group-hover:opacity-100 transition p-1 hover:bg-red-100 rounded"
          title="Удалить"
        >
          <Trash2 className="h-3 w-3 text-red-600" />
        </button>
      )}
      <Handle type="target" position={Position.Left} />
      <div className="text-xs font-semibold uppercase text-gray-600 mb-1">
        Цель · {STATE_LABELS[g.state] || g.state}
      </div>
      <div className="font-medium text-sm">{g.formulation}</div>
      {g.deadline && (
        <div className="text-xs text-gray-600 mt-1">до {g.deadline}</div>
      )}
      {g.priority && (
        <div className="text-xs text-gray-500 mt-1">Приоритет: {g.priority}</div>
      )}
    </div>
  )
}
