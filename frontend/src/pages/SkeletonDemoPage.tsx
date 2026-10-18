import { useState, useMemo, useRef, useCallback } from "react"
import { useParams, Link } from "react-router-dom"
import {
  ReactFlow,
  Background,
  Controls,
  MarkerType,
  type NodeProps,
} from "@xyflow/react"
import "@xyflow/react/dist/style.css"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Send,
  Bot,
  User,
  Code2,
  GitBranch,
} from "lucide-react"

// ====================================================================
// Типы
// ====================================================================

interface GoalNode {
  id: string
  name: string
}

interface EdgeDef {
  source: string
  target: string
}

interface ChatMessage {
  role: "user" | "system"
  text: string
  timestamp: string
}

interface VersionState {
  version: string
  goals: GoalNode[]
  edges: EdgeDef[]
  chatLog: ChatMessage[]
}

// ====================================================================
// Начальное состояние v1.0 (скелет)
// ====================================================================

const INITIAL_SKELETON: VersionState = {
  version: "v1.0",
  goals: [
    { id: "pd", name: "Сдать ПД" },
    { id: "rd", name: "Сдать РД" },
    { id: "ar-pd", name: "АР (ПД)" },
    { id: "ar-rd", name: "АР (РД)" },
    { id: "kr-pd", name: "КР (ПД)" },
    { id: "kr-rd", name: "КР (РД)" },
    { id: "vk-pd", name: "ВК (ПД)" },
    { id: "vk-rd", name: "ВК (РД)" },
  ],
  edges: [
    { source: "ar-rd", target: "rd" },
    { source: "kr-rd", target: "rd" },
    { source: "vk-rd", target: "rd" },
    { source: "ar-pd", target: "ar-rd" },
    { source: "kr-pd", target: "kr-rd" },
    { source: "vk-pd", target: "vk-rd" },
  ],
  chatLog: [
    {
      role: "system",
      text: "Скелет проекта загружен. 8 целей, 6 связей. Напишите команду для изменения.",
      timestamp: new Date().toISOString(),
    },
  ],
}

// ====================================================================
// Парсер команд (regex, клиент)
// ====================================================================

