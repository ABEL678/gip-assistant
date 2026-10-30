"""LLM-адаптеры (6.14b).

Наружу экспортируется только диспетчер: базовые адаптеры не должны
подключаться в DI/пайплайн напрямую — они не проверяют светофор.
"""

from backend.src.adapters.llm.runtime import RuntimeLLMAdapter

__all__ = ["RuntimeLLMAdapter"]
