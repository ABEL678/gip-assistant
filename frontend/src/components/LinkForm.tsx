import { useState } from "react"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { useDocumentsByProject } from "@/hooks/useDocuments"
import { type DocumentLinkType } from "@/api/documentEnums"

const LINK_TYPE_OPTIONS: { value: DocumentLinkType; label: string }[] = [
  { value: "appendix", label: "Приложение" },
  { value: "reference", label: "Ссылка" },
  { value: "replaces", label: "Заменяет" },
  { value: "version_of", label: "Версия" },
]

interface LinkFormProps {
  projectId: string
  currentDocumentId: string
  onSubmit: (payload: {
    target_document_id: string
    link_type: DocumentLinkType
  }) => void
  onCancel: () => void
  isPending: boolean
}

export function LinkForm({ projectId, currentDocumentId, onSubmit, onCancel, isPending }: LinkFormProps) {
  const { data: allDocuments } = useDocumentsByProject(projectId)

  const availableDocuments = (allDocuments || []).filter(
    (d) => d.id !== currentDocumentId
  )

  const [targetDocumentId, setTargetDocumentId] = useState("")
  const [linkType, setLinkType] = useState<DocumentLinkType | "">("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!targetDocumentId || !linkType) return

    onSubmit({
      target_document_id: targetDocumentId,
      link_type: linkType as DocumentLinkType,
    })
  }

  const hasDocuments = availableDocuments.length > 0

  return (
    <form onSubmit={handleSubmit}>
      <Card>
        <CardHeader>
          <CardTitle>Новая связь</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* target_document_id */}
          <div>
            <Label>Целевой документ *</Label>
            <Select
              value={targetDocumentId}
              onValueChange={setTargetDocumentId}
              disabled={!hasDocuments}
            >
              <SelectTrigger>
                <SelectValue placeholder="Выберите документ" />
              </SelectTrigger>
              <SelectContent>
                {availableDocuments.map((doc) => (
                  <SelectItem key={doc.id} value={doc.id}>
                    {doc.document_name} ({doc.cipher})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {!hasDocuments && (
              <p className="text-xs text-muted-foreground mt-1">
                Нет других документов в проекте для связи
              </p>
            )}
          </div>

          {/* link_type */}
          <div>
            <Label>Тип связи *</Label>
            <Select
              value={linkType}
              onValueChange={(v) => setLinkType(v as DocumentLinkType)}
              disabled={!hasDocuments}
            >
              <SelectTrigger>
                <SelectValue placeholder="Выберите тип" />
              </SelectTrigger>
              <SelectContent>
                {LINK_TYPE_OPTIONS.map((opt) => (
                  <SelectItem key={opt.value} value={opt.value}>
                    {opt.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
        <CardFooter className="gap-2">
          <Button
            type="submit"
            disabled={isPending || !hasDocuments}
          >
            {isPending ? "Создание..." : "Создать связь"}
          </Button>
          <Button variant="outline" type="button" onClick={onCancel}>
            Отмена
          </Button>
        </CardFooter>
      </Card>
    </form>
  )
}
