import { Link } from "react-router-dom"
import { type Document } from "@/api/documentsApi"
import { type DocumentType } from "@/api/documentTypesApi"
import { type LifecycleStatus } from "@/api/documentEnums"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Trash2, ExternalLink } from "lucide-react"

const STATUS_COLORS: Record<LifecycleStatus, string> = {
  DRAFT: "bg-gray-200 text-gray-700",
  IN_REVIEW: "bg-blue-200 text-blue-700",
  NORMOCONTROL: "bg-yellow-200 text-yellow-700",
  APPROVED: "bg-green-200 text-green-700",
  ARCHIVED: "bg-gray-200 text-gray-700",
  ANNULLED: "bg-red-200 text-red-700",
  REPLACED: "bg-orange-200 text-orange-700",
}

const STATUS_LABELS: Record<LifecycleStatus, string> = {
  DRAFT: "Черновик",
  IN_REVIEW: "На рассмотрении",
  NORMOCONTROL: "Нормоконтроль",
  APPROVED: "Согласован",
  ARCHIVED: "Архив",
  ANNULLED: "Аннулирован",
  REPLACED: "Заменён",
}

interface DocumentCardProps {
  document: Document
  documentType?: DocumentType
  onDelete?: (id: string) => void
}

export function DocumentCard({ document, documentType, onDelete }: DocumentCardProps) {
  const {
    id,
    document_name,
    cipher,
    document_kind,
    lifecycle_status,
    section_code,
    mark,
  } = document

  const projectId = document.project_id

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg leading-tight">{document_name}</CardTitle>
      </CardHeader>

      <CardContent className="space-y-3">
        {/* Cipher */}
        {cipher && (
          <div className="flex items-center gap-2">
            <span className="text-xs text-muted-foreground">Шифр:</span>
            <code className="text-xs font-mono bg-muted px-1.5 py-0.5 rounded">
              {cipher}
            </code>
          </div>
        )}

        {/* Badges row */}
        <div className="flex flex-wrap gap-1.5">
          <Badge variant="outline" className={STATUS_COLORS[lifecycle_status]}>
            {STATUS_LABELS[lifecycle_status]}
          </Badge>

          <Badge variant="secondary">
            {document_kind === "ПД" ? "ПД" : "РД"}
          </Badge>

          {documentType && (
            <Badge variant="secondary">{documentType.name}</Badge>
          )}
        </div>

        {/* Section / Mark */}
        {(section_code || mark) && (
          <div className="flex flex-wrap gap-2 text-sm text-muted-foreground">
            {section_code && (
              <span>
                Секция: <strong>{section_code}</strong>
              </span>
            )}
            {mark && (
              <span>
                Марка: <strong>{mark}</strong>
              </span>
            )}
          </div>
        )}
      </CardContent>

      <CardFooter className="gap-2 pt-2">
        <Link to={`/projects/${projectId}/documents/${id}/edit`} onClick={(e) => e.stopPropagation()}>
          <Button variant="outline" size="sm">
            <ExternalLink className="h-4 w-4 mr-1" />
            Открыть
          </Button>
        </Link>
        {onDelete && (
          <Button
            variant="destructive"
            size="sm"
            onClick={(e) => {
              e.stopPropagation()
              onDelete(id)
            }}
          >
            <Trash2 className="h-4 w-4 mr-1" />
            Удалить
          </Button>
        )}
      </CardFooter>
    </Card>
  )
}
