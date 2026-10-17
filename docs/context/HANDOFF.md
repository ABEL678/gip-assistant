**Дата:** 17.10.2026
**Сессия:** 6.6 (закрыта) — канвас: связь (WIP)
**Статус:** закрыта

## §1. Что было в сессии 6.6

- Claude Code установлен (через gpt2giga → GigaChat). Работает в `-p` режиме.
- Пытались починить сохранение связи (edge) на канвасе.
- Backend работает: `PATCH /goals/{id}` — 200, `premise_ids` сохраняются в БД (проверено через Swagger).
- Frontend: `onConnect` добавляет edge, `PATCH` вызывается, но после ухода/возврата edge исчезает.
- `useEffect` с `prevGoalIdsRef` — есть. `useUpdateGoal` — `invalidateQueries(["canvas"])` — нет (или не работает).
- **Статус:** WIP. Связь не сохраняется.

## §2. Что делаем сейчас

Ничего. Ветка `fix/canvas-approve-refetch` — WIP.

## §3. Что дальше

1. **Починить связь (edge)** — в новом чате.
2. Ось времени (план-график).
3. Просрочки, критический путь, агенты, LLM.

## §4. Что в контексте

- DOMAIN.md v1.1.
- Дорожная карта 7.0.
- AGENTS.md v1.2.
- Backend — работает. 193 теста.
- Канвас — работает, кроме сохранения связи.
- Claude Code — установлен, работает через gpt2giga.

## §5. Открытые вопросы

- Как починить связь (React Flow + TanStack Query + БД)?
- Как отображать ось времени?
- Как показывать просрочки?

## §6. Ключи / пути / команды

- **Проект:** `C:\Users\abelo\GIP-Assistant\gip-assistant`
- **Backend:** `uvicorn backend.src.main:app --reload`
- **Frontend:** `cd frontend && npm run dev`
- **gpt2giga:** `gpt2giga` (localhost:8090)
- **Claude Code:** `claude -p --model GigaChat-2-Max --permission-mode bypassPermissions "..."`
- **Тесты:** `pytest backend/tests/ -v`

## §7. Как продолжить в новом чате

«Привет. Проект ГИП-Ассистент. Прочитай:
1. docs/context/DOMAIN.md — онтология.
2. docs/context/HANDOFF.md — эстафета (сессия 6.6).
3. docs/context/CONTEXT.md — резюме.
4. docs/context/TASKS.md — статус.
5. AGENTS.md — правила.

Канвас работает. Связь (edge) — WIP. Нужно починить.
Claude Code установлен, работает через gpt2giga.»
