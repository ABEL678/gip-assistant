import { useState, useMemo } from "react"
import { useParams, Link } from "react-router-dom"
import { Card, CardContent, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Calendar, Clock, AlertCircle, XCircle } from "lucide-react"

// ====== Моковые данные ======

interface TimelineGoal {
  id: string
  formulation: string
  deadline: string | null
  state: string
  priority: number | null
}

const MOCK_GOALS: TimelineGoal[] = [
  {
    id: "goal-1",
    formulation: "Сдать том 7 в экспертизу",
    deadline: "2026-10-10",
    state: "in_progress",
    priority: 1,
  },
  {
    id: "goal-2",
    formulation: "Получить ИД по нагрузкам",
    deadline: "2026-10-17",
    state: "in_progress",
    priority: 1,
  },
  {
    id: "goal-3",
    formulation: "Передать расчёт ВК на субподряд",
    deadline: "2026-10-24",
    state: "plan",
    priority: 2,
  },
  {
    id: "goal-4",
    formulation: "Согласовать планировку с Заказчиком",
    deadline: "2026-11-15",
    state: "plan",
    priority: 2,
  },
  {
    id: "goal-5",
    formulation: "Финализировать смету",
    deadline: null,
    state: "plan",
    priority: 3,
  },
]

const TODAY = new Date()
TODAY.setHours(0, 0, 0, 0)

// ====== Утилиты (нативные, без date-fns) ======

type DeadlineStatus = "overdue" | "today" | "upcoming" | "far" | "no-deadline"

function parseDate(str: string): Date {
  const [y, m, d] = str.split("-").map(Number)
  return new Date(y, m - 1, d)
}

function isTodayDate(d: Date): boolean {
  return d.getFullYear() === TODAY.getFullYear()
    && d.getMonth() === TODAY.getMonth()
    && d.getDate() === TODAY.getDate()
}

function isPastDate(d: Date): boolean {
  d.setHours(23, 59, 59, 999)
  return d < TODAY
}

function daysBetween(a: Date, b: Date): number {
  const ms = 86400000
  return Math.round((b.getTime() - a.getTime()) / ms)
}

function startOfWeek(date: Date): Date {
  const d = new Date(date)
  const day = d.getDay()
  const diff = (day === 0 ? -6 : 1) - day // понедельник
  d.setDate(d.getDate() - diff)
  d.setHours(0, 0, 0, 0)
  return d
}

function addWeeks(date: Date, weeks: number): Date {
  const d = new Date(date)
  d.setDate(d.getDate() + weeks * 7)
  return d
}

function formatDateRu(date: Date): string {
  const months = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря"
  ]
  const day = date.getDate()
  const month = months[date.getMonth()]
  const year = date.getFullYear()
  return `${day} ${month} ${year}`
}

function formatShortDateRu(date: Date): string {
  const day = date.getDate().toString().padStart(2, "0")
  const months = ["ЯНВ", "ФЕВ", "МАР", "АПР", "МАЙ", "ИЮН", "ИЮЛ", "АВГ", "СЕН", "ОКТ", "НОЯ", "ДЕК"]
  const month = months[date.getMonth()]
  return `${day}.${month}`
}

function getDeadlineStatus(deadline: string | null): DeadlineStatus {
  if (!deadline) return "no-deadline"
  const d = parseDate(deadline)
  if (isTodayDate(d)) return "today"
  if (isPastDate(d)) return "overdue"
  const days = daysBetween(TODAY, d)
  if (days <= 7) return "upcoming"
  return "far"
}

function getBarStyle(status: DeadlineStatus): React.CSSProperties {
  switch (status) {
    case "overdue":
      return {
        background: "linear-gradient(90deg, #ef4444, #dc2626)",
        borderColor: "#b91c1c",
        boxShadow: "0 0 8px rgba(239, 68, 68, 0.4)",
      }
    case "today":
      return {
        background: "linear-gradient(90deg, #fbbf24, #f59e0b)",
        borderColor: "#d97706",
        boxShadow: "0 0 8px rgba(251, 191, 36, 0.4)",
      }
    case "upcoming":
      return {
        background: "linear-gradient(90deg, #3b82f6, #2563eb)",
        borderColor: "#1d4ed8",
      }
    case "far":
      return {
        background: "linear-gradient(90deg, #6366f1, #4f46e5)",
        borderColor: "#4338ca",
      }
    case "no-deadline":
      return {
        background: "repeating-linear-gradient(90deg, #9ca3af, #9ca3af 4px, transparent 4px, transparent 8px)",
        borderColor: "#6b7280",
      }
  }
}

