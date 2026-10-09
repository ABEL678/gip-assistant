import { useParams, Link } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { projectsApi } from "@/api/projectsApi"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft } from "lucide-react"

export function ProjectPage() {
  const { id } = useParams<{ id: string }>()

  const { data: project, isLoading, isError } = useQuery({
    queryKey: ["project", id],
    queryFn: () => projectsApi.getById(id!),
    enabled: !!id,
  })

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
                <Button>Импорт Excel</Button>
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
              <Button disabled>Скоро</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}