import { useState, useEffect } from "react"
import {
  type GoalCreate,
  type GoalUpdate,
  type GoalState,
  type VerificationStatus,
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

const VERIFICATION_LABELS: Record<VerificationStatus, string> = {
  confirmed: "Подтверждена",
  requires_check: "Требуется проверка",
  no_data: "Нет данных",
  not_confirmed: "Не подтверждена",
}

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
  const [schemaJson, setSchemaJson] = useState(() => {
    const fd = initialData as Record<string, unknown> | undefined
    const fs = fd?.field_schema as Record<string, unknown> | undefined
    return fs ? JSON.stringify(fs, null, 2) : ""
  })
  const verificationStatus = (initialData as Record<string, unknown>).verification_status as VerificationStatus | undefined

  // Sync state when initialData changes (edit mode)
  useEffect(() => {
    if (initialData) {
      setFormulation(initialData.formulation ?? "")
      setDeadline(initialData.deadline ?? "")
      setPriority(initialData.priority?.toString() ?? "1")
      setState(initialData.state ?? "plan")
      setSelectedPremises(initialData.premise_ids ?? [])
      setSchemaJson(
        initialData.field_schema ? JSON.stringify(initialData.field_schema, null, 2) : "",
      )
    }
  }, [initialData])

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

    // Convert deadline to ISO format
    const toISODate = (v: string): string | null => {
      if (!v) return null
      if (/^\d{4}-\d{2}-\d{2}$/.test(v)) return v
      const m = v.match(/^(\d{1,2})[.\/](\d{1,2})[.\/](\d{4})$/)
      if (m) {
        const [, day, month, year] = m
        return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`
      }
      return v
    }

    onSubmit({
      formulation: formulation.trim(),
      deadline: toISODate(deadline),
      priority: priority ? Number(priority) : null,
      state,
      premise_ids: selectedPremises,
      field_schema: schemaJson.trim() ? JSON.parse(schemaJson) : undefined,
    } as GoalCreate | GoalUpdate)
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

      <div className="space-y-2">
        <Label>Статус проверки</Label>
        <div className="text-sm text-muted-foreground bg-muted p-2 rounded">
          {verificationStatus
            ? VERIFICATION_LABELS[verificationStatus]
            : "Не проверена"}
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="schema">Schema (JSON, опционально)</Label>
        <textarea
          id="schema"
          value={schemaJson}
          onChange={(e) => setSchemaJson(e.target.value)}
          placeholder='{"deadline": "date"}'
          className="w-full min-h-[60px] rounded-md border border-input bg-background px-3 py-2 text-sm font-mono"
        />
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
