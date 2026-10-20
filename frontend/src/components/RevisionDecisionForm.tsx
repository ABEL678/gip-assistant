import { useState, useEffect } from "react"
import { type Change, type RevisionDecisionCreate } from "@/api/revisionApi"
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

const DECISION_OPTIONS: {
  value: RevisionDecisionCreate["decision"]
  label: string
}[] = [
  { value: "accepted", label: "Принято" },
  { value: "accepted_with_frame", label: "Принято с оговоркой" },
  { value: "remark", label: "Замечание" },
  { value: "rejected", label: "Отклонено" },
  { value: "moved", label: "Перенесено" },
  { value: "deadline", label: "Срок" },
]

interface RevisionDecisionFormProps {
  change: Change
  onSubmit: (payload: RevisionDecisionCreate) => void
  onCancel: () => void
  isPending?: boolean
}

export function RevisionDecisionForm({
  change,
  onSubmit,
  onCancel,
  isPending,
}: RevisionDecisionFormProps) {
  const [decision, setDecision] = useState<RevisionDecisionCreate["decision"]>("accepted")
  const [deadline, setDeadline] = useState("")

  useEffect(() => {
    if (decision === "moved" || decision === "deadline") {
      // deadline field is required for these
    }
  }, [decision])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const payload: RevisionDecisionCreate = {
      decision,
      deadline: (decision === "moved" || decision === "deadline") ? deadline || null : null,
    }
    onSubmit(payload)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="text-sm text-muted-foreground mb-2">
        <span className="font-medium text-foreground">Поле:</span> {change.field}
        {change.old_value && (
          <div className="mt-1">
            <span className="text-red-500">− {change.old_value}</span>
          </div>
        )}
        {change.new_value && (
          <div className="mt-1">
            <span className="text-green-500">+ {change.new_value}</span>
          </div>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="decision">Решение *</Label>
        <Select value={decision} onValueChange={(v) => setDecision(v as RevisionDecisionCreate["decision"])}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {DECISION_OPTIONS.map((opt) => (
              <SelectItem key={opt.value} value={opt.value}>
                {opt.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {(decision === "moved" || decision === "deadline") && (
        <div className="space-y-2">
          <Label htmlFor="deadline">Срок</Label>
          <Input
            id="deadline"
            type="date"
            value={deadline}
            onChange={(e) => setDeadline(e.target.value)}
          />
        </div>
      )}

      <div className="flex gap-2 justify-end pt-2">
        <Button type="button" variant="outline" onClick={onCancel}>
          Отмена
        </Button>
        <Button type="submit" disabled={isPending}>
          {isPending ? "Сохранение..." : "Сохранить"}
        </Button>
      </div>
    </form>
  )
}
