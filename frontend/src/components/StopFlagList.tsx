import { useState } from "react"
import { type StopFlagCreate } from "@/api/revisionApi"
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { AlertCircle } from "lucide-react"

interface StopFlagListProps {
  onStopFlag: (payload: StopFlagCreate) => void
  isPending?: boolean
}

export function StopFlagList({
  onStopFlag,
  isPending,
}: StopFlagListProps) {
  const [reason, setReason] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!reason.trim()) return
    onStopFlag({ reason: reason.trim() })
    setReason("")
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <AlertCircle className="h-5 w-5 text-destructive" />
          Стоп-сигналы
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <form onSubmit={handleSubmit} className="space-y-3">
          <Textarea
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Причина стоп-сигнала..."
            rows={3}
          />
          <Button type="submit" disabled={isPending || !reason.trim()}>
            {isPending ? "Добавление..." : "Добавить стоп-сигнал"}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
