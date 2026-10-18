import { useState } from "react"
import { ReactFlow, Background, Controls, Position, MarkerType } from "@xyflow/react"
import "@xyflow/react/dist/style.css"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { FileText, Plus, RefreshCw } from "lucide-react"

// ====================================================================
// Мок-договор (константа)
// ====================================================================

const MOCK_CONTRACT = `Договор №1. Разработка проектной и рабочей документации.
Состав: ПД, РД.
Разделы: АР, КР, ВК, ЭОМ.
Логика парсинга (простая, regex)
Если в тексте есть «ПД» → добавить узел «Сдать ПД».

Если есть «РД» → добавить «Сдать РД».

Если есть «Разделы: …» → для каждого раздела добавить:

«X (ПД)» (если ПД есть).

«X (РД)» (если РД есть).

Связи:

«Сдать ПД» → «X (ПД)».

«Сдать РД» → «X (РД)».

«X (ПД)» → «X (РД)» (красный пунктир).

UI
Сверху: кнопка «Загрузить договор» (открывает textarea с мок-текстом).

После нажатии «Построить» — граф строится из текста.

Кнопка «Сброс» — очищает.

Цвета: ПД — синий бейдж, РД — оранжевый.`

// ====================================================================
// Парсер договора
// ====================================================================

interface ParsedContract {
  hasPd: boolean
  hasRd: boolean
  sections: string[]
}

function parseContract(text: string): ParsedContract {
  const hasPd = /ПД|проектная документации/.test(text)
  const hasRd = /РД|рабочая документация/.test(text)

  // Ищем разделы после "Разделы:"
  const sectionsMatch = text.match(/Разделы[：:]\s*([^\n]+)/)
  const sections: string[] = []
  if (sectionsMatch) {
    sections.push(
      ...sectionsMatch[1]
        .split(/[,\s]+/)
        .map((s) => s.trim())
        .filter((s) => s.length > 0 && s.length < 20),
    )
  }

  return { hasPd, hasRd, sections }
}

// ====================================================================
// Генерация графа из парсенных данных
// ====================================================================

interface GraphData {
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
}

function buildGraph(parsed: ParsedContract): GraphData {
  const nodes: GraphData["nodes"] = []
  const edges: GraphData["edges"] = []

  // Левая колонка: "Сдать ПД" / "Сдать РД"
  let leftY = 80
  if (parsed.hasPd) {
    nodes.push({
      id: "submit-pd",
      position: { x: 100, y: leftY },
      data: { label: "Сдать ПД", type: "submit" },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    })
    leftY += 120
  }
  if (parsed.hasRd) {
    nodes.push({
      id: "submit-rd",
      position: { x: 100, y: leftY },
      data: { label: "Сдать РД", type: "submit" },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    })
  }

  // Правая колонка: разделы
  const rightNodes: { id: string; label: string; type: "section-pd" | "section-rd" }[] = []
  let rightY = 50

  if (parsed.hasPd && parsed.sections.length > 0) {
    for (const section of parsed.sections) {
      const id = `sec-pd-${section.toLowerCase()}`
      const label = `${section} (ПД)`
      nodes.push({
        id,
        position: { x: 500, y: rightY },
        data: { label, type: "section-pd" },
        sourcePosition: Position.Right,
        targetPosition: Position.Left,
      })
      rightNodes.push({ id, label, type: "section-pd" })
      rightY += 90
    }
  }

  rightY = 50
  if (parsed.hasRd && parsed.sections.length > 0) {
    for (const section of parsed.sections) {
      const id = `sec-rd-${section.toLowerCase()}`
      const label = `${section} (РД)`
      nodes.push({
        id,
        position: { x: 500, y: rightY },
        data: { label, type: "section-rd" },
        sourcePosition: Position.Right,
        targetPosition: Position.Left,
      })
      rightNodes.push({ id, label, type: "section-rd" })
      rightY += 90
    }
  }

  // Связи: Сдать ПД → X (ПД)
  if (parsed.hasPd) {
    const submitPd = nodes.find((n) => n.id === "submit-pd")
    if (submitPd) {
      for (const section of parsed.sections) {
        const target = nodes.find((n) => n.id === `sec-pd-${section.toLowerCase()}`)
        if (target) {
          edges.push({
            id: `e-${submitPd.id}-${target.id}`,
            source: submitPd.id,
            target: target.id,
            type: "smoothstep",
            markerEnd: { type: MarkerType.ArrowClosed },
          })
        }
      }
    }
  }

  // Связи: Сдать РД → X (РД)
  if (parsed.hasRd) {
    const submitRd = nodes.find((n) => n.id === "submit-rd")
    if (submitRd) {
      for (const section of parsed.sections) {
        const target = nodes.find((n) => n.id === `sec-rd-${section.toLowerCase()}`)
        if (target) {
          edges.push({
            id: `e-${submitRd.id}-${target.id}`,
            source: submitRd.id,
            target: target.id,
            type: "smoothstep",
            markerEnd: { type: MarkerType.ArrowClosed },
          })
        }
      }
    }
  }

  // Связи: X (ПД) → X (РД) — красные пунктирные
  if (parsed.hasPd && parsed.hasRd) {
    for (const section of parsed.sections) {
      const pdNode = nodes.find((n) => n.id === `sec-pd-${section.toLowerCase()}`)
      const rdNode = nodes.find((n) => n.id === `sec-rd-${section.toLowerCase()}`)
      if (pdNode && rdNode) {
        edges.push({
          id: `e-${pdNode.id}-${rdNode.id}`,
          source: pdNode.id,
          target: rdNode.id,
          type: "smoothstep",
          style: { stroke: "#ef4444", strokeDasharray: "5,5" },
          markerEnd: { type: MarkerType.ArrowClosed, color: "#ef4444" },
        })
      }
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
  const [graphData, setGraphData] = useState<GraphData | null>(null)

  const handleBuild = () => {
    const text = contractText || MOCK_CONTRACT
    const parsed = parseContract(text)
    const graph = buildGraph(parsed)
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
            <div className="text-sm font-medium text-gray-700">Текст договора (мок):</div>
            <Textarea
              value={contractText}
              onChange={(e) => setContractText(e.target.value)}
              placeholder="Вставьте текст договора или используйте мок по умолчанию..."
              className="min-h-[200px] font-mono text-sm"
            />
            <div className="text-xs text-gray-400">
              Или нажмите «Построить» без текста — будет использован мок-договор.
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
