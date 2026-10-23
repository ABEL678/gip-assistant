import { type Norm, NORM_TYPE_LABELS } from "@/api/normApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Pencil, Trash2, ExternalLink } from "lucide-react"

interface NormCardProps {
  norm: Norm
  onEdit: (norm: Norm) => void
  onDelete: (id: string) => void
}

const TYPE_BADGE_VARIANTS: Record<string, string> = {
  gost: "bg-red-100 text-red-800",
  snip: "bg-orange-100 text-orange-800",
  npa: "bg-purple-100 text-purple-800",
  xml_schema: "bg-cyan-100 text-cyan-800",
  other: "bg-gray-100 text-gray-800",
}

export function NormCard({ norm, onEdit, onDelete }: NormCardProps) {
  const { id, code, title, norm_type, source_url, issued_at } = norm

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <div className="space-y-1">
          <CardTitle className="text-base">{code}</CardTitle>
          <p className="text-sm font-medium">{title}</p>
        </div>
        <Badge className={TYPE_BADGE_VARIANTS[norm_type] ?? ""}>
          {NORM_TYPE_LABELS[norm_type]}
        </Badge>
      </CardHeader>

      <CardContent className="space-y-2 text-sm">
        {source_url && (
          <a
            href={source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-blue-600 hover:underline flex items-center gap-1"
          >
            <ExternalLink className="h-3 w-3" /> Источник
          </a>
        )}
        {issued_at && (
          <p className="text-xs text-muted-foreground">
            Дата введения: {new Date(issued_at).toLocaleDateString("ru-RU")}
          </p>
        )}
      </CardContent>

      <CardFooter className="gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={(e) => {
            e.stopPropagation()
            onEdit(norm)
          }}
        >
          <Pencil className="h-4 w-4 mr-1" /> Изменить
        </Button>
        <Button
          variant="destructive"
          size="sm"
          onClick={(e) => {
            e.stopPropagation()
            onDelete(id)
          }}
        >
          <Trash2 className="h-4 w-4 mr-1" /> Удалить
        </Button>
      </CardFooter>
    </Card>
  )
}
