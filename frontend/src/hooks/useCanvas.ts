import { useQuery, type UseQueryResult } from "@tanstack/react-query"
import { canvasApi } from "@/api/canvasApi"

export function useCanvas(projectId: string): UseQueryResult<{
  premises: import("@/api/premiseApi").Premise[]
  goals: import("@/api/goalApi").Goal[]
  proposals: import("@/api/goalApi").GoalProposal[]
}> {
  return useQuery({
    queryKey: ["canvas", projectId],
    queryFn: () => canvasApi.fetchCanvas(projectId),
    enabled: !!projectId,
  })
}
