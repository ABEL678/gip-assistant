import { type DocumentVersion } from "@/api/documentVersionsApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Trash2, Upload } from "lucide-react"

function formatBytes(bytes: number): string {
  if (bytes < 1024) return bytes + " B"
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB"
  return (bytes / (1024 * 1024)).toFixed(1) + " MB"
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

interface VersionCardProps {
  version: DocumentVersion
  isCurrent: boolean
  onSetCurrent?: (id: string) => void
  onDelete?: (id: string) => void
}

export function VersionCard({ version, isCurrent, onSetCurrent, onDelete }: VersionCardProps) {
  const { id, version: ver, size_bytes, format_original, file_name, hash_sha256, uploaded_at } = version

  return (
    <Card
      className={`hover:shadow-md transition-shadow ${isCurrent ? "border-green-500 border-2" : ""}`}
    >
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">{ver}</CardTitle>
          {isCurrent && (
            <Badge variant="default">Текущая</Badge>
          )}
        </div>
      </CardHeader>

      <CardContent className="space-y-2">
        {/* Размер */}
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Upload className="h-3 w-3" />
          <span>{formatBytes(size_bytes)}</span>
        </div>

        {/* Формат */}
        <div className="text-sm">
          <span className="text-muted-foreground">Формат: </span>
          <Badge variant="secondary">{format_original}</Badge>
        </div>

        {/* Имя файла */}
        {file_name && (
          <div className="text-sm">
            <span className="text-muted-foreground">Файл: </span>
            <code className="text-xs font-mono bg-muted px-1.5 py-0.5 rounded">
              {file_name}
            </code>
          </div>
        )}

        {/* Хэш */}
        <div className="text-sm">
          <span className="text-muted-foreground">Хэш: </span>
          <code className="text-xs font-mono bg-muted px-1.5 py-0.5 rounded">
            {hash_sha256.slice(0, 8)}...
          </code>
        </div>

        {/* Дата */}
        <div className="text-xs text-muted-foreground">
          Загружен: {formatDate(uploaded_at)}
        </div>
      </CardContent>

      <CardFooter className="gap-2 pt-2">
        {!isCurrent && onSetCurrent && (
          <Button
            variant="outline"
            size="sm"
            onClick={(e) => {
              e.stopPropagation()
              onSetCurrent(id)
            }}
          >
            Сделать текущей
          </Button>
        )}
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
