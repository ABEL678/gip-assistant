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
import { DocumentConstructorPage } from "@/pages/DocumentConstructorPage"
import { DocumentLinksPage } from "@/pages/DocumentLinksPage"
import { DocumentVersionsPage } from "@/pages/DocumentVersionsPage"
import { DocumentsPage } from "@/pages/DocumentsPage"
import { PremisesPage } from "@/pages/PremisesPage"
import { GoalsPage } from "@/pages/GoalsPage"
import { UploadSourcesPage } from "@/pages/UploadSourcesPage"
import { ProjectCanvasPage } from "@/pages/ProjectCanvasPage"
import { TimelineDemoPage } from "@/pages/TimelineDemoPage"
import { CanvasDemoPage } from "@/pages/CanvasDemoPage"
import { SkeletonDemoPage } from "@/pages/SkeletonDemoPage"

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
          <Route path="projects/:id/documents" element={<DocumentsPage />} />
          <Route path="projects/:id/documents/new" element={<DocumentConstructorPage />} />
          <Route path="projects/:id/documents/:docId/edit" element={<DocumentConstructorPage />} />
          <Route path="projects/:id/documents/:docId/versions" element={<DocumentVersionsPage />} />
          <Route path="projects/:id/documents/:docId/links" element={<DocumentLinksPage />} />
          <Route path="projects/:id/premises" element={<PremisesPage />} />
          <Route path="projects/:id/upload" element={<UploadSourcesPage />} />
          <Route path="projects/:id/canvas" element={<ProjectCanvasPage />} />
          <Route path="projects/:id/timeline-demo" element={<TimelineDemoPage />} />
          <Route path="projects/:id/canvas-demo" element={<CanvasDemoPage />} />
          <Route path="projects/:id/skeleton-demo" element={<SkeletonDemoPage />} />
          <Route path="projects/:id/goals" element={<GoalsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App