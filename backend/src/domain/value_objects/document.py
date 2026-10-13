"""Value objects для модели ГОСТ-документов (ГОСТ Р 21.101-2026)."""

from enum import Enum


class DocumentKind(str, Enum):
    """Вид документации (ГОСТ Р 21.101-2026, 4.1, 4.2)."""

    PD = "ПД"  # проектная документация
    RD = "РД"  # рабочая документация


class DocPartType(str, Enum):
    """Часть документа (ГОСТ Р 21.101-2026, 4.1.3.3, новое в 2026)."""

    TCH = "ТЧ"  # текстовая часть
    GCH = "ГЧ"  # графическая часть


class LifecycleStatus(str, Enum):
    """Жизненный цикл документа (ГОСТ Р 21.101-2026, 7.1-7.5)."""

    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    NORMOCONTROL = "NORMOCONTROL"
    APPROVED = "APPROVED"
    ARCHIVED = "ARCHIVED"
    ANNULLED = "ANNULLED"
    REPLACED = "REPLACED"


class DocumentLinkType(str, Enum):
    """Тип связи между документами (ГОСТ Р 21.101-2026, 4.3.3)."""

    APPENDIX = "appendix"
    REFERENCE = "reference"
    REPLACES = "replaces"
    VERSION_OF = "version_of"
