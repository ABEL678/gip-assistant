import { useSimilarityMatrix } from "@/hooks/useGoals"
import { Alert, AlertDescription } from "@/components/ui/alert"

interface SimilarityMatrixPanelProps {
  projectId: string
}

export function SimilarityMatrixPanel({ projectId }: SimilarityMatrixPanelProps) {
  const { data, isLoading } = useSimilarityMatrix(projectId)

  if (isLoading) {
    return <p className="text-muted-foreground">Загрузка матрицы...</p>
  }

  if (!data?.links?.length) {
    return (
      <Alert>
        <AlertDescription>
          Нет связей (в договоре нет нужных разделов)
        </AlertDescription>
      </Alert>
    )
  }

  return (
    <div className="space-y-3">
      <h3 className="text-lg font-semibold">Матрица смежников</h3>
      <div className="space-y-2">
        {data.links.map((link, i) => (
          <div key={i} className="border rounded-lg p-3 space-y-1">
            <div className="font-medium text-sm">
              {link.from_section} ↔ {link.to_section}
            </div>
            <div className="text-sm text-muted-foreground">
              Что: {link.what}
            </div>
            <div className="text-sm text-muted-foreground">
              Риск: {link.risk}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
