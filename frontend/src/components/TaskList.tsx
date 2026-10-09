import { useMemo, useState } from "react"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { useTasks, useUpdateTask } from "@/hooks/useTasks"
import {
  TASK_STATUS_LABELS,
  TASK_STATUS_COLORS,
  type Task,
  type TaskStatus,
} from "@/api/tasksApi"
import { Search } from "lucide-react"

interface TaskListProps {
  projectId: string
}

const STATUSES: TaskStatus[] = [
  "NOT_STARTED",
  "IN_PROGRESS",
  "REVIEW",
  "REWORK",
  "DONE",
  "CANCELLED",
]

function isOverdue(task: Task): boolean {
  if (!task.deadline) return false
  if (task.status === "DONE" || task.status === "CANCELLED") return false
  return new Date(task.deadline) < new Date()
}

export function TaskList({ projectId }: TaskListProps) {
  const { data: tasks, isPending, isError, error } = useTasks(projectId)
  const updateMutation = useUpdateTask(projectId)

  const [statusFilter, setStatusFilter] = useState<string>("all")
  const [sectionFilter, setSectionFilter] = useState<string>("all")
  const [search, setSearch] = useState("")
  const [showOverdueOnly, setShowOverdueOnly] = useState(false)

  const sections = useMemo(() => {
    if (!tasks) return []
    const set = new Set<string>()
    tasks.forEach((t) => {
      if (t.section_code) set.add(t.section_code)
    })
    return Array.from(set).sort()
  }, [tasks])

  const filtered = useMemo(() => {
    if (!tasks) return []
    return tasks.filter((t) => {
      if (statusFilter !== "all" && t.status !== statusFilter) return false
      if (sectionFilter !== "all" && t.section_code !== sectionFilter) return false
      if (showOverdueOnly && !isOverdue(t)) return false
      if (search && !t.title.toLowerCase().includes(search.toLowerCase())) return false
      return true
    })
  }, [tasks, statusFilter, sectionFilter, showOverdueOnly, search])

  const stats = useMemo(() => {
    if (!tasks) return { total: 0, overdue: 0, in_progress: 0, done: 0 }
    return {
      total: tasks.length,
      overdue: tasks.filter(isOverdue).length,
      in_progress: tasks.filter((t) => t.status === "IN_PROGRESS").length,
      done: tasks.filter((t) => t.status === "DONE").length,
    }
  }, [tasks])

  const handleStatusChange = (taskId: string, newStatus: TaskStatus) => {
    updateMutation.mutate({ taskId, payload: { status: newStatus } })
  }

  if (isPending) {
  return <div className="text-muted-foreground py-8">Загрузка задач...</div>
}

  if (isError) {
    return (
      <div className="text-destructive py-8">
        Ошибка загрузки задач: {(error as Error).message}
      </div>
    )
  }

  if (!tasks || tasks.length === 0) {
    return (
      <div className="text-muted-foreground py-8">
        В проекте пока нет задач. Импортируйте Excel.
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Статистика */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="p-3 border rounded-md">
          <div className="text-xs text-muted-foreground">Всего</div>
          <div className="text-2xl font-semibold">{stats.total}</div>
        </div>
        <div className="p-3 border rounded-md">
          <div className="text-xs text-muted-foreground">Просрочено</div>
          <div className="text-2xl font-semibold text-destructive">{stats.overdue}</div>
        </div>
        <div className="p-3 border rounded-md">
          <div className="text-xs text-muted-foreground">В работе</div>
          <div className="text-2xl font-semibold text-blue-600">{stats.in_progress}</div>
        </div>
        <div className="p-3 border rounded-md">
          <div className="text-xs text-muted-foreground">Готово</div>
          <div className="text-2xl font-semibold text-green-600">{stats.done}</div>
        </div>
      </div>

      {/* Фильтры */}
      <div className="flex flex-wrap gap-3 items-center">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Поиск по названию..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-8"
          />
        </div>

        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Статус" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Все статусы</SelectItem>
            {STATUSES.map((s) => (
              <SelectItem key={s} value={s}>
                {TASK_STATUS_LABELS[s]}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={sectionFilter} onValueChange={setSectionFilter}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Раздел" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Все разделы</SelectItem>
            {sections.map((s) => (
              <SelectItem key={s} value={s}>
                {s}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <label className="flex items-center gap-2 text-sm cursor-pointer">
          <input
            type="checkbox"
            checked={showOverdueOnly}
            onChange={(e) => setShowOverdueOnly(e.target.checked)}
            className="h-4 w-4"
          />
          Только просроченные
        </label>
      </div>

      {/* Таблица */}
      <div className="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Название</TableHead>
              <TableHead className="w-[140px]">Раздел</TableHead>
              <TableHead className="w-[140px]">Дедлайн</TableHead>
              <TableHead className="w-[180px]">Статус</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filtered.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center text-muted-foreground py-8">
                  Нет задач по выбранным фильтрам
                </TableCell>
              </TableRow>
            ) : (
              filtered.slice(0, 200).map((task) => (
                <TableRow key={task.id}>
                  <TableCell className="font-medium">{task.title}</TableCell>
                  <TableCell className="text-sm text-muted-foreground">
                    {task.section_code || "—"}
                  </TableCell>
                  <TableCell className="text-sm">
                    {task.deadline ? (
                      <span
                        className={isOverdue(task) ? "text-destructive font-medium" : ""}
                      >
                        {new Date(task.deadline).toLocaleDateString("ru-RU")}
                      </span>
                    ) : (
                      <span className="text-muted-foreground">—</span>
                    )}
                  </TableCell>
                  <TableCell>
                    <Select
                      value={task.status}
                      onValueChange={(v) => handleStatusChange(task.id, v as TaskStatus)}
                    >
                      <SelectTrigger className="h-8">
                        <SelectValue>
                          <span
                            className={`inline-block px-2 py-0.5 rounded text-xs ${TASK_STATUS_COLORS[task.status]}`}
                          >
                            {TASK_STATUS_LABELS[task.status]}
                          </span>
                        </SelectValue>
                      </SelectTrigger>
                      <SelectContent>
                        {STATUSES.map((s) => (
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
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
        {filtered.length > 200 && (
          <div className="p-3 text-center text-sm text-muted-foreground border-t">
            Показано 200 из {filtered.length}. Используйте фильтры для сужения.
          </div>
        )}
      </div>
    </div>
  )
}