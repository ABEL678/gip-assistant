"""MVP-заглушка AI-порта. Ничего не вызывает, возвращает пустышки."""

from uuid import UUID

from backend.src.domain.ports.ai_port import AIPort


class AIStub(AIPort):
    """Заглушка. Используется до MVP-3 (ИИ в продукте отложен)."""

    async def generate_tz_draft(
        self,
        wishes: list[str],
        project_context: str,
    ) -> str:
        return "[AI-stub] Генерация ТЗ появится в MVP-2."

    async def analyze_risks(self, project_id: UUID) -> list[str]:
        return []