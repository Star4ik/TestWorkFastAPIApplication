FastAPI + Celery + PostgreSQL TestTask Application

Это проект на FastAPI, который собирает данные через стороннее API и сохраняет их в PostgreSQL. Для фоновых задач используется Celery с брокером Redis. Приложение использует SQLAlchemy для работы с базой данных и поддерживает миграции через Alembic.

Особенности

FastAPI приложение с REST API

Асинхронное подключение к PostgreSQL через asyncpg

Фоновые задачи через Celery

Логирование и хранение данных в PostgreSQL

Миграции базы через Alembic

Docker Compose для быстрого поднятия всех сервисов (FastAPI, PostgreSQL, Redis, Celery)

Установка

Клонируем репозиторий:

git clone https://github.com/Star4ik/TestWorkFastAPIApplication.git
cd TestWorkFastAPIApplication


Создаем .env файл и заполняем его:

DB_NAME=app_db
DB_USER=postgres
DB_HOST=db
DB_PASSWORD=postgres
DB_PORT=5432
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/app_db

REDIS_URL=redis://redis:6379/0


Собираем и запускаем через Docker Compose:

docker compose up --build

docker compose up -d


Все сервисы (FastAPI, PostgreSQL, Redis, Celery) будут запущены.

Миграции базы данных

Создание новой миграции:

docker compose exec web alembic revision --autogenerate -m "описание миграции"


Применение миграций:

docker compose exec web alembic upgrade head

API

Пример ручек FastAPI:

GET /{ticker} — получить все цены по тикеру

GET /{ticker}/last — получить последнюю цену по тикеру

GET /{ticker}/price_by_time — получить данные по конкретному тикеру

Swagger доступен по адресу: http://localhost:8000/docs

Design Decisions
1. FastAPI

Выбран для создания REST API из-за высокой производительности и поддержки асинхронного программирования.

Простая интеграция с Pydantic для валидации входных данных.

Автоматическая генерация документации Swagger и ReDoc.

2. PostgreSQL

Надежная реляционная база данных с поддержкой транзакций и масштабируемости.

Используется вместе с SQLAlchemy для удобной работы с моделями и Alembic для миграций.

3. Asyncpg для FastAPI

Асинхронный драйвер PostgreSQL позволяет не блокировать event loop при запросах к базе данных.

Подходит для высоконагруженных приложений с большим количеством одновременных запросов.

4. Psycopg2 для Alembic

Alembic использует синхронный драйвер для управления миграциями, что является стандартной практикой.

5. Celery + Redis

Celery выбран для обработки фоновых задач (парсинг данных, периодическое обновление цен).

Redis используется как брокер сообщений из-за высокой скорости и простоты интеграции.

6. Docker Compose

Позволяет быстро развернуть все сервисы (FastAPI, PostgreSQL, Redis, Celery) в единой среде.

Изолирует окружение разработки от локальной машины, упрощает деплой и тестирование.

7. Проектная структура

Следование строгим принципам Clean Architecture считаю в данном проекте нецелесообразно, но некоторые её принципы использовались: разделение моделей, схем, сервисов и API.

Упрощает поддержку и расширение проекта: добавление новых API ручек, фоновых задач или моделей не нарушает существующую логику.

8. Логирование и мониторинг

Логирование SQL-запросов и ошибок Celery помогает быстро диагностировать проблемы.

Возможность масштабирования через отдельные контейнеры и воркеры Celery.
