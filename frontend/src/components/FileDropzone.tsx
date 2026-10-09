import { useCallback } from "react"
import { useDropzone } from "react-dropzone"
import { Upload } from "lucide-react"

interface FileDropzoneProps {
  onFileSelected: (file: File) => void
  disabled?: boolean
  selectedFile?: File | null
}

export function FileDropzone({
  onFileSelected,
  disabled = false,
  selectedFile,
}: FileDropzoneProps) {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onFileSelected(acceptedFiles[0])
      }
    },
    [onFileSelected],
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
      "application/vnd.ms-excel.sheet.macroEnabled.12": [".xlsm"],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024,
    disabled,
  })

  return (
    <div
      {...getRootProps()}
      className={`
        border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
        transition-colors
        ${isDragActive ? "border-primary bg-primary/5" : "border-border hover:border-primary/50"}
        ${disabled ? "opacity-50 cursor-not-allowed" : ""}
      `}
    >
      <input {...getInputProps()} />
      <Upload className="mx-auto h-10 w-10 text-muted-foreground mb-3" />
      {selectedFile ? (
        <div className="space-y-1">
          <p className="font-medium">{selectedFile.name}</p>
          <p className="text-sm text-muted-foreground">
            {(selectedFile.size / 1024).toFixed(1)} KB — нажмите, чтобы заменить
          </p>
        </div>
      ) : (
        <div className="space-y-1">
          <p className="font-medium">
            {isDragActive ? "Отпустите файл здесь" : "Перетащите Excel-файл сюда"}
          </p>
          <p className="text-sm text-muted-foreground">
            или нажмите для выбора. Поддерживается .xlsx / .xlsm, до 10 MB
          </p>
        </div>
      )}
    </div>
  )
}