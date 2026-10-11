import { useEffect, useState } from "react"
import { useParams, useNavigate, Link } from "react-router-dom"
import { ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { FieldList } from "@/components/FieldList"
import { useEntityType, useCreateEntityType, useUpdateEntityType } from "@/hooks/useEntityTypes"
import { type FieldDefinition, type EntityTypeSchema } from "@/api/entityApi"

export function EntityTypeConstructorPage() {
  const { id: projectId, entityTypeId } = useParams<{ id: string; entityTypeId: string }>()
  const navigate = useNavigate()
  const isEdit = !!entityTypeId

  const { data: entityType, isLoading, isError, error } = useEntityType(
    isEdit ? entityTypeId! : "",
  )

  const createMutation = useCreateEntityType(projectId!)
  const updateMutation = useUpdateEntityType(projectId!)

  const [name, setName] = useState("")
  const [icon, setIcon] = useState("📄")
  const [color, setColor] = useState("gray")
  const [description, setDescription] = useState("")
  const [fields, setFields] = useState<FieldDefinition[]>([])

  useEffect(() => {
    if (entityType) {
      setName(entityType.name)
      setIcon(entityType.icon)
      setColor(entityType.color)
      setDescription(entityType.description ?? "")
      setFields(entityType.schema?.fields ?? [])
    }
  }, [entityType])

  const handleSave = () => {
    if (!name.trim()) return

    const payload = {
      name: name.trim(),
      icon: icon || "📄",
      color: color || "gray",
      description: description || null,
      schema: { fields } as EntityTypeSchema,
    }

    if (isEdit && entityTypeId) {
      updateMutation.mutate({ entityTypeId, payload })
    } else {
      createMutation.mutate(payload)
    }
  }

  useEffect(() => {
    if (createMutation.isSuccess || updateMutation.isSuccess) {
      navigate(`/projects/${projectId}/entity-types`)
    }
  }, [createMutation.isSuccess, updateMutation.isSuccess, navigate, projectId])

  if (isLoading) {
    return <div className="text-muted-foreground">Загрузка...</div>
  }

  if (isError) {
    return (
      <Alert variant="destructive">
        <AlertDescription>{(error as Error).message}</AlertDescription>
      </Alert>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Link to={`/projects/${projectId}/entity-types`}>
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">
            {isEdit ? "Редактировать тип" : "Создать тип сущности"}
          </h1>
        </div>
      </div>

      {/* Form */}
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle>Основные параметры</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* name */}
            <div>
              <Label>Название *</Label>
              <Input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Например: Задача"
              />
            </div>

            {/* icon */}
            <div>
              <Label>Иконка (emoji)</Label>
              <Input
                value={icon}
                onChange={(e) => setIcon(e.target.value)}
                placeholder="📄"
              />
            </div>

            {/* color */}
            <div>
              <Label>Цвет</Label>
              <Input
                value={color}
                onChange={(e) => setColor(e.target.value)}
                placeholder="gray"
              />
            </div>

            {/* description */}
            <div>
              <Label>Описание</Label>
              <Textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Описание типа"
                rows={3}
              />
            </div>
          </CardContent>
        </Card>

        {/* FieldList */}
        <FieldList fields={fields} onChange={setFields} />

        {/* Footer buttons */}
        <div className="flex gap-2">
          <Button
            onClick={handleSave}
            disabled={createMutation.isPending || updateMutation.isPending}
          >
            {createMutation.isPending || updateMutation.isPending
              ? "Сохранение..."
              : "Сохранить"}
          </Button>
          <Button
            variant="outline"
            onClick={() => navigate(`/projects/${projectId}/entity-types`)}
          >
            Отмена
          </Button>
        </div>
      </div>
    </div>
  )
}
