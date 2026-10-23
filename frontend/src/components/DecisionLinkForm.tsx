import { useState } from "react"
import {
  type DecisionLinkCreate,
  type DecisionLinkType,
  DECISION_LINK_TYPE_LABELS,
} from "@/api/decisionLinkApi"
import { type Decision } from "@/api/decisionApi"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

interface DecisionLinkFormProps {
  decisions: Decision[]
  onSubmit: (data: DecisionLinkCreate) => void
  onCancel: () => void
  submitLabel?: string
}

export function DecisionLinkForm({
  decisions,
  onSubmit,
  onCancel,
  submitLabel = "Создать связь",
}: DecisionLinkFormProps) {
  const [fromDecisionId, setFromDecisionId] = useState("")
  const [toDecisionId, setToDecisionId] = useState("")
  const [linkType, setLinkType] = useState<DecisionLinkType>("sequential")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!fromDecisionId || !toDecisionId) return
    if (fromDecisionId === toDecisionId) return

    onSubmit({
      from_decision_id: fromDecisionId,
      to_decision_id: toDecisionId,
      link_type: linkType,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="from_decision_id">От решения *</Label>
        <Select value={fromDecisionId} onValueChange={setFromDecisionId}>
          <SelectTrigger>
            <SelectValue placeholder="Выберите решение" />
          </SelectTrigger>
          <SelectContent>
            {decisions.map((d) => (
              <SelectItem key={d.id} value={d.id}>{d.formulation}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="to_decision_id">К решению *</Label>
        <Select value={toDecisionId} onValueChange={setToDecisionId}>
          <SelectTrigger>
            <SelectValue placeholder="Выберите решение" />
          </SelectTrigger>
          <SelectContent>
            {decisions.map((d) => (
              <SelectItem key={d.id} value={d.id}>{d.formulation}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="link_type">Тип связи *</Label>
        <Select value={linkType} onValueChange={(v) => setLinkType(v as DecisionLinkType)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {Object.entries(DECISION_LINK_TYPE_LABELS).map(([value, label]) => (
              <SelectItem key={value} value={value}>{label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {fromDecisionId && toDecisionId && fromDecisionId === toDecisionId && (
        <p className="text-sm text-destructive">
          Нельзя создать связь решения с самим собой
        </p>
      )}

      <div className="flex gap-2 justify-end pt-2">
        <Button type="button" variant="outline" onClick={onCancel}>
          Отмена
        </Button>
        <Button
          type="submit"
          disabled={!fromDecisionId || !toDecisionId || fromDecisionId === toDecisionId}
        >
          {submitLabel}
        </Button>
      </div>
    </form>
  )
}
