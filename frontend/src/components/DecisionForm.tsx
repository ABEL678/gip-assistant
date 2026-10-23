import { useState, useEffect } from "react"
import {
  type DecisionCreate,
  type DecisionUpdate,
  type DecisionState,
  DECISION_STATE_LABELS,
} from "@/api/decisionApi"
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

interface DecisionFormProps {
  initialData?: DecisionCreate | DecisionUpdate
  projectId: string
  onSubmit: (data: DecisionCreate | DecisionUpdate) => void
  onCancel: () => void
  submitLabel?: string
}

export function DecisionForm({
  initialData,
  projectId: _projectId,
  onSubmit,
  onCancel,
  submitLabel = "Сохранить",
}: DecisionFormProps) {
  const [formulation, setFormulation] = useState(
    initialData?.formulation ?? "",
  )
  const [rationale, setRationale] = useState(
    initialData?.rationale ?? "",
  )
  const [context, setContext] = useState(
    initialData?.context ?? "",
  )
  const [deadline, setDeadline] = useState(
    initialData?.deadline ?? "",
  )
  const [state, setState] = useState<DecisionState>(
    (initialData?.state as DecisionState) ?? "plan",
  )

  useEffect(() => {
    if (initialData) {
      setFormulation(initialData.formulation ?? "")
      setRationale(initialData.rationale ?? "")
      setContext(initialData.context ?? "")
      setDeadline(initialData.deadline ?? "")
      setState((initialData.state as DecisionState) ?? "plan")
    }
  }, [initialData])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!formulation.trim()) return

    onSubmit({
      formulation: formulation.trim(),
      rationale: rationale || null,
      context: context || null,
      deadline: deadline || null,
      state,
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
          placeholder="Краткая формулировка решения"
          required
          className="min-h-[100px]"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="rationale">Обоснование</Label>
        <Textarea
          id="rationale"
          value={rationale}
          onChange={(e) => setRationale(e.target.value)}
          placeholder="Почему это решение верно?"
          className="min-h-[80px]"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="context">Контекст</Label>
        <Textarea
          id="context"
          value={context}
          onChange={(e) => setContext(e.target.value)}
          placeholder="Дополнительный контекст"
          className="min-h-[60px]"
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
        <Select value={state} onValueChange={(v) => setState(v as DecisionState)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {Object.entries(DECISION_STATE_LABELS).map(([value, label]) => (
              <SelectItem key={value} value={value}>{label}</SelectItem>
            ))}
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
