# AGENTS.md — EventFlow AI / Victory Ops Board

## 1. Суть проекта

Проект называется **EventFlow AI / Victory Ops Board**.

Это не просто Trello/Jira-аналог. Продукт должен восприниматься как **система управления digital-производством агентства**: единая операционная платформа, которая помогает агентству управлять проектами, задачами, командами, SLA, уведомлениями, автоматизациями и аналитикой.

Главная идея: пользователь работает с привычной канбан-доской, но за ней находится event-driven engine, который сам реагирует на события, двигает процессы, уведомляет людей, фиксирует историю и помогает PM видеть проблемы раньше, чем они становятся критичными.

Формулировка для понимания продукта:

> EventFlow AI — это операционный автопилот для digital-агентства, который превращает канбан-доску в живую систему управления процессами.

## 2. Для кого делаем

Основной заказчик/контекст: **Victory Group / digital-агентство**.

Типичные боли агентства:

- много клиентов и проектов одновременно;
- разные индустрии и разные рабочие процессы;
- задачи теряются в Telegram/чатах;
- PM вручную контролируют дедлайны и статусы;
- нет прозрачности по загрузке команды;
- нет автоматических сценариев;
- просрочки замечают слишком поздно;
- клиенту сложно показать прогресс без лишнего доступа внутрь агентства.

## 3. Что важно продавать в продукте

Не продавать это как “таск-менеджер”.

Правильный угол:

- управление digital-производством;
- автоматизация агентских процессов;
- контроль SLA;
- прозрачность загрузки команды;
- event-driven orchestration;
- операционный интеллект агентства;
- снижение ручной нагрузки на PM;
- меньше хаоса в коммуникациях.

## 4. Главная demo-идея

Главный сценарий, который должен работать лучше всего:

1. Менеджер создаёт задачу: `Подготовить рекламу для автосалона`.
2. Система сохраняет задачу.
3. Создаётся доменное событие `TASK_CREATED`.
4. Event попадает в очередь/внутренний event pipeline.
5. Automation Engine обрабатывает событие:
   - ставит тег `Auto`;
   - назначает нужную команду/исполнителя;
   - выставляет высокий приоритет;
   - создаёт уведомление;
   - пишет запись в activity/event log.
6. У всех подключённых пользователей интерфейс обновляется в real-time.
7. При просрочке дедлайна система создаёт `DEADLINE_EXPIRED`, уведомляет PM и помечает задачу как проблемную.

Это важнее, чем сделать 100 CRUD-ручек.

## 5. MVP-приоритеты

В условиях хакатона не надо строить весь enterprise-продукт. Нужно защищать demo-path.

### Must-have

- Авторизация или хотя бы базовая идентификация пользователя.
- Организации, пользователи, роли.
- Проекты.
- Доски.
- Колонки.
- Задачи.
- Drag & drop / перемещение задач между колонками.
- Activity log / events.
- Automation rules в формате IF → THEN.
- Notifications.
- WebSocket/live updates.
- Минимальная AI-фича:
  - summary по проекту;
  - генерация подзадач;
  - или приоритизация задач.

### Should-have

- SLA monitor.
- Tags.
- Comments.
- Analytics snapshots.
- Project summaries.
- Простые шаблоны проектов/досок для разных индустрий.

### Nice-to-have

- Client portal.
- Telegram/email интеграции.
- Workload balancer.
- Time tracking.
- CRM integration.
- Красивый visual automation builder.

## 6. Архитектурный принцип

Проект должен выглядеть не как набор случайных CRUD-файлов, а как **осознанный модульный монолит с event-driven ядром**.

Если в репозитории уже выбран стек — не менять стек без необходимости. Сначала анализируй существующую структуру проекта и подстраивайся под неё.

Если стек ещё не зафиксирован, предпочтительный backend-ориентир:

- Python 3.11+ / 3.12;
- FastAPI;
- Pydantic;
- SQLAlchemy 2.0 async;
- Alembic;
- PostgreSQL;
- Redis;
- WebSocket;
- NATS JetStream или RabbitMQ для очереди событий;
- Docker Compose.

Для frontend, если он есть:

- Next.js;
- TypeScript;
- Tailwind;
- Zustand или другой простой state manager;
- WebSocket/Socket.IO client.

## 7. Слои backend

