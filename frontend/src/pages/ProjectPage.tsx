import { useParams, Link, useNavigate } from "react-router-dom"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { projectsApi } from "@/api/projectsApi"
import { entityApi } from "@/api/entityApi"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, Upload, Grid3x3, Plus } from "lucide-react"
import { TaskList } from "@/components/TaskList"
import { EntityTypeCard } from "@/components/EntityTypeCard"

export function ProjectPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const { data: project, isLoading, isError } = useQuery({
    queryKey: ["project", id],
    queryFn: () => projectsApi.getById(id!),
    enabled: !!id,
  })

  const { data: entityTypes, isLoading: typesLoading } = useQuery({
    queryKey: ["entity-types", id],
    queryFn: () => entityApi.getTypesByProject(id!),
    enabled: !!id,
  })

  const deleteMutation = useMutation({
    mutationFn: (entityTypeId: string) => entityApi.deleteType(entityTypeId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["entity-types", id] })
    },
  })

  const handleDelete = (entityTypeId: string) => {
    if (window.confirm("Удалить этот тип сущности?")) {
      deleteMutation.mutate(entityTypeId)
    }
  }

  if (isLoading) {
    return <div className="text-muted-foreground">Загрузка проекта...</div>
  }

  if (isError || !project) {
    return (
      <div>
        <p className="text-destructive mb-4">Проект не найден.</p>
        <Link to="/">
          <Button variant="outline">← К списку проектов</Button>
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link to="/">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div>
          <h1 className="text-2xl font-bold">{project.name}</h1>
          <p className="text-sm text-muted-foreground">
            Код: {project.code} • Стадия: {project.stage}
          </p>
        </div>
        <Badge className="ml-auto" variant="secondary">
          {project.stage}
        </Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Импорт Excel</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Загрузите Excel-файл с задачами проекта.
            <div className="mt-4">
              <Link to={`/projects/${id}/import`}>
                <Button>
                  <Upload className="h-4 w-4 mr-2" />
                  Импорт Excel
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Матрица смежников</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            Просмотр заданий между разделами.
            <div className="mt-4">
              <Link to={`/projects/${id}/matrix`}>
                <Button>
                  <Grid3x3 className="h-4 w-4 mr-2" />
                  Открыть матрицу
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Задачи проекта</CardTitle>
        </CardHeader>
        <CardContent>
          <TaskList projectId={id!} />
        </CardContent>
      </Card>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">Типы сущностей</h2>
          <Link to={`/projects/${id}/entity-types/new`}>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Добавить тип
            </Button>
          </Link>
        </div>

        {typesLoading ? (
          <p className="text-muted-foreground">Загрузка...</p>
        ) : !entityTypes || entityTypes.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            Пока нет типов сущностей
            <div className="mt-4">
              <Link to={`/projects/${id}/entity-types/new`}>
                <Button variant="outline">Создать первый тип</Button>
              </Link>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {entityTypes.map((type) => (
              <EntityTypeCard
                key={type.id}
                entityType={type}
                onEdit={(entityTypeId) =>
                  navigate(`/projects/${id}/entity-types/${entityTypeId}/edit`)
                }
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}