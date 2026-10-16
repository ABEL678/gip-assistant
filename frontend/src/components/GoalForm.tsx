import { useState } from "react"
import {
  type GoalCreate,
  type GoalUpdate,
  type GoalState,
} from "@/api/goalApi"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

const STATES: { value: GoalState; label: string }[] = [
  { value: "plan", label: "В плане" },
  { value: "in_progress", label: "В работе" },
  { value: "achieved", label: "Достигнута" },
  { value: "cancelled", label: "Отменена" },
]

const PRIORITIES = [1, 2, 3, 4, 5]

interface GoalFormProps {
  initialData?: GoalCreate | GoalUpdate
  premiseNames?: Map<string, string>
  onSubmit: (data: GoalCreate | GoalUpdate) => void
  onCancel: () => void
  submitLabel?: string
}

export function GoalForm({
  initialData,
  premiseNames = new Map(),
  onSubmit,
  onCancel,
  submitLabel = "Сохранить",
}: GoalFormProps) {
  const [formulation, setFormulation] = useState(initialData?.formulation ?? "")
  const [deadline, setDeadline] = useState(initialData?.deadline ?? "")
  const [priority, setPriority] = useState(initialData?.priority?.toString() ?? "1")
  const [state, setState] = useState<GoalState>(initialData?.state ?? "plan")
  const [selectedPremises, setSelectedPremises] = useState<string[]>(
    initialData?.premise_ids ?? [],
  )

  const togglePremise = (premiseId: string) => {
    setSelectedPremises((prev) =>
      prev.includes(premiseId)
        ? prev.filter((id) => id !== premiseId)
        : [...prev, premiseId],
    )
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!formulation.trim()) return

    onSubmit({
      formulation: formulation.trim(),
      deadline: deadline || null,
      priority: priority ? Number(priority) : null,
      state,
      premise_ids: selectedPremises,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="formulation">Формулировка *</Label>
        <Input
          id="formulation"
          value={formulation}
          onChange={(e) => setFormulation(e.target.value)}
          placeholder="Что нужно достичь"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="deadline">Срок</Label>
        <Input
          id="deadline"
          type="date"
          value={deadline}
          onChange={(e) => setDeadline(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="priority">Приоритет</Label>
          <Select value={priority} onValueChange={setPriority}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {PRIORITIES.map((p) => (
                <SelectItem key={p} value={p.toString()}>
                  {p}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="state">Состояние</Label>
          <Select value={state} onValueChange={(v) => setState(v as GoalState)}>
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {STATES.map((s) => (
                <SelectItem key={s.value} value={s.value}>
                  {s.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="space-y-2">
        <Label>Связанные вводные</Label>
        <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto border rounded-md p-2">
          {Array.from(premiseNames.entries()).map(([id, name]) => (
            <button
              key={id}
              type="button"
              onClick={() => togglePremise(id)}
              className={`px-2 py-1 rounded text-sm border transition-colors ${
                selectedPremises.includes(id)
                  ? "bg-primary text-primary-foreground border-primary"
                  : "bg-background hover:bg-muted"
              }`}
            >
              {name}
            </button>
          ))}
          {premiseNames.size === 0 && (
            <span className="text-sm text-muted-foreground">Нет вводных</span>
          )}
        </div>
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
