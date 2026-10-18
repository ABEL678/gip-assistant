"""DTO связи между разделами (матрица смежников). spec_week_1.md §6.2.1."""

from pydantic import BaseModel, ConfigDict


class SimilarityLink(BaseModel):
    """Пара разделов, у которых есть что согласовать."""

    model_config = ConfigDict(populate_by_name=True)

    from_section: str  # "АР"
    to_section: str  # "ОВ"
    what: str  # что согласовать
    risk: str  # сигнал риска
