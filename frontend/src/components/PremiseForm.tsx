import { useState, useEffect } from "react"
import {
  type PremiseCreate,
  type PremiseUpdate,
  type PremiseCategory,
} from "@/api/premiseApi"
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


const CATEGORIES: { value: PremiseCategory; label: string }[] = [
  { value: "contract", label: "Договор" },
  { value: "tz", label: "ТЗ" },
  { value: "customer_requirement", label: "Требование заказчика" },
  { value: "source_data", label: "Исходные данные" },
  { value: "norm", label: "Нормативные документы" },
  { value: "npa", label: "НПА" },
  { value: "bureaucracy", label: "Гос. бюрократия" },
  { value: "internal", label: "Внутренние причины" },
]

interface PremiseFormProps {
  initialData?: PremiseCreate | PremiseUpdate
  onSubmit: (data: PremiseCreate | PremiseUpdate) => void
  onCancel: () => void
  submitLabel?: string
}

export function PremiseForm({
  initialData,
  onSubmit,
  onCancel,
  submitLabel = "Сохранить",
}: PremiseFormProps) {
  const [name, setName] = useState(initialData?.name ?? "")
  const [category, setCategory] = useState<PremiseCategory>(
    initialData?.category ?? "contract",
  )
  const [source, setSource] = useState(initialData?.source ?? "")
  const [date, setDate] = useState(initialData?.date ?? "")
  const [actual, setActual] = useState(initialData?.actual ?? true)
  const [mandatory, setMandatory] = useState(initialData?.mandatory ?? true)
  const [link, setLink] = useState(initialData?.link ?? "")
  const [validUntil, setValidUntil] = useState(initialData?.valid_until ?? "")

  // Sync state when initialData changes (edit mode)
  useEffect(() => {
    if (initialData) {
      setName(initialData.name ?? "")
      setCategory(initialData.category ?? "contract")
      setSource(initialData.source ?? "")
      setDate(initialData.date ?? "")
      setActual(initialData.actual ?? true)
      setMandatory(initialData.mandatory ?? true)
      setLink(initialData.link ?? "")
      setValidUntil(initialData.valid_until ?? "")
    }
  }, [initialData])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim()) return

    onSubmit({
      category,
      name: name.trim(),
      source: source || null,
      date: date || null,
      actual,
      mandatory,
      link: link || null,
      valid_until: validUntil || null,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="category">Категория *</Label>
        <Select value={category} onValueChange={(v) => setCategory(v as PremiseCategory)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {CATEGORIES.map((cat) => (
              <SelectItem key={cat.value} value={cat.value}>
                {cat.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="name">Название *</Label>
        <Input
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Краткое название вводной"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="source">Источник</Label>
        <Input
          id="source"
          value={source}
          onChange={(e) => setSource(e.target.value)}
          placeholder="Откуда пришла"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="date">Дата вступления</Label>
        <Input
          id="date"
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </div>

      <div className="flex items-center justify-between">
        <Label htmlFor="actual">Актуальна</Label>
        <input
          id="actual"
          type="checkbox"
          checked={actual}
          onChange={(e) => setActual(e.target.checked)}
          className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
        />
      </div>

      <div className="flex items-center justify-between">
        <Label htmlFor="mandatory">Обязательна</Label>
        <input
          id="mandatory"
          type="checkbox"
          checked={mandatory}
          onChange={(e) => setMandatory(e.target.checked)}
          className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="link">Ссылка на документ</Label>
        <Input
          id="link"
          type="url"
          value={link}
          onChange={(e) => setLink(e.target.value)}
          placeholder="https://..."
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="validUntil">Действует до</Label>
        <Input
          id="validUntil"
          type="date"
          value={validUntil}
          onChange={(e) => setValidUntil(e.target.value)}
        />
      </div>

      <div className="flex gap-2 justify-end pt-2">
        <Button type="button" variant="outline" onClick={onCancel}>
          Отмена
        </Button>
        <Button type="submit" disabled={!name.trim()}>
          {submitLabel}
        </Button>
      </div>
    </form>
  )
}