Сохранять разделение ответственности.

### API / Router layer

Роутеры отвечают только за:

- приём HTTP-запроса;
- валидацию входных данных;
- получение зависимостей;
- вызов сервиса;
- возврат DTO/response schema.

В роутерах не должно быть бизнес-логики, SQL-запросов, прямой работы с ORM, очередью или WebSocket-менеджером.

### Service layer

Сервисы отвечают за бизнес-правила:

- создание задач;
- перемещение задач;
- проверку WIP-лимитов;
- контроль прав;
- создание событий;
- запуск automation flow;
- создание уведомлений;
- orchestration между репозиториями.

Если операция затрагивает несколько сущностей — она должна быть в сервисе.

### Repository layer

Репозитории отвечают за доступ к данным:

- SQLAlchemy-запросы;
- получение объектов;
- фильтрация;
- сохранение;
- обновление;
- удаление.

Репозитории не должны знать бизнес-сценарии продукта.

### Schemas / DTO

Pydantic-схемы использовать для:

- входных запросов;
- выходных ответов;
- event payload;
- action payload;
- AI input/output.

Не возвращать наружу ORM-модели напрямую.

## 8. Доменная модель

Текущая схема проекта содержит примерно такие сущности. При добавлении логики ориентируйся на них и не плодить дублирующие таблицы без необходимости.

### Organizations

`organizations`

- `id`
- `name`
- `logo_url`
- `default_sla_hours`
- `created_at`
- `updated_at`

Организация — корень владения данными. Почти все бизнес-сущности должны быть явно или неявно привязаны к organization.

### Users / Roles

`users`

- `id`
- `email`
- `password_hash`
- `first_name`
- `last_name`
- `avatar_url`
- `created_at`
- `updated_at`

`roles`

- `id`
- `name`

`organization_users`

- `id`
- `organization_id`
- `user_id`
- `role_id`
- `joined_at`

Роли:

- `admin`
- `pm`
- `teamlead`
- `specialist`
- `client_viewer`

### Projects

`projects`

- `id`
- `organization_id`
- `client_name`
- `name`
- `description`
- `status`
- `created_by`
- `created_at`
- `updated_at`

Проект — клиентский кейс/поток работ. Важно поддерживать статусы и связь с создателем.

### Boards / Columns

`boards`

- `id`
- `project_id`
- `name`
- `template_type`
- `created_at`

`columns`

- `id`
- `board_id`
- `name`
- `position`
- `wip_limit`
- `color`
- `created_at`

Колонка — этап процесса. `position` нужен для сортировки. `wip_limit` нужен для демонстрации enterprise-логики.

### Tasks

`tasks`

- `id`
- `project_id`
- `board_id`
- `column_id`
- `parent_task_id`
- `title`
- `description`
- `priority`
- `status`
- `due_date`
- `assignee_id`
- `estimated_hours`
- `actual_hours`
- `sort_index`
- `metadata`
- `created_by`
- `created_at`
- `updated_at`

Задача — главная рабочая единица. Почти все важные действия с задачей должны создавать событие и activity record.

Приоритеты можно держать строками/enum:

- `low`
- `medium`
- `high`
- `urgent`

Статусы можно держать строками/enum:

- `todo`
- `in_progress`
- `review`
- `done`
- `blocked`
- `archived`

### Tags

`tags`

- `id`
- `organization_id`
- `name`
- `color`

`task_tags`

- `id`
- `task_id`
- `tag_id`

Теги нужны для automation rules и AI/queue enrichment.

### Comments / Activity

`comments`

- `id`
- `task_id`
- `author_id`
- `body`
- `created_at`

`task_activities`

- `id`
- `task_id`
- `actor_id`
- `activity_type`
- `payload`
- `created_at`

Activity log должен показывать понятную историю: кто создал задачу, кто переместил, какая автоматизация сработала, кому ушло уведомление.

### Events

`events`

- `id`
- `organization_id`
- `task_id`
- `event_type`
- `actor_id`
- `event_data`
- `source_service`
- `correlation_id`
- `causation_id`
- `processed`
- `created_at`

Event — системный факт, который уже произошёл. Не путать с командой.

Хорошие event types:

