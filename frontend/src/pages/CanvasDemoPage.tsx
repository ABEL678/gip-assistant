import { useState } from "react"
import { ReactFlow, Background, Controls, Position, MarkerType } from "@xyflow/react"
import "@xyflow/react/dist/style.css"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { FileText, Plus, RefreshCw, ClipboardPaste } from "lucide-react"

// ====================================================================
// Мок-договор
// ====================================================================

const MOCK_CONTRACT = `Договор №1. Разработка проектной и рабочей документации.
Состав: ПД, РД.
Разделы: АР, КР, ВК, ЭОМ.
Сроки: ПД — до 01.03.2027, РД — до 01.09.2027.`

// ====================================================================
// Парсер: извлекает разделы из текста
// ====================================================================

function parseSections(text: string): string[] {
  const match = text.match(/Разделы[：:\s]+([^\n]+)/i)
  if (!match) return ["АР", "КР", "ВК", "ЭОМ"] // fallback

  return match[1]
    .split(/[,\s]+/)
    .map((s) => s.trim())
    .filter((s) => /^[А-ЯA-Z]{2,6}$/.test(s))
}

// ====================================================================
// Генерация графа: жёсткая структура
//
// Всегда:
//   - 2 корня: goal-pd ("Сдать ПД"), goal-rd ("Сдать РД")
//   - Для каждого раздела X: x-pd, x-rd
//
// Связи:
//   goal-pd → x-pd
//   goal-rd → x-rd
//   x-pd → x-rd (красный пунктир)
// ====================================================================

function buildGraph(sections: string[]) {
  const nodes: Array<{
    id: string
    position: { x: number; y: number }
    data: { label: string; type: "submit" | "section-pd" | "section-rd" }
    sourcePosition: Position
    targetPosition: Position
  }> = [
    // === Корни (левая колонка) ===
    {
      id: "goal-pd",
      position: { x: 100, y: 100 },
      data: { label: "Сдать ПД", type: "submit" as const },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    },
    {
      id: "goal-rd",
      position: { x: 100, y: 450 },
      data: { label: "Сдать РД", type: "submit" as const },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    },
  ]

  const edges: Array<{
    id: string
    source: string
    target: string
    type: "smoothstep"
    style?: React.CSSProperties
    markerEnd?: { type: MarkerType; color?: string }
  }> = []

  let rightY = 50
  const sectionIds: { pd: string; rd: string }[] = []

  // === Узлы разделов ПД (правая колонка, верх) ===
  for (const section of sections) {
    const id = `${section.toLowerCase()}-pd`
    nodes.push({
      id,
      position: { x: 500, y: rightY },
      data: { label: `${section} (ПД)`, type: "section-pd" as const },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    })
    sectionIds.push({ pd: id, rd: "" }) // rd заполним ниже
    rightY += 90
  }

  rightY = 50
  // === Узлы разделов РД (правая колонка, низ) ===
  for (const section of sections) {
    const id = `${section.toLowerCase()}-rd`
    nodes.push({
      id,
      position: { x: 500, y: rightY },
      data: { label: `${section} (РД)`, type: "section-rd" as const },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    })
    // Связываем pd ↔ rd
    const pdIndex = sections.indexOf(section)
    if (pdIndex >= 0) sectionIds[pdIndex].rd = id
    rightY += 90
  }

  // === Связи: goal-pd → x-pd ===
  for (const section of sections) {
    const pdId = `${section.toLowerCase()}-pd`
    edges.push({
      id: `e-goal-pd-${pdId}`,
      source: "goal-pd",
      target: pdId,
      type: "smoothstep",
      markerEnd: { type: MarkerType.ArrowClosed },
    })
  }

  // === Связи: goal-rd → x-rd ===
  for (const section of sections) {
    const rdId = `${section.toLowerCase()}-rd`
    edges.push({
      id: `e-goal-rd-${rdId}`,
      source: "goal-rd",
      target: rdId,
      type: "smoothstep",
      markerEnd: { type: MarkerType.ArrowClosed },
    })
  }

  // === Связи: x-pd → x-rd (красный пунктир) ===
  for (const { pd, rd } of sectionIds) {
    if (pd && rd) {
      edges.push({
        id: `e-${pd}-${rd}`,
        source: pd,
        target: rd,
        type: "smoothstep",
        style: { stroke: "#ef4444", strokeDasharray: "5,5" },
        markerEnd: { type: MarkerType.ArrowClosed, color: "#ef4444" },
      })
    }
  }

  return { nodes, edges }
}

// ====================================================================
// Custom React Flow Node
// ====================================================================

