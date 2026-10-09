import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Layout } from "@/components/Layout"
import { ProjectsPage } from "@/pages/ProjectsPage"
import { ProjectPage } from "@/pages/ProjectPage"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<ProjectsPage />} />
          <Route path="projects/:id" element={<ProjectPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App