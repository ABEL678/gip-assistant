import { useState, useEffect } from "react"
import {
  type NormCreate,
  type NormUpdate,
  type NormType,
  NORM_TYPE_LABELS,
} from "@/api/normApi"
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

interface NormFormProps {
  initialData?: NormCreate | NormUpdate
  projectId: string
  onSubmit: (data: NormCreate | NormUpdate) => void
  onCancel: () => void
  submitLabel?: string
}

export function NormForm({
  initialData,
  projectId: _projectId,
  onSubmit,
  onCancel,
  submitLabel = "Сохранить",
}: NormFormProps) {
  const [code, setCode] = useState(initialData?.code ?? "")
  const [title, setTitle] = useState(initialData?.title ?? "")
  const [normType, setNormType] = useState<NormType>(
    (initialData?.norm_type as NormType) ?? "gost",
  )
  const [issuedAt, setIssuedAt] = useState(initialData?.issued_at ?? "")
  const [sourceUrl, setSourceUrl] = useState(initialData?.source_url ?? "")
  const [documentId, setDocumentId] = useState(initialData?.document_id ?? "")

  useEffect(() => {
    if (initialData) {
      setCode(initialData.code ?? "")
      setTitle(initialData.title ?? "")
      setNormType((initialData.norm_type as NormType) ?? "gost")
      setIssuedAt(initialData.issued_at ?? "")
      setSourceUrl(initialData.source_url ?? "")
      setDocumentId(initialData.document_id ?? "")
    }
  }, [initialData])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!code.trim() || !title.trim()) return

    onSubmit({
      code: code.trim(),
      title: title.trim(),
      norm_type: normType,
      issued_at: issuedAt || null,
      source_url: sourceUrl || null,
      document_id: documentId || null,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="code">Обозначение *</Label>
        <Input
          id="code"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="ГОСТ Р 21.101-2026"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="title">Название *</Label>
        <Input
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Название нормативного документа"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="norm_type">Тип *</Label>
        <Select value={normType} onValueChange={(v) => setNormType(v as NormType)}>
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {Object.entries(NORM_TYPE_LABELS).map(([value, label]) => (
              <SelectItem key={value} value={value}>{label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <Label htmlFor="issued_at">Дата введения</Label>
        <Input
          id="issued_at"
          type="date"
          value={issuedAt}
          onChange={(e) => setIssuedAt(e.target.value)}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="source_url">Источник (ссылка)</Label>
        <Input
          id="source_url"
          type="url"
          value={sourceUrl}
          onChange={(e) => setSourceUrl(e.target.value)}
          placeholder="https://..."
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="document_id">ID документа (UUID)</Label>
        <Input
          id="document_id"
          value={documentId}
          onChange={(e) => setDocumentId(e.target.value)}
          placeholder="uuid (необязательно)"
        />
      </div>

      <div className="flex gap-2 justify-end pt-2">
        <Button type="button" variant="outline" onClick={onCancel}>
          Отмена
        </Button>
        <Button type="submit" disabled={!code.trim() || !title.trim()}>
          {submitLabel}
        </Button>
      </div>
    </form>
  )
}
