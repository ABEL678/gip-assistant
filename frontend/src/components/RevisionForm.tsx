import { useState } from "react"
import { type RevisionCreate } from "@/api/revisionApi"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Checkbox } from "@/components/ui/checkbox"

interface RevisionFormProps {
  onSubmit: (data: RevisionCreate) => void
  onCancel: () => void
  isPending?: boolean
}

export function RevisionForm({
  onSubmit,
  onCancel,
  isPending,
}: RevisionFormProps) {
  const [version, setVersion] = useState("")
  const [date, setDate] = useState("")
  const [source, setSource] = useState("")
  const [notified, setNotified] = useState(false)
  const [stopFlag, setStopFlag] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const versionNum = parseInt(version, 10)
    if (!version || isNaN(versionNum) || versionNum < 1) return

    onSubmit({
      version: versionNum,
      date: date || null,
      source: source || null,
      notified,
      stop_flag: stopFlag,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="version">Версия *</Label>
        <Input
          id="version"
          type="number"
          min={1}
          value={version}
          onChange={(e) => setVersion(e.target.value)}
          placeholder="1"
          required
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="date">Дата</Label>
        <Input
          id="date"
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="source">Источник</Label>
        <Input
          id="source"
          value={source}
          onChange={(e) => setSource(e.target.value)}
          placeholder="Откуда взята ревизия"
        />
      </div>

      <div className="flex items-center space-x-2">
        <Checkbox
          id="notified"
          checked={notified}
          onCheckedChange={(checked) => setNotified(!!checked)}
        />
        <Label htmlFor="notified">Уведомил</Label>
      </div>

      <div className="flex items-center space-x-2">
        <Checkbox
          id="stopFlag"
          checked={stopFlag}
          onCheckedChange={(checked) => setStopFlag(!!checked)}
        />
        <Label htmlFor="stopFlag">Стоп-флаг</Label>
      </div>

      <div className="flex gap-2 justify-end pt-2">
        <Button type="button" variant="outline" onClick={onCancel}>
          Отмена
        </Button>
        <Button type="submit" disabled={isPending}>
          {isPending ? "Сохранение..." : "Сохранить"}
        </Button>
      </div>
    </form>
  )
}
