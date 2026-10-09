import { useQuery } from "@tanstack/react-query"
import { projectsApi } from "@/api/projectsApi"

export function useProjects() {
  return useQuery({
    queryKey: ["projects"],
    queryFn: projectsApi.getAll,
  })
}