function GraphNodeComponent(props: {
  data: { label: string; type: "submit" | "section-pd" | "section-rd" }
}) {
  const { label, type } = props.data

  let bgColor = "bg-white"
  let borderColor = "border-gray-300"
  let textColor = "text-gray-800"
  let badgeColor = ""

  if (type === "submit") {
    bgColor = "bg-blue-50"
    borderColor = "border-blue-400"
    textColor = "text-blue-900"
  } else if (type === "section-pd") {
    bgColor = "bg-blue-50"
    borderColor = "border-blue-300"
    textColor = "text-blue-800"
    badgeColor = "bg-blue-500 text-white"
  } else if (type === "section-rd") {
    bgColor = "bg-orange-50"
    borderColor = "border-orange-300"
    textColor = "text-orange-800"
    badgeColor = "bg-orange-500 text-white"
  }

  return (
    <div
      className={`rounded-lg border-2 ${bgColor} ${borderColor} px-4 py-3 shadow-sm min-w-[140px]`}
    >
      <div className={`text-sm font-semibold ${textColor}`}>{label}</div>
      {type !== "submit" && (
        <span
          className={`mt-1 inline-block rounded-full px-2 py-0.5 text-[10px] font-medium ${badgeColor}`}
        >
          {type === "section-pd" ? "ПД" : "РД"}
        </span>
      )}
    </div>
  )
}

// ====================================================================
// Основной компонент
// ====================================================================

export function GoalGraph() {
  const [showEditor, setShowEditor] = useState(false)
  const [contractText, setContractText] = useState("")
  const [graphData, setGraphData] = useState<{
    nodes: Array<{
      id: string
      position: { x: number; y: number }
      data: { label: string; type: "submit" | "section-pd" | "section-rd" }
      sourcePosition: Position
      targetPosition: Position
    }>
    edges: Array<{
      id: string
      source: string
      target: string
      type: "smoothstep"
      style?: React.CSSProperties
      markerEnd?: { type: MarkerType; color?: string }
    }>
  } | null>(null)

  const handleUseMock = () => {
    setContractText(MOCK_CONTRACT)
  }

  const handleBuild = () => {
    const text = contractText || MOCK_CONTRACT
    const sections = parseSections(text)
    const graph = buildGraph(sections)
    setGraphData(graph)
    setShowEditor(false)
  }

  const handleReset = () => {
    setContractText("")
    setGraphData(null)
    setShowEditor(false)
  }

  const nodeCount = graphData?.nodes.length ?? 0
  const edgeCount = graphData?.edges.length ?? 0

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Верхняя панель */}
      <div className="flex items-center justify-between px-4 py-2 border-b bg-white">
        <div className="flex items-center gap-3">
          <FileText className="h-5 w-5 text-blue-600" />
          <h1 className="text-lg font-bold">Скелет из договора</h1>
          {graphData && (
            <span className="text-xs text-gray-400">
              {nodeCount} узлов · {edgeCount} связей
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          {!showEditor && !graphData && (
            <Button size="sm" onClick={() => setShowEditor(true)}>
              <Plus className="h-3 w-3 mr-1" />
              Загрузить договор
            </Button>
          )}
          {showEditor && (
            <>
              <Button size="sm" variant="outline" onClick={handleUseMock}>
                <ClipboardPaste className="h-3 w-3 mr-1" />
                Мок-договор
              </Button>
              <Button size="sm" variant="outline" onClick={() => setShowEditor(false)}>
                Отмена
              </Button>
              <Button size="sm" onClick={handleBuild}>
                Построить
              </Button>
            </>
          )}
          {graphData && (
            <Button size="sm" variant="outline" onClick={handleReset}>
              <RefreshCw className="h-3 w-3 mr-1" />
              Сброс
            </Button>
          )}
        </div>
      </div>

      {/* Редактор договора */}
      {showEditor && (
        <div className="border-b bg-gray-50 p-4">
          <div className="max-w-3xl mx-auto space-y-3">
            <div className="text-sm font-medium text-gray-700">Текст договора:</div>
            <Textarea
              value={contractText}
              onChange={(e) => setContractText(e.target.value)}
              onPaste={() => {}}
              data-gramm="false"
              data-gramm_editor="false"
              data-enable-grammarly="false"
              placeholder="Вставьте текст договора или нажмите «Мок-договор»..."
              className="min-h-[200px] font-mono text-sm"
            />
            <div className="text-xs text-gray-400">
              Поддерживается вставка (Ctrl+V). Граммари — игнорируется.
            </div>
          </div>
        </div>
      )}

      {/* Канвас */}
      <div className="flex-1 relative">
        {!graphData && !showEditor && (
          <div className="flex items-center justify-center h-full text-gray-400">
            <div className="text-center">
              <FileText className="h-12 w-12 mx-auto mb-3 opacity-30" />
              <div className="text-sm">Нажмите «Загрузить договор» для начала</div>
            </div>
          </div>
        )}

        {graphData && (
          <div style={{ width: "100%", height: "600px" }}>
            <ReactFlow
              nodes={graphData.nodes}
              edges={graphData.edges}
              nodeTypes={{
                default: GraphNodeComponent,
              }}
              fitView
              fitViewOptions={{ padding: 0.3 }}
              minZoom={0.3}
              maxZoom={2}
            >
              <Background color="#e5e7eb" gap={16} />
              <Controls />
            </ReactFlow>
          </div>
        )}
      </div>
    </div>
  )
}
