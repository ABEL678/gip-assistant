import { useState, useMemo } from "react"
import { useParams, Link } from "react-router-dom"
import { ArrowLeft, Grid3x3, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { MatrixTable } from "@/components/MatrixTable"
import { CrossTaskDialog } from "@/components/CrossTaskDialog"
import {
  useMatrix,
  useGenerateMatrix,
  useUpdateCrossTask,
} from "@/hooks/useMatrix"
import {
  type CrossTask,
  type CrossTaskStatus,
  CROSS_TASK_STATUS_LABELS,
  CROSS_TASK_STATUS_COLORS,
} from "@/api/matrixApi"

export function MatrixPage() {
  const { id: projectId } = useParams<{ id: string }>()

  const { data: crossTasks, isLoading, isError, error } = useMatrix(projectId!)
  const generateMutation = useGenerateMatrix(projectId!)
  const updateMutation = useUpdateCrossTask(projectId!)

  const [dialogOpen, setDialogOpen] = useState(false)
  // Храним ID ячейки + разделы (а НЕ сам объект — чтобы брать свежие данные из кэша)
  const [selectedCellId, setSelectedCellId] = useState<string | null>(null)
  const [selectedSections, setSelectedSections] = useState<{
    from: string
    to: string
  } | null>(null)

  // Всегда берём АКТУАЛЬНЫЙ crossTask из свежего массива
  const selectedCrossTask: CrossTask | null = useMemo(() => {
    if (!selectedCellId || !crossTasks) return null
    return crossTasks.find((ct) => ct.id === selectedCellId) || null
  }, [selectedCellId, crossTasks])

  const handleCellClick = (
    crossTask: CrossTask | null,
    from: string,
    to: string,
  ) => {
    setSelectedCellId(crossTask?.id || null)
    setSelectedSections({ from, to })
    setDialogOpen(true)
  }

  const handleUpdateStatus = (status: CrossTaskStatus) => {
    if (!selectedCrossTask) return
    updateMutation.mutate({
      crossTaskId: selectedCrossTask.id,
      payload: { status },
    })
  }

  const handleGenerate = () => {
    generateMutation.mutate()
  }

  const handleCloseDialog = () => {
    setDialogOpen(false)
    // Чуть-чуть задержки, чтобы анимация закрытия прошла
    setTimeout(() => {
      setSelectedCellId(null)
      setSelectedSections(null)
    }, 150)
  }

  if (isLoading) {
    return <div className="text-muted-foreground">Загрузка матрицы...</div>
  }

  if (isError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Ошибка: {(error as Error).message}</AlertDescription>
      </Alert>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link to={`/projects/${projectId}`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            <Grid3x3 className="h-6 w-6" />
            Матрица смежников
          </h1>
          <p className="text-sm text-muted-foreground">
            Задания между разделами проекта
          </p>
        </div>
        <Button
          onClick={handleGenerate}
          disabled={generateMutation.isPending}
          className="ml-auto"
        >
          <RefreshCw
            className={`h-4 w-4 mr-2 ${generateMutation.isPending ? "animate-spin" : ""}`}
          />
          {generateMutation.isPending ? "Генерация..." : "Сгенерировать матрицу"}
        </Button>
      </div>

      {generateMutation.isSuccess && (
        <Alert>
          <AlertDescription>
            {generateMutation.data.cross_tasks_created > 0
              ? `Создано ячеек: ${generateMutation.data.cross_tasks_created}`
              : "Матрица актуальна — новых ячеек не создано"}
          </AlertDescription>
        </Alert>
      )}

      {crossTasks && crossTasks.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">
              Легенда ({crossTasks.length} ячеек)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-3">
              {(Object.keys(CROSS_TASK_STATUS_LABELS) as CrossTaskStatus[]).map(
                (s) => (
                  <div key={s} className="flex items-center gap-2 text-sm">
                    <span
                      className={`inline-block w-4 h-4 rounded border ${CROSS_TASK_STATUS_COLORS[s]}`}
                    />
                    {CROSS_TASK_STATUS_LABELS[s]}
                  </div>
                ),
              )}
            </div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardContent className="pt-6">
          <MatrixTable
            crossTasks={crossTasks || []}
            onCellClick={handleCellClick}
          />
        </CardContent>
      </Card>

      <CrossTaskDialog
        open={dialogOpen}
        onClose={handleCloseDialog}
        crossTask={selectedCrossTask}
        fromSection={selectedSections?.from || ""}
        toSection={selectedSections?.to || ""}
        onUpdateStatus={handleUpdateStatus}
        isUpdating={updateMutation.isPending}
      />
    </div>
  )
}