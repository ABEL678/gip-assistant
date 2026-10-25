import { useState, useEffect } from "react"
import {
  type Rfi,
  type RfiState,
  type RfiUpdate,
  RFI_STATE_LABELS,
} from "@/api/rfiApi"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

type CauseType = "decision" | "goal"

interface RfiCauseOptions {
  decisions: { id: string; label: string }[]
  goals: { id: string; label: string }[]
}

interface RfiFormProps {
  initialData?: Rfi | null
  causeOptions: RfiCauseOptions
  onSubmit: (payload: RfiUpdate) => void
  onCancel: () => void
  submitting?: boolean
}

export function RfiForm({
  initialData,
  causeOptions,
  onSubmit,
  onCancel,
  submitting = false,
}: RfiFormProps) {
  const [title, setTitle] = useState(initialData?.title ?? "")
  const [causeType, setCauseType] = useState<CauseType>(
    initialData?.rfi_cause_goal_id ? "goal" : "decision",
  )
  const [causeDecisionId, setCauseDecisionId] = useState(
    initialData?.rfi_cause_decision_id ?? "",
  )
  const [causeGoalId, setCauseGoalId] = useState(
    initialData?.rfi_cause_goal_id ?? "",
  )
  const [dueDate, setDueDate] = useState(initialData?.rfi_due_date ?? "")
  const [rfiState, setRfiState] = useState<RfiState>(
    initialData?.rfi_state ?? "open",
  )

  // «Грязные» флаги: в edit в payload попадают только реально изменённые поля.
  const [titleDirty, setTitleDirty] = useState(false)
  const [causeDirty, setCauseDirty] = useState(false)
  const [dueDateDirty, setDueDateDirty] = useState(false)
  const [stateDirty, setStateDirty] = useState(false)

  useEffect(() => {
    if (!initialData) return
    setTitle(initialData.title)
    setCauseType(initialData.rfi_cause_goal_id ? "goal" : "decision")
    setCauseDecisionId(initialData.rfi_cause_decision_id ?? "")
    setCauseGoalId(initialData.rfi_cause_goal_id ?? "")
    setDueDate(initialData.rfi_due_date ?? "")
    setRfiState(initialData.rfi_state)
    setTitleDirty(false)
    setCauseDirty(false)
    setDueDateDirty(false)
    setStateDirty(false)
  }, [initialData])

  const causeLocked =
    (initialData?.rfi_cause_decision_id ?? initialData?.rfi_cause_goal_id ?? null) !== null
  const options = causeType === "decision" ? causeOptions.decisions : causeOptions.goals
  const selectedCauseId = causeType === "decision" ? causeDecisionId : causeGoalId
  const dueDateRequired = !!initialData && initialData.rfi_due_date !== null

  const causeMissing = !initialData && !selectedCauseId
  const dueDateInvalid = dueDateRequired && !dueDate
  const submitDisabled = submitting || !title.trim() || causeMissing || dueDateInvalid

  const handleTitleChange = (value: string) => {
    setTitle(value)
    setTitleDirty(value !== (initialData?.title ?? ""))
  }

  const handleCauseTypeChange = (value: CauseType) => {
    setCauseType(value)
    const initialValue =
      value === "decision"
        ? (initialData?.rfi_cause_decision_id ?? "")
        : (initialData?.rfi_cause_goal_id ?? "")
    const selectedValue = value === "decision" ? causeDecisionId : causeGoalId
    setCauseDirty(selectedValue !== initialValue)
  }

  const handleCauseChange = (value: string) => {
    if (causeType === "decision") {
      setCauseDecisionId(value)
      setCauseDirty(value !== (initialData?.rfi_cause_decision_id ?? ""))
    } else {
      setCauseGoalId(value)
      setCauseDirty(value !== (initialData?.rfi_cause_goal_id ?? ""))
    }
  }

  const handleDueDateChange = (value: string) => {
    setDueDate(value)
    setDueDateDirty(value !== (initialData?.rfi_due_date ?? ""))
  }

  const handleStateChange = (value: string) => {
    const next = value as RfiState
    setRfiState(next)
    setStateDirty(next !== (initialData?.rfi_state ?? "open"))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (submitDisabled) return

    if (!initialData) {
      const payload: RfiUpdate = {
        title: title.trim(),
        rfi_state: rfiState,
      }
      if (dueDate) payload.rfi_due_date = dueDate
      if (causeType === "decision") {
        payload.rfi_cause_decision_id = causeDecisionId
      } else {
        payload.rfi_cause_goal_id = causeGoalId
      }
      onSubmit(payload)
      return
    }

    const payload: RfiUpdate = {}
    if (titleDirty) payload.title = title.trim()
    if (causeDirty) {
      if (causeType === "decision") {
        payload.rfi_cause_decision_id = causeDecisionId
      } else {
        payload.rfi_cause_goal_id = causeGoalId
      }
    }
    if (dueDateDirty && dueDate) payload.rfi_due_date = dueDate
    if (stateDirty) payload.rfi_state = rfiState
    onSubmit(payload)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="rfi-title">Заголовок *</Label>
        <Input
          id="rfi-title"
          value={title}
          onChange={(e) => handleTitleChange(e.target.value)}
          placeholder="Краткая формулировка запроса"
          maxLength={1000}
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="rfi-cause-type">Тип причины</Label>
        <Select
          value={causeType}
          onValueChange={(v) => handleCauseTypeChange(v as CauseType)}
          disabled={causeLocked}
        >
          <SelectTrigger id="rfi-cause-type">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="decision">Решение</SelectItem>
            <SelectItem value="goal">Цель</SelectItem>
          </SelectContent>
        </Select>
        {causeLocked && (
          <p className="text-xs text-muted-foreground">
            Тип причины нельзя изменить: он задан у RFI
          </p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="rfi-cause">Причина *</Label>
        <Select
          value={selectedCauseId}
          onValueChange={handleCauseChange}
          disabled={options.length === 0}
        >
          <SelectTrigger id="rfi-cause">
            <SelectValue
              placeholder={
                causeType === "decision" ? "Выберите решение" : "Выберите цель"
              }
            />
          </SelectTrigger>
          <SelectContent>
            {options.map((option) => (
              <SelectItem key={option.id} value={option.id}>
                {option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {options.length === 0 && (
          <p className="text-xs text-muted-foreground">
            {causeType === "decision"
              ? "Нет доступных решений"
              : "Нет доступных целей"}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="rfi-due-date">Срок RFI</Label>
        <Input
          id="rfi-due-date"
          type="date"
          value={dueDate}
          onChange={(e) => handleDueDateChange(e.target.value)}
        />
        {dueDateRequired && (
          <p className="text-xs text-muted-foreground">
            Срок можно изменить, но не очистить
          </p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="rfi-state">Состояние</Label>
        <Select value={rfiState} onValueChange={handleStateChange}>
          <SelectTrigger id="rfi-state">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {Object.entries(RFI_STATE_LABELS).map(([value, label]) => (
              <SelectItem key={value} value={value}>
                {label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="flex gap-2 justify-end pt-2">
        <Button type="button" variant="outline" onClick={onCancel}>
          Отмена
        </Button>
        <Button type="submit" disabled={submitDisabled}>
          {submitting ? "Сохранение..." : initialData ? "Сохранить" : "Создать"}
        </Button>
      </div>
    </form>
  )
}
