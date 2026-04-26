# config

Модуль отвечает за настройки приложения.

Все переменные окружения читаются через `pydantic-settings` в
`src/config/settings.py`. Остальные части приложения должны получать настройки
через `get_settings()`, а не читать `os.environ` напрямую.

Основные переменные:

- `DATABASE_URL` - полный SQLAlchemy URL для подключения к PostgreSQL.
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`,
  `POSTGRES_PORT` - отдельные параметры подключения, если `DATABASE_URL` не
  задан.
- `AUTO_CREATE_TABLES` - временный dev-флаг для создания таблиц при запуске
  ingestion-worker.
- `INGESTION_SOURCE_TIMEOUT_SECONDS` - таймаут запросов к внешним источникам.
