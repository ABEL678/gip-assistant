import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Layout } from "@/components/Layout"
import { ProjectsPage } from "@/pages/ProjectsPage"
import { ProjectPage } from "@/pages/ProjectPage"
import { ImportExcelPage } from "@/pages/ImportExcelPage"
import { MatrixPage } from "@/pages/MatrixPage"
import { CrossTaskTasksPage } from "@/pages/CrossTaskTasksPage"
import { EntityTypesPage } from "@/pages/EntityTypesPage"
import { EntityTypeConstructorPage } from "@/pages/EntityTypeConstructorPage"
import { EntitiesPage } from "@/pages/EntitiesPage"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<ProjectsPage />} />
          <Route path="projects/:id" element={<ProjectPage />} />
          <Route path="projects/:id/import" element={<ImportExcelPage />} />
          <Route path="projects/:id/matrix" element={<MatrixPage />} />
          <Route path="projects/:id/matrix/:crossTaskId" element={<CrossTaskTasksPage />} />
          <Route path="projects/:id/entity-types" element={<EntityTypesPage />} />
          <Route path="projects/:id/entity-types/new" element={<EntityTypeConstructorPage />} />
          <Route path="projects/:id/entity-types/:entityTypeId/edit" element={<EntityTypeConstructorPage />} />
          <Route path="projects/:id/entity-types/:entityTypeId" element={<EntitiesPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App