import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Layout } from "@/components/Layout"
import { ProjectsPage } from "@/pages/ProjectsPage"
import { ProjectPage } from "@/pages/ProjectPage"
import { ImportExcelPage } from "@/pages/ImportExcelPage"
import { MatrixPage } from "@/pages/MatrixPage"
import { CrossTaskTasksPage } from "@/pages/CrossTaskTasksPage"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<ProjectsPage />} />
          <Route path="projects/:id" element={<ProjectPage />} />
          <Route path="projects/:id/import" element={<ImportExcelPage />} />
          <Route path="projects/:id/matrix" element={<MatrixPage />} />
          <Route path="projects/:id/matrix" element={<MatrixPage />} />
          <Route path="projects/:id/matrix/:crossTaskId" element={<CrossTaskTasksPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App