- `TASK_CREATED`
- `TASK_UPDATED`
- `TASK_MOVED`
- `TASK_ASSIGNED`
- `TASK_PRIORITY_CHANGED`
- `COMMENT_ADDED`
- `DEADLINE_EXPIRED`
- `SLA_BREACHED`
- `AUTOMATION_EXECUTED`
- `NOTIFICATION_CREATED`
- `PROJECT_SUMMARY_GENERATED`

### Automation

`automation_rules`

- `id`
- `organization_id`
- `board_id`
- `name`
- `trigger_event`
- `conditions`
- `actions`
- `enabled`
- `created_by`
- `created_at`

`automation_executions`

- `id`
- `rule_id`
- `event_id`
- `status`
- `execution_log`
- `started_at`
- `completed_at`

Automation rule — это IF → THEN.

Примеры условий:

```json
{
  "field": "tag",
  "operator": "equals",
  "value": "urgent"
}
```

```json
{
  "field": "client_name",
  "operator": "contains",
  "value": "автосалон"
}
```

Примеры actions:

```json
[
  {
    "type": "set_priority",
    "value": "high"
  },
  {
    "type": "add_tag",
    "value": "Auto"
  },
  {
    "type": "notify_user",
    "role": "pm"
  }
]
```

Для MVP не писать сложный rule engine. Достаточно простого обработчика условий и реестра action handlers.

### SLA

`sla_monitors`

- `id`
- `task_id`
- `column_id`
- `entered_at`
- `time_limit_minutes`
- `breached`
- `breached_at`
- `created_at`

SLA monitor должен уметь ответить: сколько задача находится в колонке и нарушен ли лимит.

### Notifications

`notifications`

- `id`
- `user_id`
- `task_id`
- `type`
- `title`
- `body`
- `channel`
- `status`
- `sent_at`
- `read_at`
- `created_at`

Каналы:

- `in_app`
- `telegram`
- `email`
- `push`

Для MVP достаточно `in_app`. Telegram/email можно замокать или оставить интерфейсом.

### Analytics / AI

`analytics_snapshots`

- `id`
- `project_id`
- `snapshot_date`
- `metrics`
- `created_at`

`project_summaries`

- `id`
- `project_id`
- `summary_text`
- `bottlenecks`
- `generated_by_model`
- `generated_at`

AI-фичи должны быть полезны PM:

- краткое summary проекта;
- блокеры;
- просроченные задачи;
- рекомендации по приоритетам;
- генерация подзадач из фразы менеджера.

## 9. Event-driven flow

Каждая важная операция должна иметь понятный event flow.

Пример создания задачи:

1. `TaskService.create_task(...)`
2. Валидация входных данных.
3. Создание `tasks`.
4. Создание `task_activities`.
5. Создание `events` с `event_type = TASK_CREATED`.
6. Commit транзакции.
7. Публикация события в очередь или запуск внутреннего dispatcher.
8. Automation Engine получает событие.
9. Подходящие rules выполняют actions.
10. Создаются notifications/activity/events.
11. WebSocket отправляет обновление клиентам.

Если очередь ещё не поднята, можно сделать внутренний event dispatcher, но код должен быть написан так, чтобы потом его было легко заменить на RabbitMQ/NATS.

## 10. Очередь и обработка событий

Для MVP допустимы два варианта:

### Вариант A — настоящая очередь

Использовать RabbitMQ или NATS JetStream.

Подходит, если инфраструктура уже поднята и не ломает темп разработки.

### Вариант B — internal dispatcher

Использовать внутренний async dispatcher внутри backend.

Подходит, если времени мало. Главное — сохранить интерфейс:

- `publish_event(event)`
- `handle_event(event)`
- `register_handler(event_type, handler)`

Так потом можно заменить реализацию на реальную очередь.

## 11. WebSocket / realtime

Realtime нужен для демонстрации, поэтому не усложнять.

Минимальная модель:

- комнаты по `board_id` или `project_id`;
- клиент подключается к комнате;
- при изменении задачи backend отправляет событие всем клиентам комнаты;
- payload должен содержать тип события и изменённую сущность.

Пример payload:

```json
{
  "type": "TASK_MOVED",
  "board_id": "uuid",
  "task_id": "uuid",
  "from_column_id": "uuid",
  "to_column_id": "uuid",
  "task": {}
}
```

Если есть несколько backend-инстансов, Redis Pub/Sub может синхронизировать сообщения. Для MVP можно начать с in-memory connection manager.

