# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 16.10.2026
**Сессия:** 5.4 (закрыта)
**Статус:** закрыта (пауза)

---

## 1. Что было в прошлой сессии (16.10.2026, сессия 5.4)

Закрыта сессия 5.4 (весь уровень: API-клиенты + хуки + UI + роутинг):

- **5.4a:** 5 API-клиентов + 22 хука TanStack Query.
- **5.4b-1:** DocumentsPage + DocumentCard.
- **5.4b-2:** DocumentConstructorPage (форма создания/редактирования).
- **5.4b-3:** Роутинг в App.tsx + секция «Документы» в ProjectPage.
- **5.4c:** DocumentVersionsPage + VersionCard + VersionForm.
- **5.4d:** DocumentLinksPage + LinkCard + LinkForm.
- **5.4e:** Роутинг версий/связей + кнопки в DocumentConstructorPage.

**Итого:** 5 API-клиентов, 22 хука, 10 UI-файлов, 5 маршрутов документов.

**HEAD:** `76a8a3a` (feat(frontend): add versions and links routing + form buttons + context sync).

## 2. Что делаем сейчас

Следующая сессия: Неделя 3 — Библиотека шаблонов (6 типов) + MinIO
ИЛИ: MVP-1.5 XML-модуль.
Решение — на следующей сессии.

## 3. Что дальше

1. Библиотека шаблонов (6 типов: ИД_ПД, ИД_РД, Запросы, Тома, Письма, Протоколы).
2. MinIO AIStor Free — развёртывание + API upload/download.
3. Auth (JWT + Argon2) + Telegram-сводка + деплой на VPS.
4. MVP-1.5: XML-модуль (ТЗ и ПЗ + валидация XSD).
5. MVP-3: LLM-ассистент.

## 4. Что уже в контексте (не надо пересказывать)

- `docs/Дорожная_карта_6.4.md` — стратегия.
- `docs/ТЗ_4.4.md` — ТЗ (включая раздел 16 — ГОСТ-совместимость).
- `docs/context/CONTEXT.md` — резюме проекта (последнее обновление: 5.2f-2).
- `docs/context/TASKS.md` — статус (5.2f-2 закрыт, 122 теста).
- `docs/context/ARCHITECTURE.md` — структура.
- `docs/context/DATABASE.md` — 14 таблиц.
- `docs/context/API.md` — 39 эндпоинтов.
- `docs/context/RULES.md` — правила.
- `docs/context/HANDOFF.md` — эта эстафета.
- `AGENTS.md` — правила для GigaCode.

## 5. Открытые вопросы / блокеры

- [ ] GitHub Actions для авто-генерации DATABASE.md / API.md — не настроены.
- [ ] B027 (TaskRepository.get_by_pair) — техдолг Этапа 1.
- [ ] GigaCode запускает pytest не из корня.
- [ ] GigaCode запускает python -c без активации .venv.
- [ ] GigaCode делает отдельный коммит вместо --amend.
- [ ] GigaCode коммитит в main без feature-ветки.
- [ ] ESLint в frontend не настроен (только tsc).

## 6. Ключи / пути / команды

- **Проект:** `C:\Users\abelo\GIP-Assistant\gip-assistant`
- **Backend:** `cd backend && ..\.venv\Scripts\activate`
- **Backend (запуск):** `uvicorn backend.src.main:app --reload` (из корня)
- **Frontend:** `cd frontend && npm run dev`
- **Тесты:** `pytest backend/tests/ -v` (из корня)
- **Alembic:** `cd backend && ..\.venv\Scripts\activate && alembic current`
- **Ruff:** `.venv\Scripts\activate && ruff check backend/`
- **БД:** Docker `gip_db` на 5555
- **GitHub:** https://github.com/ABEL678/gip-assistant
- **Текущий HEAD:** `76a8a3a` (feat(frontend): add versions and links routing + form buttons + context sync)

## 7. Как продолжить в новом чате

**Первое сообщение в новом чате с DeepSeek (или другим ИИ):**

    Привет. Продолжаем проект «ГИП-Ассистент».

    Прочитай (по порядку):
    1. docs/context/HANDOFF.md — что было и что дальше.
    2. docs/context/CONTEXT.md — что за продукт.
    3. docs/context/TASKS.md — что сделано.
    4. docs/context/ARCHITECTURE.md — структура.
    5. AGENTS.md — правила для GigaCode.

    Дальше:
    - Уровень 1.5 закрыт полностью. Сессия 5.4 закрыта (пауза).
    - Следующая: Неделя 3 (шаблоны+MinIO) ИЛИ MVP-1.5 XML.
    - 10 UI-файлов документов, 5 API-клиентов, 22 хука.
    - Стиль тестов: backend/tests/test_entity_type_service.py.
    - Твоя роль: дать GigaCode промпт, проверить diff, помочь с ошибками.

    Продолжай.

---

**Конец HANDOFF.md.**
