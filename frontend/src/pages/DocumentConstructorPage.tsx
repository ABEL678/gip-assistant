import { useEffect, useState } from "react"
import { useParams, useNavigate, Link } from "react-router-dom"
import { ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { useDocument, useCreateDocument, useUpdateDocument } from "@/hooks/useDocuments"
import { useDocumentTypes } from "@/hooks/useDocumentTypes"
import { type Document, type LifecycleStatus } from "@/api/documentsApi"
import { type DocumentType } from "@/api/documentTypesApi"
import { type DocumentKind, type DocPartType } from "@/api/documentEnums"

const LIFECYCLE_OPTIONS: { value: LifecycleStatus; label: string }[] = [
  { value: "DRAFT", label: "Черновик" },
  { value: "IN_REVIEW", label: "На рассмотрении" },
  { value: "NORMOCONTROL", label: "Нормоконтроль" },
  { value: "APPROVED", label: "Согласован" },
  { value: "ARCHIVED", label: "Архив" },
  { value: "ANNULLED", label: "Аннулирован" },
  { value: "REPLACED", label: "Заменён" },
]

const KIND_OPTIONS: { value: DocumentKind; label: string }[] = [
  { value: "ПД", label: "ПД" },
  { value: "РД", label: "РД" },
]

const DOC_PART_OPTIONS: { value: DocPartType | "__none__"; label: string }[] = [
  { value: "__none__", label: "— не задано —" },
  { value: "ТЧ", label: "ТЧ" },
  { value: "ГЧ", label: "ГЧ" },
]

export function DocumentConstructorPage() {
  const { id: projectId, docId } = useParams<{ id: string; docId: string }>()
  const navigate = useNavigate()
  const isEdit = !!docId

  const { data: document, isLoading, isError, error } = useDocument(
    isEdit ? docId! : "",
  )

  const createMutation = useCreateDocument(projectId!)
  const updateMutation = useUpdateDocument(projectId!)
  const { data: documentTypes } = useDocumentTypes()

  const [documentTypeId, setDocumentTypeId] = useState("")
  const [documentName, setDocumentName] = useState("")
  const [cipher, setCipher] = useState("")
  const [documentKind, setDocumentKind] = useState<DocumentKind>("ПД")
  const [docPartType, setDocPartType] = useState<DocPartType | "__none__">("__none__")
  const [sectionCode, setSectionCode] = useState("")
  const [mark, setMark] = useState("")
  const [baseDesignation, setBaseDesignation] = useState("")
  const [lifecycleStatus, setLifecycleStatus] = useState<LifecycleStatus>("DRAFT")

  useEffect(() => {
    if (document) {
      setDocumentTypeId(document.document_type_id)
      setDocumentName(document.document_name)
      setCipher(document.cipher)
      setDocumentKind(document.document_kind)
      setDocPartType(
        document.doc_part_type === "ТЧ"
          ? "ТЧ"
          : document.doc_part_type === "ГЧ"
          ? "ГЧ"
          : "__none__",
      )
      setSectionCode(document.section_code ?? "")
      setMark(document.mark ?? "")
      setBaseDesignation(document.base_designation ?? "")
      setLifecycleStatus(document.lifecycle_status)
    }
  }, [document])

  const handleSave = () => {
    if (!documentTypeId.trim() || !documentName.trim() || !cipher.trim()) return

    const base = {
      document_kind: documentKind,
      doc_part_type: docPartType === "__none__" ? null : docPartType,
      section_code: sectionCode || null,
      mark: mark || null,
      base_designation: baseDesignation || null,
      lifecycle_status: lifecycleStatus,
    }

    if (isEdit && docId) {
      updateMutation.mutate({ documentId: docId, payload: base })
    } else {
      createMutation.mutate({
        ...base,
        document_type_id: documentTypeId,
        document_name: documentName,
        cipher: cipher,
      })
    }
  }

  useEffect(() => {
    if (createMutation.isSuccess || updateMutation.isSuccess) {
      navigate(`/projects/${projectId}/documents`)
    }
  }, [createMutation.isSuccess, updateMutation.isSuccess, navigate, projectId])

  if (isLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (isError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>{(error as Error).message}</AlertDescription>
      </Alert>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link to={`/projects/${projectId}/documents`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">
            {isEdit ? "Редактировать документ" : "Создать документ"}
          </h1>
        </div>
      </div>

      {/* Form */}
      <div className="space-y-6">
        {/* Card 1: Обозначение */}
        <Card>
          <CardHeader>
            <CardTitle>Обозначение</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* documentTypeId */}
            <div>
              <Label>Тип документа *</Label>
              <Select
                value={documentTypeId}
                onValueChange={setDocumentTypeId}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Выберите тип" />
                </SelectTrigger>
                <SelectContent>
                  {documentTypes?.map((type) => (
                    <SelectItem key={type.id} value={type.id}>
                      {type.name} ({type.code})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* cipher */}
            <div>
              <Label>Шифр *</Label>
              <Input
                value={cipher}
                onChange={(e) => setCipher(e.target.value)}
                placeholder="АБЗ-001-ПЗ"
              />
            </div>

            {/* base_designation */}
            <div>
              <Label>Базовое обозначение</Label>
              <Input
                value={baseDesignation}
                onChange={(e) => setBaseDesignation(e.target.value)}
                placeholder="АБЗ-001-ПЗ"
              />
            </div>
          </CardContent>
        </Card>

        {/* Card 2: Наименование */}
        <Card>
          <CardHeader>
            <CardTitle>Наименование</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label>Наименование *</Label>
              <Input
                value={documentName}
                onChange={(e) => setDocumentName(e.target.value)}
                placeholder="Пояснительная записка"
              />
            </div>
          </CardContent>
        </Card>

        {/* Card 3: Классификация */}
        <Card>
          <CardHeader>
            <CardTitle>Классификация</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* document_kind */}
            <div>
              <Label>Вид</Label>
              <Select
                value={documentKind}
                onValueChange={(v) => setDocumentKind(v as DocumentKind)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {KIND_OPTIONS.map((opt) => (
                    <SelectItem key={opt.value} value={opt.value}>
                      {opt.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* doc_part_type */}
            <div>
              <Label>Часть</Label>
              <Select
                value={docPartType}
                onValueChange={(v) => setDocPartType(v as DocPartType | "__none__")}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {DOC_PART_OPTIONS.map((opt) => (
                    <SelectItem key={opt.value} value={opt.value}>
                      {opt.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* lifecycle_status */}
            <div>
              <Label>Статус</Label>
              <Select
                value={lifecycleStatus}
                onValueChange={(v) => setLifecycleStatus(v as LifecycleStatus)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {LIFECYCLE_OPTIONS.map((opt) => (
                    <SelectItem key={opt.value} value={opt.value}>
                      {opt.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* section_code */}
            <div>
              <Label>Секция</Label>
              <Input
                value={sectionCode}
                onChange={(e) => setSectionCode(e.target.value)}
                placeholder="АБЗ"
              />
            </div>

            {/* mark */}
            <div>
              <Label>Марка</Label>
              <Input
                value={mark}
                onChange={(e) => setMark(e.target.value)}
                placeholder="АБЗ-001"
              />
            </div>
          </CardContent>
        </Card>

        {/* Footer buttons */}
        <div className="flex gap-2">
          <Button
            onClick={handleSave}
            disabled={createMutation.isPending || updateMutation.isPending}
          >
            {createMutation.isPending || updateMutation.isPending
              ? "Сохранение..."
              : "Сохранить"}
          </Button>
          <Button
            variant="outline"
            onClick={() => navigate(`/projects/${projectId}/documents`)}
          >
            Отмена
          </Button>
        </div>
      </div>
    </div>
  )
}
