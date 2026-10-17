import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { useParams } from "react-router-dom"
import { usePremises, useUploadPremise } from "@/hooks/usePremises"
import { premiseApi } from "@/api/premiseApi"
import { Button } from "@/components/ui/button"

export function UploadSourcesPage() {
  const { id } = useParams<{ id: string }>()
  const projectId = id!
  const { data: premises, isLoading } = usePremises(projectId)
  const upload = useUploadPremise(projectId)
  const [category, setCategory] = useState("source_data")

  const onDrop = useCallback(
    (files: File[]) => {
      files.forEach((file) => {
        upload.mutate({ file, category })
      })
    },
    [category, upload],
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop })

  const handleDownload = async (premiseId: string, fileName: string) => {
    try {
      const blob = await premiseApi.downloadPremiseFile(premiseId)
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = fileName
      a.click()
      URL.revokeObjectURL(url)
    } catch {
      alert("Ошибка при скачивании файла")
    }
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">Загрузить исходники</h1>

      <div className="flex gap-4 items-center">
        <label className="text-sm font-medium">Категория:</label>
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="border rounded p-2"
        >
          <option value="source_data">Исходные данные</option>
          <option value="contract">Договор</option>
          <option value="tz">ТЗ</option>
          <option value="customer_requirement">Требование заказчика</option>
        </select>
      </div>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition ${
          isDragActive
            ? "border-blue-500 bg-blue-50"
            : "border-gray-300"
        }`}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Отпустите файл здесь...</p>
        ) : (
          <p>Перетащите файлы сюда или кликните для выбора</p>
        )}
      </div>

      {upload.isPending && <p>Загрузка...</p>}
      {upload.isError && (
        <p className="text-red-600">
          Ошибка: {(upload.error as Error).message}
        </p>
      )}

      <div className="space-y-2">
        <h2 className="text-xl font-semibold">
          Загруженные ({premises?.length || 0})
        </h2>
        {isLoading && <p>Загрузка...</p>}
        {premises?.map((p) => {
          const fileSize =
            typeof p.data?.file_size === "number"
              ? Math.round(p.data.file_size / 1024)
              : null
          const fileName =
            typeof p.data?.file_name === "string" ? p.data.file_name : null
          return (
            <div
              key={p.id}
              className="border rounded p-4 flex justify-between items-center"
            >
              <div>
                <p className="font-medium">{p.name}</p>
                <p className="text-sm text-muted-foreground">
                  {p.category}
                  {fileSize !== null ? ` · ${fileSize} КБ` : ""}
                </p>
              </div>
              {fileName && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleDownload(p.id, fileName)}
                >
                  Скачать
                </Button>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
