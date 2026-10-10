import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import {
  CROSS_TASK_STATUS_LABELS,
  CROSS_TASK_STATUS_COLORS,
  type CrossTask,
  type CrossTaskStatus,
} from "@/api/matrixApi"

interface CrossTaskDialogProps {
  open: boolean
  onClose: () => void
  crossTask: CrossTask | null
  fromSection: string
  toSection: string
  onUpdateStatus?: (status: CrossTaskStatus) => void
  isUpdating?: boolean
}

const ALL_STATUSES: CrossTaskStatus[] = [
  "NOT_STARTED",
  "IN_PROGRESS",
  "WAITING_INFO",
  "DONE",
  "OVERDUE",
]

export function CrossTaskDialog({
  open,
  onClose,
  crossTask,
  fromSection,
  toSection,
  onUpdateStatus,
  isUpdating,
}: CrossTaskDialogProps) {
  return (
    <Dialog open={open} onOpenChange={(v) => !v && onClose()}>
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>
            {fromSection} → {toSection}
          </DialogTitle>
          <DialogDescription>
            Задание от раздела «{fromSection}» разделу «{toSection}»
          </DialogDescription>
        </DialogHeader>

        {crossTask ? (
          <div className="space-y-4">
            <div>
              <div className="text-xs text-muted-foreground mb-1">Текущий статус</div>
              <Badge
                variant="outline"
                className={CROSS_TASK_STATUS_COLORS[crossTask.status]}
              >
                {CROSS_TASK_STATUS_LABELS[crossTask.status]}
              </Badge>
            </div>

            {crossTask.description && (
              <div>
                <div className="text-xs text-muted-foreground mb-1">Сводка</div>
                <div className="text-sm">{crossTask.description}</div>
              </div>
            )}

            <div>
              <div className="text-xs text-muted-foreground mb-2">
                Изменить статус
              </div>
              <Select
                key={`${crossTask.id}-${crossTask.status}`}
                value={crossTask.status}
                onValueChange={(v) => onUpdateStatus?.(v as CrossTaskStatus)}
                disabled={isUpdating}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {ALL_STATUSES.map((s) => (
                    <SelectItem key={s} value={s}>
                      {CROSS_TASK_STATUS_LABELS[s]}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
        ) : (
          <div className="text-sm text-muted-foreground py-4">
            Между разделами «{fromSection}» и «{toSection}» нет заданий.
            Матрица строится автоматически из задач, где заполнены поля
            «Раздел (от кого)» и «Получатель (кому)».
          </div>
        )}

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            Закрыть
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}