function parseCommand(input: string, currentGoals: GoalNode[], currentEdges: EdgeDef[]): {
  action: "add" | "remove" | "link" | "rename" | "unknown"
  response: string
  newGoals: GoalNode[]
  newEdges: EdgeDef[]
} {
  const text = input.trim()
  const lower = text.toLowerCase()

  // 1. «добавь [раздел] [АББР]»
  const addMatch = lower.match(/добавь\s+(?:раздел\s+)?([а-яa-z]{2,6})/)
  if (addMatch) {
    const abbr = addMatch[1].toUpperCase()

    const pdId = `${abbr.toLowerCase()}-pd`
    const rdId = `${abbr.toLowerCase()}-rd`

    const existsPd = currentGoals.find((g) => g.id === pdId)
    const existsRd = currentGoals.find((g) => g.id === rdId)

    const newGoals = [...currentGoals]
    const newEdges = [...currentEdges]
    let added = ""

    if (!existsPd) {
      newGoals.push({ id: pdId, name: `${abbr} (ПД)` })
      added += `${abbr} (ПД), `
    }
    if (!existsRd) {
      newGoals.push({ id: rdId, name: `${abbr} (РД)` })
      added += `${abbr} (РД)`
    }

    if (added) {
      // Связать с «Сдать РД»
      if (!existsRd) {
        newEdges.push({ source: rdId, target: "rd" })
      }
      // Связать ПД → РД
      if (!existsPd) {
        newEdges.push({ source: pdId, target: rdId })
      }

      return {
        action: "add",
        response: `✅ Добавлено: ${added}. Связи с «Сдать РД» созданы.`,
        newGoals,
        newEdges,
      }
    }
    return {
      action: "unknown",
      response: `⚠️ ${abbr} (ПД) и ${abbr} (РД) уже есть в скелете.`,
      newGoals: [...currentGoals],
      newEdges: [...currentEdges],
    }
  }

  // 2. «убери [АББР] (из) (ПД|РД)?»
  const removeMatch = lower.match(/убери\s+([а-яa-z]{2,6})(?:\s+из\s+)?(пд|рд)?/)
  if (removeMatch) {
    const abbr = removeMatch[1].toUpperCase()
    const part = removeMatch[2]?.toUpperCase() || null

    const filteredGoals = currentGoals.filter((g) => {
      const idLower = g.id.toLowerCase()
      if (part) {
        return !(idLower.includes(abbr.toLowerCase()) && idLower.includes(part.toLowerCase()))
      }
      return !idLower.includes(abbr.toLowerCase())
    })

    const removed = currentGoals.filter((g) => !filteredGoals.find((fg) => fg.id === g.id))
    const removedNames = removed.map((g) => g.name).join(", ")

    if (removed.length === 0) {
      return {
        action: "unknown",
        response: `⚠️ Цель с аббревиатурой «${abbr}» не найдена.`,
        newGoals: [...currentGoals],
        newEdges: [...currentEdges],
      }
    }

    // Удалить связи с удалёнными целями
    const removedIds = new Set(removed.map((g) => g.id))
    const filteredEdges = currentEdges.filter(
      (e: EdgeDef) => !removedIds.has(e.source) && !removedIds.has(e.target),
    )

    return {
      action: "remove",
      response: `🗑️ Убрано: ${removedNames}. Связи удалены.`,
      newGoals: filteredGoals,
      newEdges: filteredEdges,
    }
  }

  // 3. «свяжи [АББР1] и [АББР2]»
  const linkMatch = lower.match(/свяжи\s+([а-яa-z]{2,6})\s+и\s+([а-яa-z]{2,6})/)
  if (linkMatch) {
    const abbr1 = linkMatch[1].toUpperCase()
    const abbr2 = linkMatch[2].toUpperCase()

    const goal1 = currentGoals.find((g) => g.id.includes(abbr1.toLowerCase()))
    const goal2 = currentGoals.find((g) => g.id.includes(abbr2.toLowerCase()))

    if (!goal1 || !goal2) {
      return {
        action: "unknown",
        response: `⚠️ Одна или обе цели («${abbr1}», «${abbr2}») не найдены.`,
        newGoals: [...currentGoals],
        newEdges: [...currentEdges],
      }
    }

    const existingEdge = currentEdges.find(
      (e: EdgeDef) => (e.source === goal1.id && e.target === goal2.id) ||
             (e.source === goal2.id && e.target === goal1.id),
    )
    if (existingEdge) {
      return {
        action: "unknown",
        response: `⚠️ Связь между «${goal1.name}» и «${goal2.name}» уже существует.`,
        newGoals: [...currentGoals],
        newEdges: [...currentEdges],
      }
    }

    return {
      action: "link",
      response: `🔗 Связано: «${goal1.name}» → «${goal2.name}».`,
      newGoals: [...currentGoals],
      newEdges: [...currentEdges, { source: goal1.id, target: goal2.id }],
    }
  }

  // 4. «переименуй [АББР] в [НАЗВАНИЕ]»
  const renameMatch = lower.match(/переименуй\s+([а-яa-z]{2,6})\s+в\s+(.+)/)
  if (renameMatch) {
    const abbr = renameMatch[1].toUpperCase()
    const newName = renameMatch[2].trim()

    const goal = currentGoals.find((g) => g.id.includes(abbr.toLowerCase()))
    if (!goal) {
      return {
        action: "unknown",
        response: `⚠️ Цель «${abbr}» не найдена.`,
        newGoals: [...currentGoals],
        newEdges: [...currentEdges],
      }
    }

    const renamed = currentGoals.map((g) =>
      g.id === goal.id ? { ...g, name: newName } : g,
    )

    return {
      action: "rename",
      response: `✏️ «${goal.name}» → «${newName}».`,
      newGoals: renamed,
      newEdges: [...currentEdges],
    }
  }

  return {
    action: "unknown",
    response: `❓ Неизвестная команда. Поддерживаются:\n• добавь ЭОМ\n• убери КР из ПД\n• свяжи АР и КР\n• переименуй АР в Архитектура`,
    newGoals: [...currentGoals],
    newEdges: [...currentEdges],
  }
}

// ====================================================================
// Custom React Flow Node
// ====================================================================