## 12. Automation Engine

Automation Engine — главная фича. Беречь её от превращения в хаос.

Минимальный интерфейс:

- `AutomationService.process_event(event)`
- `AutomationRuleRepository.get_enabled_rules_for_event(...)`
- `ConditionEvaluator.match(rule.conditions, event_context)`
- `ActionExecutor.execute(rule.actions, event_context)`

Поддерживаемые MVP actions:

- `set_priority`
- `add_tag`
- `assign_user`
- `move_task`
- `create_notification`
- `create_comment`
- `mark_sla_breached`

Поддерживаемые MVP conditions:

- `field equals value`
- `field contains value`
- `field in values`
- `deadline_less_than_hours`
- `task_stale_more_than_hours`

Не делать универсальный язык программирования внутри JSON. Нужно сделать простые, надёжные сценарии для демо.

## 13. AI-фичи

AI не должен ломать основной продукт. AI — enhancement поверх event/task/project данных.

Правила:

- AI-вызовы изолировать в отдельном сервисе: `AIService`, `ProjectSummaryService`, `TaskGeneratorService`.
- Не блокировать критические CRUD-операции ожиданием AI, если можно выполнить AI асинхронно.
- Сохранять результат AI в `project_summaries` или в task metadata.
- Обязательно предусмотреть fallback, если API недоступен.
- Не хранить API-ключи в коде.
- Не отправлять в AI лишние персональные данные.

Минимальные AI use cases:

### AI Summary

На вход:

- проект;
- последние задачи;
- последние events;
- просрочки;
- блокеры.

На выход:

- краткий статус проекта;
- что горит;
- кто перегружен;
- что сделать дальше.

### AI Task Generator

На вход:

> Запустить рекламу стоматологии

На выход:

- несколько задач;
- примерные исполнители/роли;
- дедлайны;
- теги;
- приоритеты.

### AI Prioritization

На вход:

- список задач;
- дедлайны;
- текущие статусы;
- исполнители.

На выход:

- какие задачи критичны;
- почему;
- какие задачи можно отложить.

## 14. API-ориентиры

Не обязательно реализовывать всё, но не придумывать противоречивые ручки.

Примерный набор:

### Auth

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Organizations

- `GET /organizations/{organization_id}`
- `GET /organizations/{organization_id}/users`

### Projects

- `POST /projects`
- `GET /projects`
- `GET /projects/{project_id}`
- `PATCH /projects/{project_id}`

### Boards

- `POST /projects/{project_id}/boards`
- `GET /projects/{project_id}/boards`
- `GET /boards/{board_id}`

### Columns

- `POST /boards/{board_id}/columns`
- `PATCH /columns/{column_id}`
- `POST /boards/{board_id}/columns/reorder`

### Tasks

