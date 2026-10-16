import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { documentTypesApi, type DocumentType } from "@/api/documentTypesApi"

export function useDocumentTypes() {
  return useQuery({
    queryKey: ["document-types"],
    queryFn: documentTypesApi.getAll,
  })
}

export function useDocumentType(id: string) {
  return useQuery({
    queryKey: ["document-type", id],
    queryFn: () => documentTypesApi.getById(id),
    enabled: !!id,
  })
}

export function useDocumentTypeByCode(code: string) {
  return useQuery({
    queryKey: ["document-type-by-code", code],
    queryFn: () => documentTypesApi.getByCode(code),
    enabled: !!code,
  })
}

export function useCreateDocumentType() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (
      payload: {
        code: string
        name: string
        description?: string | null
        gost_code?: string | null
      },
    ) => documentTypesApi.create(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["document-types"] })
    },
  })
}

export function useUpdateDocumentType() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({
      id,
      payload,
    }: {
      id: string
      payload: Partial<Pick<DocumentType, "name" | "description" | "gost_code">>
    }) => documentTypesApi.update(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["document-types"] })
    },
  })
}

export function useDeleteDocumentType() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => documentTypesApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["document-types"] })
    },
  })
}
