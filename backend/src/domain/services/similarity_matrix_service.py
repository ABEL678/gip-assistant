"""Матрица смежников (spec_week_1.md §6.2.1).

10 связей между разделами. Система предлагает — ГИП утверждает.
Работает на правилах, без LLM.
"""

import re
from uuid import UUID

from backend.src.application.dto.similarity_link import SimilarityLink
from backend.src.domain.ports.repositories import PremiseRepository
from backend.src.domain.value_objects.enums import PremiseCategory

_SECTION_RE = re.compile(r"^[А-ЯA-Z]{2,6}$")


class SimilarityMatrixService:
    """Правила вывода связей между разделами (spec_week_1.md §6.2.1)."""

    MATRIX: dict[tuple[str, str], dict[str, str]] = {
        ("АР", "ОВ"): {
            "what": "Отверстия и шахты под воздуховоды, венткамеры, дымоудаление",
            "risk": "Пробивка по факту, простой, переделка узла",
        },
        ("АР", "КЖ"): {
            "what": "Проёмы в несущих, нагрузки от перегородок, оси и отметки",
            "risk": "Пересчёт узла, усиление",
        },
        ("АР", "ВК"): {
            "what": "Стояки, короба, санузлы, гидроизоляция, уклоны полов",
            "risk": "Перенос санузла на РД",
        },
        ("АР", "ЭО"): {
            "what": "Щитовые, ниши под щиты, трассы, помещения связи",
            "risk": "Перепланировка под щит",
        },
        ("АР", "ПБ"): {
            "what": "Пути эвакуации, преграды, огнестойкость, зоны безопасности",
            "risk": "Возврат с экспертизы",
        },
        ("АР", "ПЗУ"): {
            "what": "Посадка здания, отметки входов, отступы, благоустройство",
            "risk": "Несоответствие ГПЗУ",
        },
        ("ОВ", "КЖ"): {
            "what": "Нагрузки на перекрытия от оборудования (200 кг – 3 т)",
            "risk": "Пересчёт плиты, усиление",
        },
        ("ОВ", "ЭО"): {
            "what": "Электропитание: мощность, фазы, IP, способ ввода",
            "risk": "Переделка кабеля, щита",
        },
        ("ОВ", "ТХ"): {
            "what": "Категории помещений по СП 12.13130",
            "risk": "Противодымка не заложена",
        },
        ("ОВ", "ПБ"): {
            "what": "Противодымная вентиляция по СП 7.13130",
            "risk": "Возврат с экспертизы",
        },
    }

    def __init__(self, premise_repo: PremiseRepository) -> None:
        self._premise_repo = premise_repo

    async def find_links(self, project_id: UUID) -> list[SimilarityLink]:
        """Найти разделы в договоре/ТЗ проекта, вернуть пересечения с MATRIX."""
        premises = await self._premise_repo.list_by_project(project_id)
        relevant = [
            p
            for p in premises
            if p.category in (PremiseCategory.CONTRACT, PremiseCategory.TZ)
        ]

        sections: set[str] = set()

        for premise in relevant:
            # (B) sections поле — список строк
            sections_field = premise.data_field("sections")
            sections_present = (
                sections_field is not None
                and isinstance(sections_field.value, list)
                and len(sections_field.value) > 0
            )
            if sections_present:
                for s in sections_field.value:
                    if isinstance(s, str) and _SECTION_RE.match(s):
                        sections.add(s)
                # Приоритет B: не смотрим остальные поля
                continue

            # (C) сканируем строковые значения data
            for key in premise.data:
                if key == "sections":
                    continue
                f = premise.data_field(key)
                if f is None:
                    continue
                if isinstance(f.value, str) and _SECTION_RE.match(f.value):
                    sections.add(f.value)
                elif isinstance(f.value, list):
                    for s in f.value:
                        if isinstance(s, str) and _SECTION_RE.match(s):
                            sections.add(s)

        # Сопоставляем с MATRIX
        links: list[SimilarityLink] = []
        for (a, b), meta in self.MATRIX.items():
            if a in sections and b in sections:
                links.append(
                    SimilarityLink(
                        from_section=a,
                        to_section=b,
                        what=meta["what"],
                        risk=meta["risk"],
                    )
                )

        return links
