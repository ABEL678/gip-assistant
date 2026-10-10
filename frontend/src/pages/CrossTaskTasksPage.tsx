import { useMemo, useState } from "react"
import { useParams, Link } from "react-router-dom"
import { ArrowLeft, ChevronDown, ChevronRight } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useCrossTaskTasks, useMatrix } from "@/hooks/useMatrix"
import { useUpdateTask } from "@/hooks/useTasks"
import {
  TASK_STATUS_LABELS,
  TASK_STATUS_COLORS,
  type TaskStatus,
} from "@/api/tasksApi"
import type { CrossTaskTask } from "@/api/matrixApi"

const ALL_STATUSES: TaskStatus[] = [
  "NOT_STARTED",
  "IN_PROGRESS",
  "REVIEW",
  "REWORK",
  "DONE",
  "CANCELLED",
]

interface TaskGroup {
  key: string
  label: string
  colorClass: string
  tasks: CrossTaskTask[]
  defaultOpen: boolean
}

export function CrossTaskTasksPage() {
  const { id: projectId, crossTaskId } = useParams<{
    id: string
    crossTaskId: string
  }>()

  const { data: crossTasks } = useMatrix(projectId!)
  const { data: tasks, isLoading, isError, error } = useCrossTaskTasks(
    crossTaskId || null,
  )
  const updateMutation = useUpdateTask(projectId!)

  const crossTask = crossTasks?.find((ct) => ct.id === crossTaskId)

  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({})

  const groups: TaskGroup[] = useMemo(() => {
    if (!tasks) return []
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    const overdue = tasks.filter(
      (t) => t.overdue_days > 0 && t.status !== "DONE" && t.status !== "CANCELLED",
    )
    const soon = tasks.filter(
      (t) =>
        t.days_until_deadline !== null &&
        t.days_until_deadline >= 0 &&
        t.days_until_deadline <= 7 &&
        t.status !== "DONE" &&
        t.status !== "CANCELLED",
    )
    const inProgress = tasks.filter(
      (t) =>
        t.status === "IN_PROGRESS" &&
        t.overdue_days === 0 &&
        !soon.includes(t),
    )
    const notStarted = tasks.filter(
      (t) =>
        t.status === "NOT_STARTED" &&
        t.overdue_days === 0 &&
        !soon.includes(t),
    )
    const done = tasks.filter(
      (t) => t.status === "DONE" || t.status === "CANCELLED",
    )

    return [
      {
        key: "overdue",
        label: "Просрочено",
        colorClass: "text-red-600",
        tasks: overdue.sort((a, b) => b.overdue_days - a.overdue_days),
        defaultOpen: true,
      },
      {
        key: "soon",
        label: "Скоро дедлайн (≤7 дней)",
        colorClass: "text-yellow-600",
        tasks: soon.sort(
          (a, b) => (a.days_until_deadline ?? 0) - (b.days_until_deadline ?? 0),
        ),
        defaultOpen: true,
      },
      {
        key: "inProgress",
        label: "В работе",
        colorClass: "text-blue-600",
        tasks: inProgress,
        defaultOpen: false,
      },
      {
        key: "notStarted",
        label: "Не начато",
        colorClass: "text-muted-foreground",
        tasks: notStarted,
        defaultOpen: false,
      },
      {
        key: "done",
        label: "Готово / Отменено",
        colorClass: "text-green-600",
        tasks: done,
        defaultOpen: false,
      },
    ].filter((g) => g.tasks.length > 0)
  }, [tasks])

  if (isLoading) {
    return <div className="text-muted-foreground">Загрузка задач...</div>
  }

  if (isError) {
    return <div className="text-destructive">Ошибка: {(error as Error).message}</div>
  }

  const totalOverdue = tasks?.filter((t) => t.overdue_days > 0 && t.status !== "DONE").length || 0

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link to={`/projects/${projectId}/matrix`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-2xl font-bold">
            {crossTask
              ? `${crossTask.from_section_code} → ${crossTask.to_section_code}`
              : "Задачи пары"}
          </h1>
          <p className="text-sm text-muted-foreground">
            {tasks?.length || 0} задач · {totalOverdue} просрочено
          </p>
        </div>
      </div>

      {groups.map((group) => {
        const isOpen = !collapsed[group.key]
        return (
          <Card key={group.key}>
            <CardHeader
              className="cursor-pointer select-none"
              onClick={() =>
                setCollapsed((prev) => ({ ...prev, [group.key]: !prev[group.key] }))
              }
            >
              <CardTitle className={`text-base flex items-center gap-2 ${group.colorClass}`}>
                {isOpen ? (
                  <ChevronDown className="h-4 w-4" />
                ) : (
                  <ChevronRight className="h-4 w-4" />
                )}
                {group.label} ({group.tasks.length})
              </CardTitle>
            </CardHeader>
            {isOpen && (
              <CardContent className="p-0">
                <div className="divide-y">
                  {group.tasks.map((task) => (
                    <TaskRow
                      key={task.id}
                      task={task}
                      onChangeStatus={(status) =>
                        updateMutation.mutate({
                          taskId: task.id,
                          payload: { status },
                        })
                      }
                    />
                  ))}
                </div>
              </CardContent>
            )}
          </Card>
        )
      })}

      {groups.length === 0 && (
        <Card>
          <CardContent className="py-12 text-center text-muted-foreground">
            У этой пары нет задач.
          </CardContent>
        </Card>
      )}
    </div>
  )
}

function TaskRow({
  task,
  onChangeStatus,
}: {
  task: CrossTaskTask
  onChangeStatus: (status: TaskStatus) => void
}) {
  const overdueLabel =
    task.overdue_days > 0
      ? `${task.overdue_days} дн. просрочки`
      : task.days_until_deadline !== null && task.days_until_deadline >= 0
        ? `${task.days_until_deadline} дн. до срока`
        : ""

  return (
    <div className="flex items-start gap-4 p-4 hover:bg-muted/30">
      <div className="flex-1 min-w-0">
        <div className="font-medium">{task.title}</div>
        <div className="flex flex-wrap items-center gap-3 mt-1 text-xs text-muted-foreground">
          {task.deadline && (
            <span>
              Срок:{" "}
              {new Date(task.deadline).toLocaleDateString("ru-RU")}
            </span>
          )}
          {overdueLabel && (
            <span
              className={
                task.overdue_days > 0 ? "text-destructive font-medium" : ""
              }
            >
              {overdueLabel}
            </span>
          )}
        </div>
      </div>
      <div className="w-[180px] flex-shrink-0">
        <Select
          value={task.status}
          onValueChange={(v) => onChangeStatus(v as TaskStatus)}
        >
          <SelectTrigger className="h-8">
            <SelectValue>
              <span
                className={`inline-block px-2 py-0.5 rounded text-xs ${
                  TASK_STATUS_COLORS[task.status as TaskStatus] || ""
                }`}
              >
                {TASK_STATUS_LABELS[task.status as TaskStatus] || task.status}
              </span>
            </SelectValue>
          </SelectTrigger>
          <SelectContent>
            {ALL_STATUSES.map((s) => (
              <SelectItem key={s} value={s}>
                <span
                  className={`inline-block px-2 py-0.5 rounded text-xs ${TASK_STATUS_COLORS[s]}`}
                >
                  {TASK_STATUS_LABELS[s]}
                </span>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  )
}