import { useState, useEffect } from "react"
import {
  type ResultCreate,
  type ResultUpdate,
} from "@/api/resultApi"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

interface ResultFormProps {
  initialData?: ResultCreate | ResultUpdate
  onSubmit: (data: ResultCreate | ResultUpdate) => void
  onCancel: () => void
  submitLabel?: string
}

export function ResultForm({
  initialData,
  onSubmit,
  onCancel,
  submitLabel = "Сохранить",
}: ResultFormProps) {
  const [formulation, setFormulation] = useState(
    initialData?.formulation ?? "",
  )
  const [source, setSource] = useState(initialData?.source ?? "")

  // Sync state when initialData changes (edit mode)
  useEffect(() => {
    if (initialData) {
      setFormulation(initialData.formulation ?? "")
      setSource(initialData.source ?? "")
    }
  }, [initialData])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!formulation.trim()) return

    onSubmit({
      formulation: formulation.trim(),
      source: source || null,
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
          placeholder="Краткая формулировка результата"
          required
          className="min-h-[100px]"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="source">Источник</Label>
        <Input
          id="source"
          value={source}
          onChange={(e) => setSource(e.target.value)}
          placeholder="Откуда взят результат"
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