function SkeletonNodeComponent(props: NodeProps) {
  const node = props.data as { goal: GoalNode }
  const goal = node.goal

  // Цвет по типу
  let color = "#3b82f6" // default blue
  if (goal.id === "pd" || goal.id === "rd") color = "#8b5cf6" // purple — top-level
  else if (goal.name.includes("(ПД)")) color = "#06b6d4" // cyan
  else if (goal.name.includes("(РД)")) color = "#f59e0b" // amber

  return (
    <div
      className="rounded-lg border-2 px-4 py-3 shadow-sm min-w-[140px] text-center"
      style={{
        background: `${color}15`,
        borderColor: color,
      }}
    >
      <div className="text-sm font-semibold" style={{ color }}>
        {goal.name}
      </div>
      <div className="text-[10px] text-gray-400 mt-1">{goal.id}</div>
    </div>
  )
}

// ====================================================================
// Основной компонент
// ====================================================================

export function SkeletonDemoPage() {
  const { id: projectId } = useParams<{ id: string }>()
  const chatEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  // Состояние: массив версий, текущая версия
  const [versions, setVersions] = useState<VersionState[]>([INITIAL_SKELETON])
  const [currentVersionIndex, setCurrentVersionIndex] = useState(0)
  const [inputValue, setInputValue] = useState("")

  // Текущее состояние
  const current = versions[currentVersionIndex]
  const currentGoals = current.goals
  const currentEdges = current.edges

  // В��числяем узлы и рёбра для React Flow
  const flowNodes = useMemo(() => {
    return currentGoals.map((g, i) => {
      // Позиции: 2 колонки
      const isLeft = i < Math.ceil(currentGoals.length / 2)
      const col = isLeft ? 0 : 1
      const row = isLeft ? i : i - Math.ceil(currentGoals.length / 2)
      return {
        id: g.id,
        type: "skeleton",
        position: { x: 100 + col * 350, y: 80 + row * 100 },
        data: { goal: g },
      }
    })
  }, [currentGoals])

  const flowEdges = useMemo(() => {
    return currentEdges.map((e) => ({
      id: `edge-${e.source}-${e.target}`,
      source: e.source,
      target: e.target,
      type: "smoothstep",
      animated: false,
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: "#6b7280",
      },
      style: { stroke: "#9ca3af", strokeWidth: 1.5 },
    }))
  }, [currentEdges])

  // Отправка команды
  const sendCommand = useCallback(() => {
    const input = inputValue.trim()
    if (!input) return

    const userMsg: ChatMessage = {
      role: "user",
      text: input,
      timestamp: new Date().toISOString(),
    }

    // Парсим команду
    const result = parseCommand(input, currentGoals, currentEdges)

    const systemMsg: ChatMessage = {
      role: "system",
      text: result.response,
      timestamp: new Date().toISOString(),
    }

    // Создаём новую версию
    const newVersion: VersionState = {
      version: `v${(1 + currentVersionIndex + 1).toFixed(0)}.${(currentVersionIndex + 1) % 10}`,
      goals: result.newGoals,
      edges: result.newEdges,
      chatLog: [...current.chatLog, userMsg, systemMsg],
    }

    setVersions((prev) => [...prev, newVersion])
    setCurrentVersionIndex(versions.length)
    setInputValue("")
  }, [inputValue, currentGoals, currentVersionIndex, versions.length])

  // Переключение версии
  const switchVersion = useCallback((index: number) => {
    setCurrentVersionIndex(index)
  }, [])

  // Enter для отправки
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendCommand()
    }
  }, [sendCommand])

  // Скролл чата вниз
  useMemo(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [current.chatLog])

  // Счётчики
  const goalCount = currentGoals.length
  const edgeCount = currentEdges.length

  return (
    <div className="flex flex-col h-screen bg-gray-950 text-white">
      {/* Верхняя панель */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-gray-800 bg-gray-900">
        <div className="flex items-center gap-3">
          <Link to={`/projects/${projectId}`}>
            <Button variant="ghost" size="sm" className="text-gray-400 hover:text-white">← Назад</Button>
          </Link>
          <div className="flex items-center gap-2">
            <Code2 className="h-5 w-5 text-blue-400" />
            <h1 className="text-lg font-bold">Диалоговый скелет</h1>
          </div>
          <Badge variant="outline" className="text-xs text-gray-500">v3 prototype</Badge>
        </div>

        {/* Селектор версий */}
        <div className="flex items-center gap-2">
          <GitBranch className="h-4 w-4 text-gray-500" />
          <div className="flex items-center gap-1">
            {versions.map((v, i) => (
              <button
                key={i}
                className={`px-3 py-1 rounded text-xs font-mono transition-colors ${
                  i === currentVersionIndex
                    ? "bg-blue-600 text-white"
                    : "bg-gray-800 text-gray-400 hover:bg-gray-700"
                }`}
                onClick={() => switchVersion(i)}
              >
                {v.version}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Основная область */}
      <div className="flex flex-1 overflow-hidden">
        {/* Канвас */}
        <div className="flex-1 relative">
          <ReactFlow
            nodes={flowNodes}
            edges={flowEdges}
            nodeTypes={{ skeleton: SkeletonNodeComponent }}
            defaultViewport={{ x: 0, y: 0, zoom: 0.9 }}
            fitView
            fitViewOptions={{ padding: 0.3 }}
            panOnDrag
            zoomOnScroll
          >
            <Background color="#1f2937" gap={24} />
            <Controls
              className="fill-white stroke-white"
            />
          </ReactFlow>

          {/* Overlay: статистика */}
          <div className="absolute top-3 left-3 z-10 flex items-center gap-3 bg-gray-900/90 border border-gray-700 rounded-lg px-3 py-2 text-xs">
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 rounded-full bg-blue-500" />
              <span className="text-gray-400">Цели: </span>
              <span className="text-white font-bold">{goalCount}</span>
            </div>
            <div className="flex items-center gap-1">
              <div className="w-2 h-2 rounded-full bg-gray-500" />
              <span className="text-gray-400">Связи: </span>
              <span className="text-white font-bold">{edgeCount}</span>
            </div>
            <div className="text-gray-500">|</div>
            <div className="text-gray-400">
              Версия: <span className="text-blue-400 font-mono font-bold">{current.version}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Чат-панель (снизу) */}
      <div className="border-t border-gray-800 bg-gray-900">
        {/* История чата */}
        <div className="h-48 overflow-y-auto p-4 space-y-3 border-b border-gray-800">
          {current.chatLog.map((msg, i) => (
            <div key={i} className={`flex items-start gap-2 ${msg.role === "user" ? "justify-end" : ""}`}>
              {msg.role === "system" && (
                <Bot className="h-5 w-5 text-blue-400 flex-shrink-0 mt-0.5" />
              )}
              <div
                className={`max-w-[80%] rounded-lg px-3 py-2 text-sm whitespace-pre-line ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-800 text-gray-200 border border-gray-700"
                }`}
              >
                {msg.text}
              </div>
              {msg.role === "user" && (
                <User className="h-5 w-5 text-gray-400 flex-shrink-0 mt-0.5" />
              )}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        {/* Поле ввода */}
        <div className="flex items-center gap-2 p-3">
          <Input
            ref={inputRef}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Команда: добавь ЭОМ / убери КР / свяжи АР и КР / переименуй АР в ..."
            className="flex-1 bg-gray-800 border-gray-700 text-white placeholder-gray-500 focus:border-blue-500"
          />
          <Button
            size="sm"
            onClick={sendCommand}
            disabled={!inputValue.trim()}
            className="bg-blue-600 hover:bg-blue-700 text-white"
          >
            <Send className="h-4 w-4" />
          </Button>
        </div>

        {/* Подсказки команд */}
        <div className="flex items-center gap-2 px-3 pb-2 text-[10px] text-gray-600">
          <span>Примеры:</span>
          <button
            className="hover:text-blue-400 transition-colors"
            onClick={() => setInputValue("добавь ЭОМ")}
          >
            добавь ЭОМ
          </button>
          <button
            className="hover:text-blue-400 transition-colors"
            onClick={() => setInputValue("убери КР из ПД")}
          >
            убери КР из ПД
          </button>
          <button
            className="hover:text-blue-400 transition-colors"
            onClick={() => setInputValue("свяжи АР и КР")}
          >
            свяжи АР и КР
          </button>
          <button
            className="hover:text-blue-400 transition-colors"
            onClick={() => setInputValue("переименуй АР в Архитектура")}
          >
            переименуй АР в Архитектура
          </button>
        </div>
      </div>
    </div>
  )
}
