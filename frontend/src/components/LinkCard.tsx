import { type DocumentLink, type DocumentLinkType } from "@/api/documentLinksApi"
import { type Document } from "@/api/documentsApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Trash2 } from "lucide-react"

const LINK_TYPE_LABELS: Record<DocumentLinkType, string> = {
  appendix: "Приложение",
  reference: "Ссылка",
  replaces: "Заменяет",
  version_of: "Версия",
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("ru-RU", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  })
}

interface LinkCardProps {
  link: DocumentLink
  direction: "outgoing" | "incoming"
  targetDocument?: Document
  sourceDocument?: Document
  onDelete?: (id: string) => void
}

export function LinkCard({ link, direction, targetDocument, sourceDocument, onDelete }: LinkCardProps) {
  const { id, link_type, created_at } = link

  const isOutgoing = direction === "outgoing"

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">
            {LINK_TYPE_LABELS[link_type]}
          </CardTitle>
          <Badge variant={isOutgoing ? "default" : "secondary"}>
            {isOutgoing ? "→ Исходящая" : "← Входящая"}
          </Badge>
        </div>
      </CardHeader>

      <CardContent className="space-y-2">
        {/* Target/Source document */}
        {(isOutgoing ? targetDocument : sourceDocument) && (
          <div className="text-sm">
            <span className="text-muted-foreground">
              {isOutgoing ? "Цель: " : "Источник: "}
            </span>
            <strong>
              {(isOutgoing ? targetDocument : sourceDocument)?.document_name}
            </strong>
          </div>
        )}

        {/* Date */}
        <div className="text-xs text-muted-foreground">
          Создана: {formatDate(created_at)}
        </div>
      </CardContent>

      <CardFooter className="gap-2 pt-2">
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
