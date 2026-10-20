import { useState, useEffect } from "react"
import {
  type ActionCreate,
  type ActionUpdate,
} from "@/api/actionApi"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Input } from "@/components/ui/input"

interface ActionFormProps {
  initialData?: ActionCreate | ActionUpdate
  projectId: string
  onSubmit: (data: ActionCreate | ActionUpdate) => void
  onCancel: () => void
  submitLabel?: string
  prefillTaskId?: string
}

type ActionState = "plan" | "in_progress" | "done" | "overdue" | "cancelled"

export function ActionForm({
  initialData,
  projectId: _projectId,
  onSubmit,
  onCancel,
  submitLabel = "Сохранить",
  prefillTaskId,
}: ActionFormProps) {
  const [formulation, setFormulation] = useState(
    initialData?.formulation ?? "",
  )
  const [measurableResult, setMeasurableResult] = useState(
    initialData?.measurable_result ?? "",
  )
  const [deadline, setDeadline] = useState(
    initialData?.deadline ?? "",
  )
  const [state, setState] = useState<ActionState>(
    (initialData?.state as ActionState) ?? "plan",
  )
  const [taskId, setTaskId] = useState<string | null>(
    initialData?.task_id ?? prefillTaskId ?? null,
  )

  // Sync state when initialData changes (edit mode)
  useEffect(() => {
    if (initialData) {
      setFormulation(initialData.formulation ?? "")
      setMeasurableResult(initialData.measurable_result ?? "")
      setDeadline(initialData.deadline ?? "")
      setState((initialData.state as ActionState) ?? "plan")
      setTaskId(initialData.task_id ?? null)
    } else if (prefillTaskId) {
      setTaskId(prefillTaskId)
    }
  }, [initialData, prefillTaskId])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!formulation.trim()) return

    onSubmit({
      formulation: formulation.trim(),
      measurable_result: measurableResult || null,
      deadline: deadline || null,
      state,
      task_id: taskId,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="formulation">Формулировка *</Label>
        <Textarea
          id="formulation"
          value={formulation}
          onChange={(e) => setFormulation(e.target.value)}
          placeholder="Краткая формулировка действия"
          required
          className="min-h-[100px]"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="measurable_result">Измеримый результат</Label>
        <Textarea
          id="measurable_result"
          value={measurableResult}
          onChange={(e) => setMeasurableResult(e.target.value)}
          placeholder="Как будет измеряться результат?"
          className="min-h-[80px]"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="deadline">Дедлайн</Label>
        <Input
          id="deadline"
          type="date"
          value={deadline}
          onChange={(e) => setDeadline(e.target.value)}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="state">Состояние</Label>
        <Select value={state} onValueChange={(v) => setState(v as ActionState)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="plan">План</SelectItem>
            <SelectItem value="in_progress">В работе</SelectItem>
            <SelectItem value="done">Готово</SelectItem>
            <SelectItem value="overdue">Просрочено</SelectItem>
            <SelectItem value="cancelled">Отменено</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="flex gap-2 justify-end pt-2">
        <Button type="button" variant="outline" onClick={onCancel}>
          Отмена
        </Button>
        <Button type="submit" disabled={!formulation.trim()}>
          {submitLabel}
        </Button>
      </div>
    </form>
  )
}
