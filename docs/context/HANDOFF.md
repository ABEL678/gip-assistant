# HANDOFF.md — эстафета между сессиями

> **Назначение:** файл-эстафета. Пишется по запросу человека — перед
> завершением сессии в чате с ИИ-ассистентом (DeepSeek, ChatGPT, Claude),
> или при приближении к лимиту контекста.
> Читается первым в новом чате. Позволяет продолжить работу без потери контекста.

**Дата:** 22.10.2026
**Сессия:** 6.11e → Веха 3 закрыта
**Статус:** Веха 3 ЗАКРЫТА полностью (6.11a → 6.11b → 6.11c → 6.11d → 6.11e). 392 теста, frontend build зелёный.

---

## 1. Что было в прошлой сессии

**Веха 3 — полностью закрыта (22.10.2026):**

- ✅ **6.11a** — модель Decision + миграция `8aad8fd713f0` (298 тестов).
- ✅ **6.11b** — модели Norm + DecisionLink + DecisionNorm + миграция `c52a3c176d47` (310 тестов).
- ✅ **6.11c** — 5 сервисов + DecisionProposalService (2 правила) (366 тестов).
- ✅ **6.11d** — 21 эндпоинт (decisions 7, norms 5, decision-links 5, decision-norms 4) + 26 тестов роутов (392 теста).
- ✅ **6.11e** — UI: 4 API-клиента, 3 хука, 7 компонентов, 3 страницы (DecisionsPage, NormsPage, DecisionLinkPage), роутинг (85822e4).

**Коммиты вехи 3:** `8fa1bd8` (6.11b), `d35aee4` (6.11c), `ca297f5` (6.11d), `85822e4` (6.11e).

**Итог вехи 3:**
- 392 теста pytest.
- 27 таблиц в БД.
- 60+ эндпоинтов API.
- Весь стек: domain → application → adapters → frontend.

## 2. Что делаем сейчас

**Веха 3 закрыта.** Следующий шаг — развилка.

## 3. Что дальше

**Развилка — не решено (нужен выбор):**

### Путь A: «Очередь после вехи 3» (доработка вехи 1)
1. Дашборд ГИПа (§5.1.12 Дорожная карта 7.0).
2. Скелет из договора (§5.1.13).
3. Отчёты и недельный план (§5.1.14).
4. Экспорт в MS Project XML (§5.1.15).
5. Полнотекстовый поиск (§5.1.16).

### Путь B: Веха 4 (RFI) — **рекомендуется**
1. RFI как особый Task (причина — нехватка ИД, результат — Document).
2. «Живые вводные»: RFI → Document → новые ИД → пополнение Premise.
3. Document ↔ Action связь.
4. Агент RFI.

**Рекомендация: Путь B.** RFI — ядро онтологии (`DOMAIN.md §3.3`), без него вводные статичны. Дашборд/скелет — после RFI, когда данные «живые».

## 4. Что уже в контексте (не надо пересказывать)

- `docs/context/DOMAIN.md` v1.1 — онтология ядра. **Главный документ.**
- `docs/Дорожная_карта_7.0.md` — стратегия.
- `docs/specs/spec_week_3.md` — финальная спека Вехи 3.
- `docs/context/CONTEXT.md` v2.13 — резюме.
- `docs/context/TASKS.md` v2.5 — статус.
- `docs/context/ARCHITECTURE.md` — структура.
- `docs/context/DATABASE.md` — схема БД.
- `docs/context/API.md` v1.1 — эндпоинты.
- `docs/context/RULES.md` — правила.
- `AGENTS.md` — правила для GigaCode.
- `GIGACODE.md` v1.3 — правила (адаптация под GigaIDE + GLM-5.3).

## 5. Открытые вопросы / блокеры

- [ ] **`decision_id` в домене Task** — отклонение от спеки §2.1 (6.11a). В домене Task есть поле decision_id, но в спеке связь только через FK в БД. Зафиксировано в TASKS.md §4. Решение: узаконить или откатить — в вехе 4 или позже.
- [ ] **API.md baseline** — несвежий (до 6.11d не включал Actions, Results, ProjectStandards, Revisions). Полная сверка с фактическими роутерами — отдельная задача.
- [ ] **CONTEXT.md** — §4/§6 всё ещё ссылается на `docs/archive/` — почистить.

**Блокеров нет.**

## 6. Ключи / пути / команды

- **Проект:** `C:\Users\abelo\GIP-Assistant\gip-assistant`
- **Backend:** `cd backend && ..\.venv\Scripts\activate`
- **Backend (запуск):** `uvicorn backend.src.main:app --reload` (из корня)
- **Frontend:** `cd frontend && npm run dev`
- **Тесты:** `pytest backend/tests/ -v` (из корня)
- **Alembic:** `cd backend && ..\.venv\Scripts\activate && alembic current`
- **Ruff:** `.venv\Scripts\activate && ruff check backend/`
- **Docker:** `docker compose -f docker/docker-compose.yml up -d` (из корня, поднимает gip_db на 5555)
- **БД-инспекция:** `docker exec -it gip_db psql -U gip -d gip_assistant -c "..."` (юзер gip, БД gip_assistant)
- **GitHub:** https://github.com/ABEL678/gip-assistant

## 7. Как продолжить в новом чате

**Первое сообщение (для рутинного чата):**

    Привет. Продолжаем «ГИП-Ассистент». Прочитай:
    1. docs/context/HANDOFF.md
    2. docs/context/DOMAIN.md (v1.1)
    3. docs/Дорожная_карта_7.0.md
    4. docs/specs/spec_week_3.md
    5. docs/context/CONTEXT.md
    6. docs/context/TASKS.md
    7. AGENTS.md

    Веха 3 ЗАКРЫТА (6.11a → 6.11e, 392 теста).
    Следующий шаг: развилка — Путь A (очередь после вехи 3) или Путь B (веха 4 RFI).
    Рекомендация: Путь B.

    Твоя роль: помочь выбрать путь, дать GigaCode промпт.

---

**Конец HANDOFF.md.**
