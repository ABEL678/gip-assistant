import { useQuery } from "@tanstack/react-query"
import { canvasApi } from "@/api/canvasApi"

export function useCanvas(projectId: string) {
  return useQuery({
    queryKey: ["canvas", projectId],
    queryFn: () => canvasApi.fetchCanvas(projectId),
    enabled: !!projectId,
  })
}
