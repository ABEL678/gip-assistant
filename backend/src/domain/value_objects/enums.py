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
    REVIEW = "REVIEW"            # На проверке
    REWORK = "REWORK"            # На доработке
    DONE = "DONE"                # Завершена
    CANCELLED = "CANCELLED"      # Отменена


class CrossTaskStatus(StrEnum):
    """Статус задания смежнику (ячейка матрицы)."""

    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_INFO = "WAITING_INFO"
    DONE = "DONE"
    OVERDUE = "OVERDUE"


class ExecutorType(StrEnum):
    """Тип исполнителя."""

    STAFF = "STAFF"          # Штатный
    CONTRACTOR = "CONTRACTOR"  # Подрядчик


class UserRole(StrEnum):
    """Роль пользователя."""

    GIP = "GIP"              # Главный инженер проекта
    DESIGNER = "DESIGNER"    # Проектировщик
    OBSERVER = "OBSERVER"    # Наблюдатель


class ImportStatus(StrEnum):
    """Статус импорта Excel."""

    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"