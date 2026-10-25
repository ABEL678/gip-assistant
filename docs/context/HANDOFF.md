# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 25.10.2026
**Сессия:** 6.12c → реорганизация docs
**Статус:** Веха 3 закрыта. Веха 4: 6.12a, 6.12b, 6.12c закрыты. 450 тестов, frontend build зелёный.

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

**Код не в работе.** Следующая кодовая сессия — **6.12d (UI RFI)**.

Перед ней: прочитать `docs/specs/spec_week_4.md` §9 (UI) и `MASTER_PIPELINE.md`,
проверить, что контракты 8 эндпоинтов из 6.12c не менялись.

---

## 3. Что дальше

1. **6.12d** — UI RFI: RfiPage, RfiCard, RfiForm, API-клиент, хуки, роутинг.
2. **6.14a–d** — админка LLM (для демо).
3. **6.13a–d** — парсинг + связывание + валидация + ревизии.
4. **6.12e** — агент RFI (первый автономный агент, `DOMAIN.md §9.2`).
5. **6.12f** — `gip-mcp-gateway` (Agent Gateway + MCP-Tools).
6. Веха 4 закрывается после 6.12e.

После вехи 4 — «Очередь после вехи 3» (дашборд, скелет, отчёты, экспорт, поиск).

---

## 4. Что уже в контексте (не надо пересказывать)

- `docs/README.md` — карта документации. **Читать первым.**
- `docs/context/DOMAIN.md` v1.1 — онтология ядра. **Главный документ.**
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

### 6.1. Аудитор GLM-5.3 (GigaCode Ask)

**Роль:** независимый аудитор кода/плана. Не меняет код. Только отчёт.
**Модель:** GLM-5.3 через Cloud.ru (GigaCode Ask mode, `reasoning_effort: high`).
**Промпты:** `docs/tools/AUDIT_PROMPTS.md`.

**Три точки встраивания:**
1. **Аудит плана** — перед каждым промптом на реализацию. Дёшево.
2. **Аудит кода** — после реализации, до коммита. Средне.
3. **Архитектурный аудит** — раз в веху. Дорого.

**Процесс:**
1. Координатор (DeepSeek) пишет промпт для GLM.
2. Человек копирует в GigaCode Ask (модель GLM-5.3).
3. GLM возвращает отчёт (список проблем).
4. Человек присылает отчёт координатору.
5. Координатор сверяет, даёт финальный промпт GigaCode (Agent): «исправь / коммить».

**Правило:** GigaCode (Agent) не коммитит без аудита GLM (точка 2) — для сессий 6.12a–e. Для мелких правок (docs, косметика) аудит не нужен.

- **Проект:** `C:\Users\abelo\GIP-Assistant\gip-assistant`
- **Инструменты:** GigaIDE + GLM-5.3 (Cloud.ru). Встроенный терминал GigaIDE висит на Windows — известный баг. Все команды Git/Alembic/pytest — через **внешний CMD**.
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
    3. docs/context/DOMAIN.md (v1.1)
    4. docs/specs/spec_week_4.md
    5. docs/context/CONTEXT.md
    6. docs/context/TASKS.md
    7. AGENTS.md

    Веха 3 закрыта. Веха 4: 6.12a/b/c закрыты (450 passed, миграция c0a9ff2f6038).
    Следующий шаг — 6.12d (UI RFI).

    Твоя роль: проверить план 6.12d, дать промпт на реализацию.

---

**Конец HANDOFF.md.**
