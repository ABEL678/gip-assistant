import { useParams, Link } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { projectsApi } from "@/api/projectsApi"
import { premiseApi } from "@/api/premiseApi"
import { goalApi } from "@/api/goalApi"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, Upload, Grid3x3, Plus } from "lucide-react"
import { TaskList } from "@/components/TaskList"
import { useDocumentsByProject } from "@/hooks/useDocuments"

import { DocumentCard } from "@/components/DocumentCard"

export function ProjectPage() {
  const { id } = useParams<{ id: string }>()

  const { data: project, isLoading, isError } = useQuery({
    queryKey: ["project", id],
    queryFn: () => projectsApi.getById(id!),
    enabled: !!id,
  })

  const { data: documents, isLoading: documentsLoading } = useDocumentsByProject(id!)

  const { data: premises, isLoading: premisesLoading } = useQuery({
    queryKey: ["premises", id],
    queryFn: () => premiseApi.fetchPremises(id!),
    enabled: !!id,
  })

  const { data: goals } = useQuery({
    queryKey: ["goals", id],
    queryFn: () => goalApi.fetchGoals(id!),
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
          <h2 className="text-xl font-semibold">Документы</h2>
          <div className="flex gap-2">
            <Link to={`/projects/${id}/documents`}>
              <Button variant="outline">Все документы</Button>
            </Link>
            <Link to={`/projects/${id}/documents/new`}>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Создать документ
              </Button>
            </Link>
          </div>
        </div>

        {documentsLoading ? (
          <p className="text-muted-foreground">Загрузка...</p>
        ) : !documents || documents.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            Пока нет документов
            <div className="mt-4">
              <Link to={`/projects/${id}/documents/new`}>
                <Button variant="outline">Создать первый документ</Button>
              </Link>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {documents.slice(0, 6).map((doc) => (
              <DocumentCard key={doc.id} document={doc} />
            ))}
          </div>
        )}
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">
            Вводные <span className="text-muted-foreground">({premises?.length ?? 0})</span>
          </h2>
          <div className="flex gap-2">
            <Link to={`/projects/${id}/premises`}>
              <Button variant="outline">Все вводные</Button>
            </Link>
            <Link to={`/projects/${id}/premises`}>
              <Button>
                <Plus className="h-4 w-4 mr-2" />
                Добавить вводную
              </Button>
            </Link>
          </div>
        </div>

        {premisesLoading ? (
          <p className="text-muted-foreground">Загрузка...</p>
        ) : !premises || premises.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            Пока нет вводных
            <div className="mt-4">
              <Link to={`/projects/${id}/premises`}>
                <Button variant="outline">Добавить вводную</Button>
              </Link>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {premises.slice(0, 3).map((p) => (
              <div key={p.id} className="border rounded-lg p-3">
                <div className="font-medium">{p.name}</div>
                <div className="text-sm text-muted-foreground">{p.category}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">
            Цели <span className="text-muted-foreground">({goals?.length ?? 0})</span>
          </h2>
          <Link to={`/projects/${id}/goals`}>
            <Button variant="outline">Все цели</Button>
          </Link>
        </div>

        {premisesLoading ? (
          <p className="text-muted-foreground">Загрузка...</p>
        ) : !goals || goals.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            Пока нет целей
            <div className="mt-4">
              <Link to={`/projects/${id}/goals`}>
                <Button variant="outline">Перейти к целям</Button>
              </Link>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {goals.slice(0, 3).map((g) => (
              <div key={g.id} className="border rounded-lg p-3">
                <div className="font-medium">{g.formulation}</div>
                <div className="text-sm text-muted-foreground">{g.state}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}