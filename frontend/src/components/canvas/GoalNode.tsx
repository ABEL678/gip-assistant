import { Handle, Position } from "@xyflow/react"
import type { Goal } from "@/api/goalApi"

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

export function GoalNode({ data }: { data: { goal: Goal } }) {
  const g = data.goal
  return (
    <div
      className={`rounded-lg border-2 p-3 min-w-[220px] max-w-[300px] ${
        STATE_COLORS[g.state] || "bg-blue-100 border-blue-300"
      }`}
    >
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
