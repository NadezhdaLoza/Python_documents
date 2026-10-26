# Document Flow System (Go Microservices)

Микросервисная система учета документов на Go. Чистая архитектура: Domain -> Service -> Repository -> Transport.

## Стек

- **Язык:** Go
- **БД:** PostgreSQL
- **Маршрутизация:** Gorilla Mux
- **Архитектура:** Clean Architecture, Microservices
- **Frontend:** HTML/Templates, Materialize CSS

## Структура

- `services/base` — утилиты и подключение к БД
- `services/product` — микросервис товаров (backend + frontend)
- `services/home` — прокси-сервер (порт 80)
- `sql/` — скрипты создания таблиц

## Запуск

1. Скачать зависимости:
   ```bash
   go mod tidy
   ```
2. Инициализировать БД:
   Выполнить скрипт `/sql/create_tables.sql в PostgreSQL`.
3. Запустить сервисы (каждый в отдельном терминале)
4. Приложение доступно по адресу: http://localhost
