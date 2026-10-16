import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { documentsApi, type Document } from "@/api/documentsApi"
import { type LifecycleStatus } from "@/api/documentEnums"

export function useDocumentsByProject(
  projectId: string,
  lifecycleStatus?: LifecycleStatus,
) {
  return useQuery({
    queryKey: ["documents", projectId, lifecycleStatus],
    queryFn: () => documentsApi.getByProject(projectId, lifecycleStatus),
    enabled: !!projectId,
  })
}

export function useDocument(id: string) {
  return useQuery({
    queryKey: ["document", id],
    queryFn: () => documentsApi.getById(id),
    enabled: !!id,
  })
}

export function useDocumentByGuid(guid: string) {
  return useQuery({
    queryKey: ["document-by-guid", guid],
    queryFn: () => documentsApi.getByGuid(guid),
    enabled: !!guid,
  })
}

export function useCreateDocument(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (
      payload: {
        document_type_id: string
        document_name: string
        cipher: string
        document_kind?: "ПД" | "РД"
        doc_part_type?: "ТЧ" | "ГЧ" | null
        section_code?: string | null
        mark?: string | null
        base_designation?: string | null
        entity_id?: string | null
        task_id?: string | null
        lifecycle_status?: LifecycleStatus
        version_parent_id?: string | null
        replaces_id?: string | null
        replaced_by_id?: string | null
      },
    ) => documentsApi.create(projectId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents", projectId] })
    },
  })
}

export function useUpdateDocument(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      documentId,
      payload,
    }: {
      documentId: string
      payload: Partial<
        Pick<
          Document,
          | "document_name"
          | "document_kind"
          | "doc_part_type"
          | "section_code"
          | "mark"
          | "base_designation"
          | "lifecycle_status"
        >
      >
    }) => documentsApi.update(documentId, payload),
    onSuccess: (_, { documentId }) => {
      queryClient.invalidateQueries({ queryKey: ["documents", projectId] })
      queryClient.invalidateQueries({ queryKey: ["document", documentId] })
    },
  })
}

export function useDeleteDocument(projectId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (documentId: string) => documentsApi.delete(documentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["documents", projectId] })
    },
  })
}
