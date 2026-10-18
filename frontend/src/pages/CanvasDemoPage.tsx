import {
  ReactFlow,
  Background,
  Controls,
  Position,
  type Node,
  type Edge,
} from "@xyflow/react"
import "@xyflow/react/dist/style.css"

// ====================================================================
// Минимальный граф: 8 узлов, 6 связей
// ====================================================================

const NODES: Node[] = [
  // Левая колонка (x=50)
  {
    id: "submit-pd",
    type: "default",
    position: { x: 50, y: 100 },
    data: { label: "Сдать ПД" },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
  },
  {
    id: "submit-rd",
    type: "default",
    position: { x: 50, y: 400 },
    data: { label: "Сдать РД" },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
  },
  // Правая колонка (x=400)
  {
    id: "ar-pd",
    type: "default",
    position: { x: 400, y: 50 },
    data: { label: "АР (ПД)" },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
  },
  {
    id: "kr-pd",
    type: "default",
    position: { x: 400, y: 150 },
    data: { label: "КР (ПД)" },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
  },
  {
    id: "vk-pd",
    type: "default",
    position: { x: 400, y: 250 },
    data: { label: "ВК (ПД)" },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
  },
  {
    id: "ar-rd",
    type: "default",
    position: { x: 400, y: 400 },
    data: { label: "АР (РД)" },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
  },
  {
    id: "kr-rd",
    type: "default",
    position: { x: 400, y: 500 },
    data: { label: "КР (РД)" },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
  },
  {
    id: "vk-rd",
    type: "default",
    position: { x: 400, y: 600 },
    data: { label: "ВК (РД)" },
    sourcePosition: Position.Right,
    targetPosition: Position.Left,
  },
]

const EDGES: Edge[] = [
  // "Сдать ПД" → правая колонка
  { id: "e1", source: "submit-pd", target: "ar-pd", type: "smoothstep" },
  { id: "e2", source: "submit-pd", target: "kr-pd", type: "smoothstep" },
  { id: "e3", source: "submit-pd", target: "vk-pd", type: "smoothstep" },
  // "Сдать РД" → правая колонка
  { id: "e4", source: "submit-rd", target: "ar-rd", type: "smoothstep" },
  { id: "e5", source: "submit-rd", target: "kr-rd", type: "smoothstep" },
  { id: "e6", source: "submit-rd", target: "vk-rd", type: "smoothstep" },
  // Пунктирные красные связи ПД → РД
  {
    id: "e-dash-1",
    source: "ar-pd",
    target: "ar-rd",
    type: "smoothstep",
    style: { stroke: "#ef4444", strokeDasharray: "8 4" },
  },
  {
    id: "e-dash-2",
    source: "kr-pd",
    target: "kr-rd",
    type: "smoothstep",
    style: { stroke: "#ef4444", strokeDasharray: "8 4" },
  },
  {
    id: "e-dash-3",
    source: "vk-pd",
    target: "vk-rd",
    type: "smoothstep",
    style: { stroke: "#ef4444", strokeDasharray: "8 4" },
  },
]

export function CanvasDemoPage() {
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Верхняя панель */}
      <div className="flex items-center gap-3 px-4 py-2 border-b bg-white">
        <h1 className="text-lg font-bold">Граф целей (минимальный)</h1>
        <span className="text-xs text-gray-400">8 узлов · 9 связей</span>
      </div>

      {/* Канвас */}
      <div className="flex-1 relative">
        <ReactFlow
          nodes={NODES}
          edges={EDGES}
          nodeTypes={{
            default: (props) => (
              <div className="px-4 py-2 bg-white border-2 border-gray-300 rounded-lg shadow-sm text-sm font-medium whitespace-nowrap">
                {props.data.label}
              </div>
            ),
          }}
          defaultViewport={{ x: 0, y: 0, zoom: 0.9 }}
          fitView
          fitViewOptions={{ padding: 0.3 }}
          minZoom={0.3}
          maxZoom={2}
        >
          <Background color="#e5e7eb" gap={16} />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  )
}
