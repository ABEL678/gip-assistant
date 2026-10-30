# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 27.10.2026
**Сессия:** 6.12d → фиксация ручной проверки
**Статус:** Веха 3 закрыта. Веха 4: 6.12d — закрыта (проверена вручную), следующий шаг — 6.14a–d (админка LLM). 450 тестов, frontend build зелёный.

---

## 1. Что было в прошлой сессии

**6.12c — RFI-эндпоинты + DI (24.10.2026):**

- ✅ `routes/rfis.py` — 8 эндпоинтов: CRUD + proposals + from-proposal + escalate.
- ✅ Порядок: `/proposals` и `/from-proposal` объявлены ПЕРЕД `/{id}`.
- ✅ Ошибки: `ValueError` → 400, `IntegrityError` → 409, not found → 404.
- ✅ Регистрация в `routes/__init__.py` + `main.py`.
- ✅ 14 тестов роутов (httpx.AsyncClient + ASGITransport).
- ✅ **450 тестов pytest.**

**Реорганизация документации (25.10.2026):**

- ✅ Создан `docs/README.md` — карта документации (4 уровня).
- ✅ `GIGACODE.md` влит в `AGENTS.md` v1.4; `GIGACODE.md` — заглушка.
- ✅ `AUDIT_PROMPTS.md` → `docs/tools/`.
- ✅ `docs/context/README.md` удалён (дубль), полезное — в `docs/README.md`.
- ✅ Планы 6.12b/6.12c → `docs/tasks/archive/`.
- ✅ `CONTEXT.md` сокращён до резюме; история — в `TASKS.md` §5.

---

## 2. Что делаем сейчас

**Код не в работе.** **6.12d (UI RFI) — закрыта (проверена вручную, 27.10.2026).**
Следующий шаг — **6.14a–d (админка LLM)**.

Ручная проверка 6.12d: создание RFI из формы (причина — Goal, срок, состояние),
карточка показывает бейдж, причину, срок, связи. Тестовый проект —
`5abc7792-0bdf-4ee9-8c96-4320d16978b2`.

Перед 6.12e (после 6.14a–d и 6.13a–d): прочитать `docs/specs/spec_week_4.md`
§9–11, `DOMAIN.md §9.2`, проверить, что контракты 8 эндпоинтов из 6.12c
не менялись.

---

## 3. Что дальше

1. ✅ **6.12d** — UI RFI: RfiPage, RfiCard, RfiForm, API-клиент, хуки, роутинг. Закрыта (проверена вручную 27.10.2026).
2. **6.14a–d** — админка LLM (для демо).
3. **6.13a–d** — парсинг + связывание + валидация + ревизии.
4. **6.12e** — агент RFI (первый автономный агент, `DOMAIN.md §9.2`).
5. **6.12f** — `gip-mcp-gateway` (Agent Gateway + MCP-Tools).
6. Веха 4 закрывается после 6.12e.

После вехи 4 — «Очередь после вехи 3» (дашборд, скелет, отчёты, экспорт, поиск).

---

## 4. Что уже в контексте (не надо пересказывать)

- `docs/README.md` — карта документации. **Читать первым.**
- `docs/context/DOMAIN.md` v1.2 — онтология ядра. **Главный документ.**
- `docs/Дорожная_карта_7.0.md` — стратегия.
- `docs/specs/spec_week_4.md` — спека вехи 4 (RFI).
- `docs/context/CONTEXT.md` v2.17 — резюме продукта.
- `docs/context/TASKS.md` v2.10 — статус + журнал.
- `docs/context/ARCHITECTURE.md` — структура.
- `docs/context/DATABASE.md` — схема БД.
- `docs/context/API.md` v1.1 — эндпоинты.
- `docs/context/RULES.md` — правила кода.
- `docs/context/MASTER_PIPELINE.md` — сквозной пайплайн.
- `AGENTS.md` v1.4 — правила для ИИ-агентов (единственный источник).
- `GIGACODE.md` — заглушка, ссылается на `AGENTS.md`.