function getStatusBadge(status: DeadlineStatus): { label: string; variant: "destructive" | "default" | "secondary" | "outline" } {
  switch (status) {
    case "overdue":
      return { label: "ПРОСРОЧЕНО", variant: "destructive" }
    case "today":
      return { label: "СЕГОДНЯ", variant: "default" }
    case "upcoming":
      return { label: "Через неделю", variant: "secondary" }
    case "far":
      return { label: "Через месяц", variant: "outline" }
    case "no-deadline":
      return { label: "Без срока", variant: "outline" }
  }
}

function getStatusIcon(status: DeadlineStatus) {
  switch (status) {
    case "overdue":
      return <AlertCircle className="h-4 w-4 text-red-600" />
    case "today":
      return <Clock className="h-4 w-4 text-amber-600" />
    case "no-deadline":
      return <XCircle className="h-4 w-4 text-gray-500" />
    default:
      return <Calendar className="h-4 w-4 text-blue-600" />
  }
}

// ====== Компонент Timeline Bar ======

interface TimelineBarProps {
  goal: TimelineGoal
  timelineStart: Date
  totalWeeks: number
}

function TimelineBar({ goal, timelineStart, totalWeeks }: TimelineBarProps) {
  const status = getDeadlineStatus(goal.deadline)
  const barStyle = getBarStyle(status)

  if (status === "no-deadline") {
    const daysFromStart = daysBetween(timelineStart, TODAY)
    const leftPercent = (daysFromStart / (totalWeeks * 7)) * 100
    return (
      <div
        className="absolute top-1/2 -translate-y-1/2 h-3 w-16 rounded-full"
        style={{
          ...barStyle,
          left: `${leftPercent}%`,
        }}
        title="Без установленного срока"
      />
    )
  }

  const deadlineDate = goal.deadline ? parseDate(goal.deadline) : TODAY
  const daysFromStart = daysBetween(timelineStart, TODAY)
  const daysToEnd = daysBetween(timelineStart, deadlineDate)
  const widthDays = Math.max(daysToEnd - daysFromStart, 7) // минимум 1 неделя

  const leftPercent = (daysFromStart / (totalWeeks * 7)) * 100
  const widthPercent = (widthDays / (totalWeeks * 7)) * 100

  const tooltipText = goal.deadline
    ? `Срок: ${formatDateRu(deadlineDate)}`
    : "Без установленного срока"

  return (
    <div
      className="absolute top-1/2 -translate-y-1/2 h-7 rounded-md cursor-pointer transition-all duration-200 hover:scale-y-125 hover:z-10"
      style={{
        ...barStyle,
        left: `${leftPercent}%`,
        width: `${widthPercent}%`,
        minWidth: "40px",
        border: "1px solid",
      }}
      title={tooltipText}
    />
  )
}

// ====== Основной компонент страницы ======

