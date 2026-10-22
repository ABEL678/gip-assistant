"""Все Enum'ы домена ГИП-Ассистента (см. ТЗ 3.0, раздел 4.2)."""

from enum import StrEnum


class StageType(StrEnum):
    """Стадия проекта."""

    EP = "EP"  # Эскизный проект
    PP = "PP"  # Предварительный Проект
    PD = "PD"  # Проектная документация
    RD = "RD"  # Рабочая документация (стадия РД)


class TaskStatus(StrEnum):
    """Статус задачи."""

    NOT_STARTED = "NOT_STARTED"  # Не начата
    IN_PROGRESS = "IN_PROGRESS"  # В работе
    REVIEW = "REVIEW"  # На проверке
    REWORK = "REWORK"  # На доработке
    DONE = "DONE"  # Завершена
    CANCELLED = "CANCELLED"  # Отменена


class CrossTaskStatus(StrEnum):
    """Статус задания смежнику (ячейка матрицы)."""

    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_INFO = "WAITING_INFO"
    DONE = "DONE"
    OVERDUE = "OVERDUE"


class ExecutorType(StrEnum):
    """Тип исполнителя."""

    STAFF = "STAFF"  # Штатный
    CONTRACTOR = "CONTRACTOR"  # Подрядчик


class UserRole(StrEnum):
    """Роль пользователя."""

    GIP = "GIP"  # Главный инженер проекта
    DESIGNER = "DESIGNER"  # Проектировщик
    OBSERVER = "OBSERVER"  # Наблюдатель


class ImportStatus(StrEnum):
    """Статус импорта Excel."""

    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


class PremiseCategory(StrEnum):
    """Категория вводной (Premise)."""

    CONTRACT = "contract"  # Договор
    TZ = "tz"  # ТЗ
    CUSTOMER_REQUIREMENT = "customer_requirement"  # Требования Заказчика
    SOURCE_DATA = "source_data"  # Исходные данные
    NORM = "norm"  # Нормативные документы
    NPA = "npa"  # НПА
    BUREAUCRACY = "bureaucracy"  # Гос. бюрократия
    INTERNAL = "internal"  # Внутренние причины


class GoalState(StrEnum):
    """Состояние цели (Goal)."""

    PLAN = "plan"  # В плане
    IN_PROGRESS = "in_progress"  # В работе
    ACHIEVED = "achieved"  # Достигнута
    CANCELLED = "cancelled"  # Отменена


class VerificationStatus(StrEnum):
    """Статус проверки (verification_status). DOMAIN.md §4.4.1."""

    CONFIRMED = "confirmed"  # Подтверждено (есть доказательство)
    NOT_CONFIRMED = "not_confirmed"  # Не соответствует (есть доказательство обратного)
    REQUIRES_CHECK = "requires_check"  # Требует проверки (данных достаточно, вывод не авто)
    NO_DATA = "no_data"  # Нет данных (сигнал к RFI, не ошибка)


class ChangeStatus(StrEnum):
    """Статус изменения между ревизиями."""

    ADDED = "added"
    REMOVED = "removed"
    CHANGED = "changed"
    UNCHANGED = "unchanged"


class RevisionDecisionType(StrEnum):
    """Решение по ревизии (6 статусов)."""

    ACCEPTED = "accepted"
    ACCEPTED_WITH_FRAME = "accepted_with_frame"
    REMARK = "remark"
    REJECTED = "rejected"
    MOVED = "moved"
    DEADLINE = "deadline"


class ProjectStandardType(StrEnum):
    """Тип стандарта проекта (spec_week_1.md §2.4)."""

    DEADLINE = "deadline"
    COMPOSITION = "composition"
    FORMAT = "format"


class ActionState(StrEnum):
    """Состояние действия (Action)."""

    PLAN = "plan"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


class DecisionState(StrEnum):
    """Состояние решения (Decision)."""

    PLAN = "plan"  # В плане
    IN_PROGRESS = "in_progress"  # В работе
    ACCEPTED = "accepted"  # Принято
    CANCELLED = "cancelled"  # Отменено
    REPLACED = "replaced"  # Заменено
