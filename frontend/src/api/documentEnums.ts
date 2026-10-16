// ====== Enum-типы для ГОСТ-документов ======

export type DocumentKind = "ПД" | "РД"

export type DocPartType = "ТЧ" | "ГЧ"

export type LifecycleStatus =
  | "DRAFT"
  | "IN_REVIEW"
  | "NORMOCONTROL"
  | "APPROVED"
  | "ARCHIVED"
  | "ANNULLED"
  | "REPLACED"

export type DocumentLinkType = "appendix" | "reference" | "replaces" | "version_of"