export function TimelineDemoPage() {
  const { id: projectId } = useParams<{ id: string }>()
  const [hoveredGoalId, setHoveredGoalId] = useState<string | null>(null)

  const timelineWeeks = 12
  const timelineStart = useMemo(() => startOfWeek(TODAY), [])
  const weeks = useMemo(() => {
    const result: { start: Date; label: string }[] = []
    for (let i = 0; i <= timelineWeeks; i++) {
      const d = addWeeks(timelineStart, i)
      result.push({ start: d, label: formatShortDateRu(d) })
    }
    return result
  }, [timelineStart])

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b bg-white">
        <div className="flex items-center gap-3">
          <Link to={`/projects/${projectId}`}>
            <Button variant="ghost" size="sm">← Назад</Button>
          </Link>
          <div>
            <CardTitle className="text-xl">Timeline — Цели проекта</CardTitle>
            <CardDescription>Демо-прототип оси времени (Asana Timeline style)</CardDescription>
          </div>
        </div>
        <Badge variant="outline" className="text-xs">v0.1 prototype</Badge>
      </div>

      {/* Timeline Area */}
      <div className="flex-1 overflow-auto p-6">
        <Card className="shadow-lg">
          <CardContent className="p-0">
            <div className="flex min-w-[800px]">
              {/* Left: Goal List */}
              <div className="w-72 flex-shrink-0 border-r bg-white p-4">
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Цели</h3>
                <div className="space-y-1">
                  {MOCK_GOALS.map((goal) => {
                    const status = getDeadlineStatus(goal.deadline)
                    const badge = getStatusBadge(status)
                    const isHovered = hoveredGoalId === goal.id
                    return (
                      <div
                        key={goal.id}
                        className={`flex items-center gap-2 px-3 py-2 rounded-lg transition-colors cursor-pointer ${
                          isHovered ? "bg-gray-100" : ""
                        }`}
                        onMouseEnter={() => setHoveredGoalId(goal.id)}
                        onMouseLeave={() => setHoveredGoalId(null)}
                      >
                        {getStatusIcon(status)}
                        <div className="flex-1 min-w-0">
                          <div className={`text-sm font-medium truncate ${
                            status === "overdue" ? "text-red-700" : ""
                          }`}>
                            {goal.formulation}
                          </div>
                          {goal.deadline && (
                            <div className="text-xs text-gray-500">
                              до {parseDate(goal.deadline).getDate().toString().padStart(2, "0")}.{(parseDate(goal.deadline).getMonth() + 1).toString().padStart(2, "0")}
                            </div>
                          )}
                        </div>
                        <Badge
                          variant={badge.variant}
                          className="text-xs flex-shrink-0"
                        >
                          {badge.label}
                        </Badge>
                      </div>
                    )
                  })}
                </div>
              </div>

              {/* Right: Timeline Bars */}
              <div className="flex-1 overflow-x-auto">
                <div style={{ minWidth: `${timelineWeeks * 120}px` }}>
                  {/* Week Headers */}
                  <div className="flex border-b sticky top-0 bg-white z-10">
                    {weeks.map((week, i) => (
                      <div
                        key={i}
                        className="flex-1 text-xs font-medium text-gray-500 px-2 py-2 border-l"
                        style={{ minWidth: "120px" }}
                      >
                        {week.label}
                      </div>
                    ))}
                  </div>

                  {/* Today Marker */}
                  <div className="relative h-8 border-b bg-amber-50/30">
                    <div
                      className="absolute top-0 bottom-0 w-px bg-amber-400 z-10"
                      style={{ left: "0%" }}
                    >
                      <div className="absolute -top-1 -translate-x-1/2 bg-amber-400 text-amber-900 text-[10px] font-bold px-1 rounded">
                        СЕГОДНЯ
                      </div>
                    </div>
                  </div>

                  {/* Goal Bars */}
                  <div className="relative">
                    {/* Grid Lines */}
                    <div className="absolute inset-0 flex pointer-events-none">
                      {weeks.map((_, i) => (
                        <div
                          key={i}
                          className="flex-1 border-l border-gray-100"
                          style={{ minWidth: "120px" }}
                        />
                      ))}
                    </div>

                    {/* Bars */}
                    <div className="relative py-3">
                      {MOCK_GOALS.map((goal) => (
                        <div
                          key={goal.id}
                          className="relative h-10 flex items-center"
                          onMouseEnter={() => setHoveredGoalId(goal.id)}
                          onMouseLeave={() => setHoveredGoalId(null)}
                        >
                          <TimelineBar
                            goal={goal}
                            timelineStart={timelineStart}
                            totalWeeks={timelineWeeks}
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Legend */}
      <div className="px-6 py-3 border-t bg-white flex items-center gap-6 text-xs text-gray-600">
        <span className="font-semibold">Легенда:</span>
        <div className="flex items-center gap-2">
          <div className="w-4 h-3 rounded" style={{ background: "linear-gradient(90deg, #ef4444, #dc2626)" }} />
          <span>Просрочено</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-3 rounded" style={{ background: "linear-gradient(90deg, #fbbf24, #f59e0b)" }} />
          <span>Сегодня</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-3 rounded" style={{ background: "linear-gradient(90deg, #3b82f6, #2563eb)" }} />
          <span>Ближайшие (≤7 дней)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-3 rounded" style={{ background: "linear-gradient(90deg, #6366f1, #4f46e5)" }} />
          <span>Дальние (&gt;7 дней)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-3 rounded" style={{ background: "repeating-linear-gradient(90deg, #9ca3af, #9ca3af 4px, transparent 4px, transparent 8px)" }} />
          <span>Без срока</span>
        </div>
      </div>
    </div>
  )
}
