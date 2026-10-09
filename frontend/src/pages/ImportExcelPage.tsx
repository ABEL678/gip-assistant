import { useState } from "react"
import { useParams, Link } from "react-router-dom"
import { ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { FileDropzone } from "@/components/FileDropzone"
import { HeaderRowSelector } from "@/components/HeaderRowSelector"
import { ColumnMappingTable } from "@/components/ColumnMappingTable"
import { useImportPreview, useImportConfirm } from "@/hooks/useImport"
import type {
  ImportPreviewResponse,
  ColumnMappingPayload,
} from "@/api/importApi"

export function ImportExcelPage() {
  const { id: projectId } = useParams<{ id: string }>()

  const [file, setFile] = useState<File | null>(null)
  const [headerRow, setHeaderRow] = useState<number | undefined>(undefined)
  const [preview, setPreview] = useState<ImportPreviewResponse | null>(null)
  const [mapping, setMapping] = useState<Partial<ColumnMappingPayload>>({})

  const previewMutation = useImportPreview()
  const confirmMutation = useImportConfirm()

  const handleFileSelected = async (f: File) => {
    setFile(f)
    setPreview(null)
    setHeaderRow(undefined)
    setMapping({})

    if (!projectId) return
    const result = await previewMutation.mutateAsync({
      projectId,
      file: f,
    })
    setPreview(result)
    setHeaderRow(result.header_row_index)
    setMapping(result.suggested_mapping as Partial<ColumnMappingPayload>)
  }

  const handleHeaderRowChange = async (idx: number) => {
    if (!projectId || !file) return
    setHeaderRow(idx)
    const result = await previewMutation.mutateAsync({
      projectId,
      file,
      headerRow: idx,
    })
    setPreview(result)
    setMapping(result.suggested_mapping as Partial<ColumnMappingPayload>)
  }

  const handleConfirm = async () => {
    if (!projectId || !file || !mapping.task_title) return
    await confirmMutation.mutateAsync({
      projectId,
      file,
      columnMapping: mapping as ColumnMappingPayload,
      headerRow,
    })
  }

  const canConfirm = !!mapping.task_title && !!preview

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link to={`/projects/${projectId}`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-2xl font-bold">Импорт Excel</h1>
          <p className="text-sm text-muted-foreground">
            Загрузите Excel-файл с задачами проекта
          </p>
        </div>
      </div>

      <FileDropzone
        onFileSelected={handleFileSelected}
        selectedFile={file}
        disabled={previewMutation.isPending || confirmMutation.isPending}
      />

      {previewMutation.isPending && (
        <Card>
          <CardContent className="py-8 text-center text-muted-foreground">
            Читаем файл...
          </CardContent>
        </Card>
      )}

      {previewMutation.isError && (
        <Alert variant="destructive">
          <AlertDescription>
            Ошибка чтения файла: {(previewMutation.error as Error).message}
          </AlertDescription>
        </Alert>
      )}

      {preview && (
        <>
          <HeaderRowSelector
            previewRows={preview.preview_rows_raw}
            selectedIndex={preview.header_row_index}
            onSelect={handleHeaderRowChange}
          />

          <Card>
            <CardHeader>
              <CardTitle className="text-base">
                Маппинг колонок ({preview.columns.length} колонок,{" "}
                {preview.total_rows} строк данных)
              </CardTitle>
              <p className="text-sm text-muted-foreground">
                Укажите, какая колонка Excel соответствует какому полю задачи.
                Обязательно — «Название задачи».
              </p>
            </CardHeader>
            <CardContent>
              <ColumnMappingTable
                columns={preview.columns}
                mapping={mapping}
                onChange={setMapping}
              />
            </CardContent>
          </Card>

          {confirmMutation.isError && (
            <Alert variant="destructive">
              <AlertDescription>
                Ошибка импорта: {(confirmMutation.error as Error).message}
              </AlertDescription>
            </Alert>
          )}

          {confirmMutation.isSuccess && confirmMutation.data && (
            <Card>
              <CardContent className="py-6 space-y-3">
                <div className="flex items-center gap-2">
                  <Badge variant="default">Импорт завершён</Badge>
                  <span className="text-sm">
                    Создано задач: <strong>{confirmMutation.data.tasks_created}</strong>
                  </span>
                </div>
                {confirmMutation.data.errors.length > 0 && (
                  <details>
                    <summary className="cursor-pointer text-sm text-destructive">
                      Ошибки ({confirmMutation.data.errors.length})
                    </summary>
                    <ul className="mt-2 text-sm space-y-1">
                      {confirmMutation.data.errors.slice(0, 20).map((e, i) => (
                        <li key={i}>
                          Строка {e.row}: {e.message}
                        </li>
                      ))}
                    </ul>
                  </details>
                )}
                <div className="flex gap-2">
                  <Link to={`/projects/${projectId}`}>
                    <Button>К проекту</Button>
                  </Link>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setFile(null)
                      setPreview(null)
                      setMapping({})
                      setHeaderRow(undefined)
                    }}
                  >
                    Импортировать ещё
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}

          {!confirmMutation.isSuccess && (
            <div className="flex justify-end">
              <Button
                onClick={handleConfirm}
                disabled={!canConfirm || confirmMutation.isPending}
              >
                {confirmMutation.isPending ? "Импортируем..." : "Импортировать"}
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  )
}