import { useParams, Link } from "react-router-dom"
import { useState } from "react"
import { ArrowLeft, Plus, Filter } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { useDocumentsByProject, useDeleteDocument } from "@/hooks/useDocuments"
import { useDocumentTypes } from "@/hooks/useDocumentTypes"
import { type LifecycleStatus } from "@/api/documentEnums"
import { DocumentCard } from "@/components/DocumentCard"

const LIFECYCLE_OPTIONS: { value: LifecycleStatus | undefined; label: string }[] = [
  { value: undefined, label: "Все" },
  { value: "DRAFT", label: "Черновик" },
  { value: "IN_REVIEW", label: "На рассмотрении" },
  { value: "NORMOCONTROL", label: "Нормоконтроль" },
  { value: "APPROVED", label: "Согласован" },
  { value: "ARCHIVED", label: "Архив" },
  { value: "ANNULLED", label: "Аннулирован" },
  { value: "REPLACED", label: "Заменён" },
]

export function DocumentsPage() {
  const { id: projectId } = useParams<{ id: string }>()

  const [lifecycleStatus, setLifecycleStatus] = useState<LifecycleStatus | undefined>(undefined)

  const { data: documents, isLoading, isError, error } = useDocumentsByProject(projectId!, lifecycleStatus)
  const { data: documentTypes } = useDocumentTypes()
  const deleteMutation = useDeleteDocument(projectId!)

  const handleDelete = (id: string) => {
    if (window.confirm("Удалить этот документ?")) {
      deleteMutation.mutate(id)
    }
  }

  const typeMap = documentTypes
    ? Object.fromEntries(documentTypes.map((t) => [t.id, t]))
    : {}

  if (isLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (isError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Ошибка: {(error as Error).message}</AlertDescription>
      </Alert>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link to={`/projects/${projectId}`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">Документы проекта</h1>
          <p className="text-sm text-muted-foreground">
            Управление документами проекта
          </p>
        </div>
        <Link to={`/projects/${projectId}/documents/new`}>
          <Button>
            <Plus className="h-4 w-4 mr-2" />
            Создать документ
          </Button>
        </Link>
      </div>

      {/* Filter */}
      <div className="flex items-center gap-2">
        <Filter className="h-4 w-4 text-muted-foreground" />
        <Select
          value={lifecycleStatus}
          onValueChange={(v) =>
            setLifecycleStatus(v === "" ? undefined : (v as LifecycleStatus))
          }
        >
          <SelectTrigger className="w-[200px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {LIFECYCLE_OPTIONS.map((opt) => (
              <SelectItem key={opt.value ?? "all"} value={opt.value ?? ""}>
                {opt.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Empty state */}
      {!isLoading && !isError && documents && documents.length === 0 && (
        <div className="text-center py-12 text-muted-foreground">
          Пока нет документов
          <div className="mt-4">
            <Link to={`/projects/${projectId}/documents/new`}>
              <Button variant="outline">Создать первый документ</Button>
            </Link>
          </div>
        </div>
      )}

      {/* Grid */}
      {!isLoading && !isError && documents && documents.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {documents.map((doc) => (
            <DocumentCard
              key={doc.id}
              document={doc}
              documentType={typeMap[doc.document_type_id]}
              onDelete={handleDelete}
            />
          ))}
        </div>
      )}
    </div>
  )
}
