# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** [DD.MM.YYYY]
**Сессия:** [номер]
**Статус:** [в работе / закрыта]

---

## 1. Что было в прошлой сессии

[краткое описание — 3-5 пунктов]

## 2. Что делаем сейчас

- **Задача:** [название]
- **Файлы:** [список]
- **Прогресс:** [% или статус]

## 3. Что дальше

[следующие шаги по порядку]

## 4. Что уже в контексте (не надо пересказывать)

- `docs/Дорожная_карта_6.4.md` — стратегия.
- `docs/ТЗ_4.4.md` — ТЗ.
- `docs/context/CONTEXT.md` — резюме.
- `docs/context/TASKS.md` — статус.
- `docs/context/ARCHITECTURE.md` — структура.
- `docs/context/DATABASE.md` — схема БД.
- `docs/context/API.md` — эндпоинты.
- `docs/context/RULES.md` — правила.
- `AGENTS.md` — правила для GigaCode.

## 5. Открытые вопросы / блокеры

- [ ] [вопрос 1]

## 6. Ключи / пути / команды

- Проект: `C:\Users\abelo\GIP-Assistant\gip-assistant`
- Backend: `cd backend && ..\.venv\Scripts\activate`
- Frontend: `cd frontend && npm run dev`
- Тесты: `pytest backend/tests/ -v`
- Alembic: `cd backend && ..\.venv\Scripts\activate && alembic current`
- БД: Docker `gip_db` на 5555
- GitHub: https://github.com/ABEL678/gip-assistant

## 7. Как продолжить в новом чате

Первое сообщение:

    Привет. Продолжаем проект «ГИП-Ассистент».
    Прочитай:
    1. docs/context/HANDOFF.md
    2. docs/context/CONTEXT.md
    3. docs/context/TASKS.md
    Дальше — продолжай с того места, где остановились.

---

**Конец HANDOFF.md.**