---

## 5. Открытые вопросы / блокеры

- [ ] **`decision_id` в домене Task** — отклонение от спеки §2.1 (6.11a). В домене есть поле, в спеке связь только через FK. Решение: узаконить или откатить — в вехе 4 или позже.
- [ ] **API.md baseline** — несвежий (до 6.11d не включал Actions, Results, ProjectStandards, Revisions). Полная сверка с фактическими роутерами — отдельная задача.
- [ ] **Набор Tools в gip-mcp-gateway:** минимальный список для агента RFI (создать RFI, прочитать Decision, прочитать Premise) — утвердить до 6.12f.
- [x] **Agent Gateway + gip-mcp-gateway:** решено — единый сервис (FastAPI, один контейнер, два модуля), не модуль backend. Реализация — 6.12f.

**Блокеров нет.**

---

## 6. Ключи / пути / команды

### 6.1. Аудитор — Kilo Ask (DeepSeek V4.1 Flash)

**Роль:** независимый аудитор кода/плана. Не меняет код. Только отчёт.
**Модель:** DeepSeek V4.1 Flash (`provod/deepseek-v4.1-flash-1017`), Kilo Ask mode (edit: deny).
**Промпты:** `docs/tools/AUDIT_PROMPTS.md`.

**Три точки встраивания:**
1. **Аудит плана** — перед каждым промптом на реализацию. Дёшево.
2. **Аудит кода** — после реализации, до коммита. Средне.
3. **Архитектурный аудит** — раз в веху. Дорого.

**Процесс:**
1. Координатор (DeepSeek) пишет промпт для аудитора.
2. Человек запускает его в Kilo Ask (DeepSeek V4.1 Flash).
3. Аудитор возвращает отчёт (список проблем).
4. Человек присылает отчёт координатору.
5. Координатор сверяет, даёт финальный промпт Kilo (code): «исправь / коммить».

**Правило:** Kilo (code) не коммитит без аудита (точка 2) — для сессий 6.12a–e. Для мелких правок (docs, косметика) аудит не нужен.

- **Проект:** `C:\Users\abelo\GIP-Assistant\gip-assistant`
- **Инструменты:** Kilo (code) + Kilo Ask (DeepSeek V4.1 Flash). Все команды Git/Alembic/pytest — через **внешний терминал** (CMD).
- **Backend (запуск):** `uvicorn backend.src.main:app --reload` (из корня).
- **Backend (venv):** `cd backend && ..\.venv\Scripts\activate`
- **Frontend:** `cd frontend && npm run dev`
- **Тесты:** `pytest backend/tests/ -v` (из корня).
- **Alembic:** `cd backend && ..\.venv\Scripts\activate && alembic current` / `alembic upgrade head`.
- **Ruff:** `.venv\Scripts\activate && ruff check backend/`
- **Docker:** `docker compose -f docker/docker-compose.yml up -d` (gip_db на 5555).
- **БД-инспекция:** `docker exec -it gip_db psql -U gip -d gip_assistant -c "..."` (юзер gip, БД gip_assistant).
- **GitHub:** https://github.com/ABEL678/gip-assistant

---

## 7. Как продолжить в новом чате

**Первое сообщение:**

    Привет. Продолжаем «ГИП-Ассистент». Прочитай:
    1. docs/context/HANDOFF.md
    2. docs/README.md (карта документации)
    3. docs/context/DOMAIN.md (v1.2)
    4. docs/specs/spec_week_4.md
    5. docs/context/CONTEXT.md
    6. docs/context/TASKS.md
    7. AGENTS.md

    Веха 3 закрыта. Веха 4: 6.12a/b/c закрыты, 6.12d закрыта (проверена вручную), 450 passed, миграция c0a9ff2f6038.
    Следующий шаг — 6.14a–d (админка LLM).

    Твоя роль: проверить план 6.14a–d, дать промпт на реализацию.

---

**Конец HANDOFF.md.**
