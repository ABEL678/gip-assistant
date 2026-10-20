import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  revisionApi,
  type RevisionCreate,
  type ChangeCreate,
  type RevisionDecisionCreate,
  type StopFlagCreate,
} from "@/api/revisionApi"

// ====== Revisions ======

export function useRevisions(documentId: string) {
  return useQuery({
    queryKey: ["revisions", documentId],
    queryFn: () => revisionApi.listRevisions(documentId),
    enabled: !!documentId,
  })
}

export function useRevision(revisionId: string) {
  return useQuery({
    queryKey: ["revision", revisionId],
    queryFn: () => revisionApi.getRevision(revisionId),
    enabled: !!revisionId,
  })
}

export function useCreateRevision(documentId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: RevisionCreate) =>
      revisionApi.createRevision(documentId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["revisions", documentId] })
    },
  })
}

export function useDeleteRevision(documentId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (revisionId: string) => revisionApi.deleteRevision(revisionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["revisions", documentId] })
    },
  })
}

// ====== Changes ======

export function useChanges(revisionId: string) {
  return useQuery({
    queryKey: ["changes", revisionId],
    queryFn: () => revisionApi.listChanges(revisionId),
    enabled: !!revisionId,
  })
}

export function useCreateChange(revisionId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: ChangeCreate) =>
      revisionApi.createChange(revisionId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["changes", revisionId] })
    },
  })
}

// ====== Decisions ======

export function useCreateDecision() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      changeId,
      payload,
    }: {
      changeId: string
      payload: RevisionDecisionCreate
    }) => revisionApi.createDecision(changeId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["changes"] })
    },
  })
}

// ====== Stop Flags ======

export function useCreateStopFlag(revisionId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (payload: StopFlagCreate) =>
      revisionApi.createStopFlag(revisionId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["revision", revisionId] })
    },
  })
}
