import { useRun3Times } from "@/hooks/useGoals"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Play } from "lucide-react"

interface ProtocolSummaryPanelProps {
  projectId: string
}

export function ProtocolSummaryPanel({ projectId }: ProtocolSummaryPanelProps) {
  const { data: protocol, isPending, mutate: run3Times } = useRun3Times(projectId)

  const VERIFICATION_LABELS: Record<string, string> = {
    confirmed: "Подтверждена",
    requires_check: "Требуется проверка",
    no_data: "Нет данных",
    not_confirmed: "Не подтверждена",
  }

  const VERIFICATION_BADGE: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
    confirmed: "default",
    requires_check: "secondary",
    no_data: "outline",
    not_confirmed: "destructive",
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0">
        <CardTitle className="text-lg font-semibold">
          Протокол 3 прогонов
        </CardTitle>
        <Button
          onClick={() => run3Times()}
          disabled={isPending}
          size="sm"
        >
          <Play className="h-4 w-4 mr-1" />
          {isPending ? "Запуск..." : "Запустить 3 прогона"}
        </Button>
      </CardHeader>
      <CardContent className="space-y-4">
        {protocol && (
          <>
            {/* Unanimous */}
            <div>
              <h4 className="text-sm font-semibold text-green-600 mb-1">
                Unanimous (единогласно) — {Object.keys(protocol.unanimous).length}
              </h4>
              {Object.entries(protocol.unanimous).map(([goalId, status]) => (
                <div key={goalId} className="flex items-center gap-2 text-sm">
                  <span className="font-mono text-xs">{goalId}</span>
                  <Badge variant={VERIFICATION_BADGE[status] ?? "outline"} className="text-xs">
                    {VERIFICATION_LABELS[status] ?? status}
                  </Badge>
                </div>
              ))}
              {Object.keys(protocol.unanimous).length === 0 && (
                <p className="text-xs text-muted-foreground">Пусто</p>
              )}
            </div>

            {/* Majority */}
            <div>
              <h4 className="text-sm font-semibold text-amber-600 mb-1">
                Majority (большинство) — {Object.keys(protocol.majority).length}
              </h4>
              {Object.entries(protocol.majority).map(([goalId, status]) => (
                <div key={goalId} className="flex items-center gap-2 text-sm">
                  <span className="font-mono text-xs">{goalId}</span>
                  <Badge variant={VERIFICATION_BADGE[status] ?? "outline"} className="text-xs">
                    {VERIFICATION_LABELS[status] ?? status}
                  </Badge>
                </div>
              ))}
              {Object.keys(protocol.majority).length === 0 && (
                <p className="text-xs text-muted-foreground">Пусто</p>
              )}
            </div>

            {/* Split */}
            <div>
              <h4 className="text-sm font-semibold text-muted-foreground mb-1">
                Split (разделены) — {protocol.split.length}
              </h4>
              {protocol.split.map((goalId) => (
                <div key={goalId} className="text-sm font-mono text-xs">
                  {goalId}
                </div>
              ))}
              {protocol.split.length === 0 && (
                <p className="text-xs text-muted-foreground">Пусто</p>
              )}
            </div>

            {/* Total */}
            <div className="text-xs text-muted-foreground pt-2 border-t">
              Всего целей: {protocol.total}
            </div>
          </>
        )}
        {!protocol && !isPending && (
          <p className="text-sm text-muted-foreground">
            Нажмите «Запустить 3 прогона» для анализа целей
          </p>
        )}
      </CardContent>
    </Card>
  )
}