- `POST /tasks`
- `GET /boards/{board_id}/tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `POST /tasks/{task_id}/move`
- `POST /tasks/{task_id}/assign`
- `POST /tasks/{task_id}/comments`

Для действий, которые имеют бизнес-смысл, лучше отдельные action endpoints, а не только generic PATCH.

### Automation

- `POST /automation/rules`
- `GET /automation/rules`
- `PATCH /automation/rules/{rule_id}`
- `POST /automation/rules/{rule_id}/test`
- `GET /automation/executions`

### Notifications

- `GET /notifications`
- `POST /notifications/{notification_id}/read`

### AI

- `POST /projects/{project_id}/summary/generate`
- `GET /projects/{project_id}/summary`
- `POST /ai/task-generator`
- `POST /ai/prioritize`

### WebSocket

- `WS /ws/boards/{board_id}`
- или `WS /ws/projects/{project_id}`

## 15. Работа с БД и миграциями

- Все изменения схемы проводить через Alembic/migrations.
- Не менять БД руками без фиксации в миграциях.
- Для UUID использовать единый подход по всему проекту.
- Для `created_at` и `updated_at` использовать единый механизм.
- Для JSON-полей явно описывать ожидаемую структуру в Pydantic-схемах.
- Не хранить вычисляемые значения без необходимости, если их можно получить запросом.
- Для важных связей добавлять foreign keys.
- Для частых запросов думать об индексах:
  - `tasks.board_id`;
  - `tasks.column_id`;
  - `tasks.assignee_id`;
  - `tasks.due_date`;
  - `events.organization_id`;
  - `events.task_id`;
  - `notifications.user_id`;
  - `automation_rules.trigger_event`.

## 16. Транзакции и события

Не публиковать событие наружу до успешного commit, иначе обработчики могут увидеть событие о данных, которых нет в БД.

Хороший MVP-подход:

1. В рамках транзакции сохранить task/activity/event.
2. Commit.
3. После commit отправить event в dispatcher/queue.
4. Если публикация не удалась, event всё равно остался в таблице `events`, его можно переобработать.

Более правильный подход на будущее — Transactional Outbox.

## 17. Ошибки и ответы API

Использовать понятные ошибки:

- `400` — некорректные данные или невозможное действие;
- `401` — пользователь не авторизован;
- `403` — нет прав в организации/проекте;
- `404` — сущность не найдена;
- `409` — конфликт бизнес-правил, например WIP-limit exceeded;
- `422` — ошибка валидации схемы.

Не отдавать наружу stack trace.

## 18. Права доступа

Минимальная логика:

- пользователь должен быть участником organization;
- `admin` может всё внутри organization;
- `pm` управляет проектами, задачами, automation rules;
- `teamlead` управляет задачами своей команды;
- `specialist` видит и обновляет свои задачи;
- `client_viewer` видит только клиентский прогресс без внутренней кухни.

Если времени мало, сначала сделать проверку membership в organization, потом расширять роли.

## 19. Что нельзя делать без явной причины

- Не переписывать весь проект ради “чистой архитектуры”.
- Не менять стек без необходимости.
- Не добавлять микросервисы, если MVP можно сделать модульным монолитом.
- Не добавлять сложный rule engine, если хватает простых IF → THEN.
- Не делать универсальный no-code builder, если нужен demo-сценарий.
- Не плодить дублирующие сущности `TaskEvent`, `ActivityEvent`, `SystemEvent`, если уже есть `events` и `task_activities`.
- Не класть бизнес-логику в роутеры.
- Не обращаться к БД напрямую из WebSocket handler, если это можно сделать через сервис.
- Не хранить секреты в репозитории.
- Не ломать уже работающий demo-path ради второстепенной фичи.

## 20. Как принимать технические решения

В спорных ситуациях выбирать вариант, который:

1. быстрее доведёт MVP до работающего демо;
2. не создаст очевидный архитектурный тупик;
3. сохраняет event-driven идею;
4. делает систему понятнее для жюри;
5. не требует переписывать половину проекта.

Если есть выбор между “идеально, но долго” и “достаточно правильно, но быстро”, для хакатона выбирать второе.

## 21. Definition of Done для фичи

Фича считается готовой, если:

- есть рабочий backend flow;
- есть сохранение в БД;
- есть понятная схема данных;
- есть activity/event запись, если действие доменно важно;
- есть корректный response DTO;
- есть обработка ошибок;
- есть минимальная проверка прав;
- фича не ломает demo-path;
- при необходимости отправляется realtime update;
- можно показать это в демо без ручного вмешательства в БД.

## 22. Минимальные тесты

Если есть тестовая инфраструктура, добавлять хотя бы тесты на сервисный слой.

Приоритетные сценарии:

- создание задачи создаёт event;
- перемещение задачи меняет column_id и создаёт `TASK_MOVED`;
- automation rule срабатывает на нужный event;
- automation rule не срабатывает, если condition не совпадает;
- notification создаётся после action;
- WIP-limit блокирует перемещение или возвращает предупреждение;
- пользователь без membership не получает доступ к organization/project.

## 23. README и демо

В README обязательно поддерживать:

- что такое EventFlow AI;
- почему это не просто канбан;
- архитектурную схему;
- event flow;
- схему automation engine;
- список ключевых сущностей;
- как запускать через Docker Compose;
- как открыть API docs;
- demo scenario;
- какие фичи готовы;
- какие фичи замоканы;
- что можно развить после хакатона.

## 24. Главный фокус для Codex

Когда помогаешь с кодом, всегда держи в голове:

> Главная ценность проекта — не CRUD задач, а связка: task action → event → automation → notification/activity → realtime update → AI/analytics.

Если задача пользователя не уточняет приоритет, сначала помогай укреплять эту цепочку.
