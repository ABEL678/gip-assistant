import { useState } from "react"
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

interface VersionFormProps {
  onSubmit: (payload: {
    version: string
    file_path: string
    file_name: string
    hash_sha256: string
    format_original: string
    format_archive: string | null
    size_bytes: number
    change_number: number | null
  }) => void
  onCancel: () => void
  isPending: boolean
}

export function VersionForm({ onSubmit, onCancel, isPending }: VersionFormProps) {
  const [version, setVersion] = useState("")
  const [filePath, setFilePath] = useState("")
  const [fileName, setFileName] = useState("")
  const [hashSha256, setHashSha256] = useState("")
  const [formatOriginal, setFormatOriginal] = useState("")
  const [formatArchive, setFormatArchive] = useState("")
  const [sizeBytes, setSizeBytes] = useState("")
  const [changeNumber, setChangeNumber] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!version.trim() || !filePath.trim() || !fileName.trim()
        || !hashSha256.trim() || !formatOriginal.trim() || !sizeBytes.trim()) {
      return
    }

    onSubmit({
      version: version.trim(),
      file_path: filePath.trim(),
      file_name: fileName.trim(),
      hash_sha256: hashSha256.trim(),
      format_original: formatOriginal.trim(),
      format_archive: formatArchive.trim() || null,
      size_bytes: Number(sizeBytes) || 0,
      change_number: changeNumber.trim() ? Number(changeNumber) : null,
    })
  }

  return (
    <form onSubmit={handleSubmit}>
      <Card>
        <CardHeader>
          <CardTitle>Новая версия</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* version */}
          <div>
            <Label>Версия *</Label>
            <Input
              value={version}
              onChange={(e) => setVersion(e.target.value)}
              placeholder="v1.0"
            />
          </div>

          {/* file_path */}
          <div>
            <Label>Путь к файлу *</Label>
            <Input
              value={filePath}
              onChange={(e) => setFilePath(e.target.value)}
              placeholder="/files/..."
            />
          </div>

          {/* file_name */}
          <div>
            <Label>Имя файла *</Label>
            <Input
              value={fileName}
              onChange={(e) => setFileName(e.target.value)}
              placeholder="document.pdf"
            />
          </div>

          {/* hash_sha256 */}
          <div>
            <Label>Хэш SHA-256 *</Label>
            <Input
              value={hashSha256}
              onChange={(e) => setHashSha256(e.target.value)}
              placeholder="64 символа (hex)"
            />
          </div>

          {/* format_original */}
          <div>
            <Label>Формат *</Label>
            <Input
              value={formatOriginal}
              onChange={(e) => setFormatOriginal(e.target.value)}
              placeholder="pdf"
            />
          </div>

          {/* format_archive */}
          <div>
            <Label>Архивный формат</Label>
            <Input
              value={formatArchive}
              onChange={(e) => setFormatArchive(e.target.value)}
              placeholder="zip"
            />
          </div>

          {/* size_bytes */}
          <div>
            <Label>Размер (байты) *</Label>
            <Input
              type="number"
              value={sizeBytes}
              onChange={(e) => setSizeBytes(e.target.value)}
              placeholder="0"
            />
          </div>

          {/* change_number */}
          <div>
            <Label>Номер изменения</Label>
            <Input
              type="number"
              value={changeNumber}
              onChange={(e) => setChangeNumber(e.target.value)}
              placeholder=""
            />
          </div>
        </CardContent>
        <CardFooter className="gap-2">
          <Button type="submit" disabled={isPending}>
            {isPending ? "Добавление..." : "Добавить версию"}
          </Button>
          <Button variant="outline" type="button" onClick={onCancel}>
            Отмена
          </Button>
        </CardFooter>
      </Card>
    </form>
  )
}
