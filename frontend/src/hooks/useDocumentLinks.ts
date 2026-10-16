import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  documentLinksApi,
  type DocumentLink,
  type DocumentLinkType,
} from "@/api/documentLinksApi"

export function useDocumentLinks(documentId: string) {
  return useQuery({
    queryKey: ["document-links", documentId],
    queryFn: () => documentLinksApi.listOutgoing(documentId),
    enabled: !!documentId,
  })
}

export function useIncomingDocumentLinks(documentId: string) {
  return useQuery({
    queryKey: ["document-links-incoming", documentId],
    queryFn: () => documentLinksApi.listIncoming(documentId),
    enabled: !!documentId,
  })
}

export function useCreateDocumentLink(documentId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (
      payload: {
        target_document_id: string
        link_type: DocumentLinkType
      },
    ) => documentLinksApi.create(documentId, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["document-links", documentId] })
    },
  })
}

export function useDeleteDocumentLink(documentId: string) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (linkId: string) => documentLinksApi.delete(linkId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["document-links", documentId] })
    },
  })
}
