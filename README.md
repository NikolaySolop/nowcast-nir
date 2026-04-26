# Nowcast NIR

Минимальный стартовый каркас nowcast-проекта.

На текущем этапе проект ограничен двумя частями:

- `postgres` - база данных для хранения загруженных данных и статусов запусков.
- `ingestion-worker` - сервис сбора данных из внешних источников.

Модели, feature engineering, API и dashboard будут добавляться позже, когда
появится первый устойчивый контур данных.

## Architecture

```text
External sources
    |
    v
ingestion-worker  --->  PostgreSQL
```

## Project Layout

```text
src/
  config/        Pydantic-настройки из переменных окружения.
  storage/       Подключение к базе, схемы и функции сохранения.
  ingestion/     Сбор данных из API, файлов и сайтов.

tests/           Smoke-тесты структуры проекта.
```

## Local Development

Создать локальный файл окружения:

```bash
cp .env.example .env
```

Поднять PostgreSQL:

```bash
docker compose up -d postgres
```

Запустить ingestion-worker как одноразовую задачу:

```bash
docker compose run --rm ingestion-worker
```

Или запустить оба сервиса вместе:

```bash
docker compose up --build
```

По умолчанию PostgreSQL доступен на `localhost:5432`.

## Next Implementation Steps

1. Определить первый источник данных.
2. Описать raw-формат и нормализованный формат наблюдений.
3. Добавить первый ingestion-client в `src/ingestion/sources/`.
4. Сохранять raw payload и статус запуска в PostgreSQL.
5. После этого добавлять слой очистки данных и feature engineering.
