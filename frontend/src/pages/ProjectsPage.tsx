import { Link } from "react-router-dom"
import { useProjects } from "@/hooks/useProjects"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

export function ProjectsPage() {
  const { data: projects, isLoading, isError, error, refetch } = useProjects()

  if (isLoading) {
    return <div className="text-muted-foreground">Загрузка проектов...</div>
  }

  if (isError) {
    return (
      <div>
        <p className="text-destructive mb-4">
          Ошибка загрузки: {(error as Error).message}
        </p>
        <Button onClick={() => refetch()}>Повторить</Button>
      </div>
    )
  }

  if (!projects || projects.length === 0) {
    return (
      <div>
        <p className="text-muted-foreground mb-4">Проектов пока нет.</p>
        <p className="text-sm text-muted-foreground">
          Добавь проект через Swagger: POST /api/projects
        </p>
      </div>
    )
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Проекты</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {projects.map((project) => (
          <Link key={project.id} to={`/projects/${project.id}`}>
            <Card className="hover:border-primary/50 transition-colors cursor-pointer h-full">
              <CardHeader>
                <div className="flex items-start justify-between gap-2">
                  <CardTitle className="text-lg">{project.name}</CardTitle>
                  <Badge variant="secondary">{project.stage}</Badge>
                </div>
              </CardHeader>
              <CardContent className="text-sm text-muted-foreground space-y-1">
                <p>
                  <span className="font-medium text-foreground">Код:</span>{" "}
                  {project.code}
                </p>
                {project.client && (
                  <p>
                    <span className="font-medium text-foreground">Заказчик:</span>{" "}
                    {project.client}
                  </p>
                )}
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  )
}