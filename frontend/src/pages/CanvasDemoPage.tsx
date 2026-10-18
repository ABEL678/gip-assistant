import { ReactFlow, Background, Controls, Position, MarkerType } from "@xyflow/react"
import "@xyflow/react/dist/style.css"

const initialNodes = [
  { id: "goal-pd",     position: { x: 100, y: 100 }, data: { label: "Сдать ПД" }, sourcePosition: Position.Right, targetPosition: Position.Left },
  { id: "goal-rd",     position: { x: 100, y: 450 }, data: { label: "Сдать РД" }, sourcePosition: Position.Right, targetPosition: Position.Left },
  { id: "ar-pd",       position: { x: 500, y: 50 },  data: { label: "АР (ПД)" },  sourcePosition: Position.Right, targetPosition: Position.Left },
  { id: "kr-pd",       position: { x: 500, y: 150 }, data: { label: "КР (ПД)" },  sourcePosition: Position.Right, targetPosition: Position.Left },
  { id: "vk-pd",       position: { x: 500, y: 250 }, data: { label: "ВК (ПД)" },  sourcePosition: Position.Right, targetPosition: Position.Left },
  { id: "ar-rd",       position: { x: 500, y: 450 }, data: { label: "АР (РД)" },  sourcePosition: Position.Right, targetPosition: Position.Left },
  { id: "kr-rd",       position: { x: 500, y: 550 }, data: { label: "КР (РД)" },  sourcePosition: Position.Right, targetPosition: Position.Left },
  { id: "vk-rd",       position: { x: 500, y: 650 }, data: { label: "ВК (РД)" },  sourcePosition: Position.Right, targetPosition: Position.Left },
]

const initialEdges = [
  { id: "e1", source: "goal-pd", target: "ar-pd", type: "smoothstep", markerEnd: { type: MarkerType.ArrowClosed } },
  { id: "e2", source: "goal-pd", target: "kr-pd", type: "smoothstep", markerEnd: { type: MarkerType.ArrowClosed } },
  { id: "e3", source: "goal-pd", target: "vk-pd", type: "smoothstep", markerEnd: { type: MarkerType.ArrowClosed } },
  { id: "e4", source: "goal-rd", target: "ar-rd", type: "smoothstep", markerEnd: { type: MarkerType.ArrowClosed } },
  { id: "e5", source: "goal-rd", target: "kr-rd", type: "smoothstep", markerEnd: { type: MarkerType.ArrowClosed } },
  { id: "e6", source: "goal-rd", target: "vk-rd", type: "smoothstep", markerEnd: { type: MarkerType.ArrowClosed } },
  // зависимости ПД → РД (пунктир, красный)
  { id: "e7", source: "ar-pd", target: "ar-rd", type: "smoothstep", style: { stroke: "red", strokeDasharray: "5,5" }, markerEnd: { type: MarkerType.ArrowClosed, color: "red" } },
  { id: "e8", source: "kr-pd", target: "kr-rd", type: "smoothstep", style: { stroke: "red", strokeDasharray: "5,5" }, markerEnd: { type: MarkerType.ArrowClosed, color: "red" } },
  { id: "e9", source: "vk-pd", target: "vk-rd", type: "smoothstep", style: { stroke: "red", strokeDasharray: "5,5" }, markerEnd: { type: MarkerType.ArrowClosed, color: "red" } },
]

export function GoalGraph() {
  return (
    <div style={{ width: "100%", height: "600px" }}>
      <ReactFlow nodes={initialNodes} edges={initialEdges} fitView>
        <Background />
        <Controls />
      </ReactFlow>
    </div>
  )
}
