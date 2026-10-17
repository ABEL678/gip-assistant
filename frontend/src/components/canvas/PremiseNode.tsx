import { Handle, Position } from "@xyflow/react"
import type { Premise } from "@/api/premiseApi"
import { Trash2 } from "lucide-react"

const CATEGORY_LABELS: Record<string, string> = {
  contract: "Договор",
  tz: "ТЗ",
  customer_requirement: "Требование",
  source_data: "ИД",
  norm: "Норма",
  npa: "НПА",
  bureaucracy: "Бюрократия",
  internal: "Ресурс",
}

const CATEGORY_COLORS: Record<string, string> = {
  contract: "bg-purple-100 border-purple-300",
  tz: "bg-blue-100 border-blue-300",
  customer_requirement: "bg-orange-100 border-orange-300",
  source_data: "bg-green-100 border-green-300",
  norm: "bg-gray-100 border-gray-300",
  npa: "bg-gray-100 border-gray-300",
  bureaucracy: "bg-gray-100 border-gray-300",
  internal: "bg-gray-100 border-gray-300",
}

export function PremiseNode({ data }: { data: { premise: Premise; onDelete?: (id: string) => void } }) {
  const p = data.premise
  return (
    <div
      className={`rounded-lg border-2 p-3 min-w-[200px] max-w-[280px] relative group ${
        CATEGORY_COLORS[p.category] || "bg-gray-100 border-gray-300"
      }`}
    >
      {data.onDelete && (
        <button
          onClick={() => data.onDelete?.(p.id)}
          className="absolute top-1 right-1 opacity-0 group-hover:opacity-100 transition p-1 hover:bg-red-100 rounded"
          title="Удалить"
        >
          <Trash2 className="h-3 w-3 text-red-600" />
        </button>
      )}
      <div className="text-xs font-semibold uppercase text-gray-600 mb-1">
        {CATEGORY_LABELS[p.category] || p.category}
      </div>
      <div className="font-medium text-sm">{p.name}</div>
      {p.source && (
        <div className="text-xs text-gray-500 mt-1">{p.source}</div>
      )}
      {p.valid_until && (
        <div className="text-xs text-red-600 mt-1">до {p.valid_until}</div>
      )}
      <Handle type="source" position={Position.Right} />
    </div>
  )
}
