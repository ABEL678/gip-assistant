import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  documentVersionsApi,
  type DocumentVersion,
} from "@/api/documentVersionsApi"

export function useDocumentVersions(documentId: string) {
  return useQuery({
    queryKey: ["document-versions", documentId],
    queryFn: () => documentVersionsApi.listByDocument(documentId),
    enabled: !!documentId,
  })
}

export function useCurrentDocumentVersion(documentId: string) {
  return useQuery({
    queryKey: ["document-version-current", documentId],
    queryFn: () => documentVersionsApi.getCurrent(documentId),
    enabled: !!documentId,
  })
}

export function useDocumentVersion(versionId: string) {
  return useQuery({
    queryKey: ["document-version", versionId],
    queryFn: () => documentVersionsApi.getById(versionId),
    enabled: !!versionId,
  })
}

export function useCreateDocumentVersion(documentId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (
      payload: {
        version: string
        file_path: string
        file_name: string
        hash_sha256: string
        format_original: string
        format_archive?: string | null
        size_bytes: number
        change_number?: number | null
      },
    ) => documentVersionsApi.create(documentId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["document-versions", documentId] })
    },
  })
}

export function useSetCurrentDocumentVersion(documentId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (versionId: string) =>
      documentVersionsApi.setCurrent(documentId, versionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["document-versions", documentId] })
      queryClient.invalidateQueries({ queryKey: ["document-version-current", documentId] })
    },
  })
}

export function useDeleteDocumentVersion(documentId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (versionId: string) => documentVersionsApi.delete(versionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["document-versions", documentId] })
    },
  })
}
