import { ArrowUp, Plus, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { type RfiProposal, proposalKey } from "@/api/rfiApi"

const RULE_LABELS: Record<string, string> = {
  decision_без_ид: "Решение без ИД",
  rfi_просрочен: "RFI просрочен",
}

interface RfiProposalListProps {
  proposals: RfiProposal[]
  onCreateFromProposal: (proposal: RfiProposal) => void
  onEscalate: (proposal: RfiProposal) => void
  onRefresh: () => void
  approving: boolean
}

export function RfiProposalList({
  proposals,
  onCreateFromProposal,
  onEscalate,
  onRefresh,
  approving,
}: RfiProposalListProps) {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">
          Предложенные RFI{" "}
          <span className="text-muted-foreground">({proposals.length})</span>
        </h3>
        <Button variant="outline" size="sm" onClick={onRefresh}>
          <RefreshCw className="h-4 w-4 mr-1" /> Обновить
        </Button>
      </div>

      {proposals.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">
          Предложений нет
        </div>
      ) : (
        <div className="space-y-3">
          {proposals.map((proposal) => {
            const cannotCreate = !proposal.reason_decision_id || !proposal.rfi_due_date
            const cannotEscalate = !proposal.existing_rfi_id

            return (
              <div
                key={proposalKey(proposal)}
                className="border rounded-lg p-4 space-y-3"
              >
                <div className="flex flex-wrap items-center gap-2">
                  <Badge variant={proposal.action === "create" ? "default" : "destructive"}>
                    {proposal.action === "create" ? "Создать RFI" : "Эскалировать"}
                  </Badge>
                  <Badge variant="secondary">
                    {RULE_LABELS[proposal.rule] ?? proposal.rule}
                  </Badge>
                  {proposal.rfi_due_date && (
                    <Badge variant="outline">Срок: {proposal.rfi_due_date}</Badge>
                  )}
                </div>

                <p className="font-medium">{proposal.formulation}</p>

                {proposal.rationale && (
                  <p className="text-sm text-muted-foreground">{proposal.rationale}</p>
                )}

                {/* approving — общий флаг страницы: дизейблим блок целиком, чтобы исключить двойное создание */}
                {proposal.action === "create" ? (
                  <Button
                    size="sm"
                    onClick={() => onCreateFromProposal(proposal)}
                    disabled={approving || cannotCreate}
                  >
                    <Plus className="h-4 w-4 mr-1" /> Создать
                  </Button>
                ) : (
                  <Button
                    size="sm"
                    onClick={() => onEscalate(proposal)}
                    disabled={approving || cannotEscalate}
                  >
                    <ArrowUp className="h-4 w-4 mr-1" /> Эскалировать
                  </Button>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
