import { useState, useEffect } from "react"
import {
  type ProjectStandardCreate,
  type ProjectStandardUpdate,
  type ProjectStandardType,
} from "@/api/projectStandardApi"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"

const STANDARD_TYPES: { value: ProjectStandardType; label: string }[] = [
  { value: "deadline", label: "Срок" },
  { value: "composition", label: "Состав" },
  { value: "format", label: "Формат" },
]

interface ProjectStandardFormProps {
  initialData?: ProjectStandardCreate | ProjectStandardUpdate
  onSubmit: (data: ProjectStandardCreate | ProjectStandardUpdate) => void
  onCancel: () => void
  submitLabel?: string
}

export function ProjectStandardForm({
  initialData,
  onSubmit,
  onCancel,
  submitLabel = "Сохранить",
}: ProjectStandardFormProps) {
  const [type, setType] = useState<ProjectStandardType>(
    initialData?.type ?? "deadline",
  )
  const [valueJson, setValueJson] = useState(() =>
    initialData?.value
      ? JSON.stringify(initialData.value, null, 2)
      : "{}",
  )
  const [jsonError, setJsonError] = useState<string | null>(null)

  // Sync state when initialData changes (edit mode)
  useEffect(() => {
    if (initialData) {
      setType(initialData.type ?? "deadline")
      setValueJson(
        initialData.value
          ? JSON.stringify(initialData.value, null, 2)
          : "{}",
      )
    }
  }, [initialData])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setJsonError(null)

    let parsedValue: Record<string, unknown> = {}
    if (valueJson.trim()) {
      try {
        parsedValue = JSON.parse(valueJson)
      } catch {
        setJsonError("Невалидный JSON")
        return
      }
    }

    onSubmit({
      type,
      value: parsedValue,
    } as ProjectStandardCreate | ProjectStandardUpdate)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="type">Тип *</Label>
        <Select value={type} onValueChange={(v) => setType(v as ProjectStandardType)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {STANDARD_TYPES.map((t) => (
              <SelectItem key={t.value} value={t.value}>
                {t.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="value">Значение (JSON)</Label>
        <Textarea
          id="value"
          value={valueJson}
          onChange={(e) => {
            setValueJson(e.target.value)
            setJsonError(null)
          }}
          placeholder='{"deadline": "2026-12-31"}'
          className="min-h-[120px] font-mono"
        />
      </div>

      {jsonError && (
        <p className="text-sm text-destructive">{jsonError}</p>
      )}

      <div className="flex gap-2 justify-end pt-2">
        <Button type="button" variant="outline" onClick={onCancel}>
          Отмена
        </Button>
        <Button type="submit">
          {submitLabel}
        </Button>
      </div>
    </form>
  )
}
