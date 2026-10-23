import { type DecisionLink, DECISION_LINK_TYPE_LABELS } from "@/api/decisionLinkApi"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Trash2, ArrowRight } from "lucide-react"

interface DecisionLinkCardProps {
  link: DecisionLink
  fromFormulation?: string
  toFormulation?: string
  onDelete: (id: string) => void
}

const TYPE_BADGE_VARIANTS: Record<string, string> = {
  sequential: "bg-blue-100 text-blue-800",
  parallel: "bg-green-100 text-green-800",
  nested: "bg-purple-100 text-purple-800",
}

export function DecisionLinkCard({
  link,
  fromFormulation,
  toFormulation,
  onDelete,
}: DecisionLinkCardProps) {
  const { id, link_type } = link

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-start justify-between gap-3">
        <CardTitle className="text-base flex-1">
          <div className="flex items-center gap-2">
            <span className="line-clamp-1">{fromFormulation ?? link.from_decision_id.slice(0, 8)}</span>
            <ArrowRight className="h-4 w-4 shrink-0" />
            <span className="line-clamp-1">{toFormulation ?? link.to_decision_id.slice(0, 8)}</span>
          </div>
        </CardTitle>
        <Badge className={TYPE_BADGE_VARIANTS[link_type] ?? ""}>
          {DECISION_LINK_TYPE_LABELS[link_type]}
        </Badge>
      </CardHeader>

      <CardContent>
        <p className="text-xs text-muted-foreground">
          Связь создана: {link.created_at ? new Date(link.created_at).toLocaleDateString("ru-RU") : "—"}
        </p>
      </CardContent>

      <CardFooter>
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
