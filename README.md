# gRPCTestTask

## Описание

`gRPCTestTask` — это система для приема пользовательских оценок на определенные события. Система состоит из двух независимых микросервисов:

- **line-provider**: сервис, предоставляющий информацию о событиях.
- **score-maker**: сервис, который принимает оценки от пользователей для этих событий.

Оба сервиса работают независимо, с индивидуальными базами данных. Для обеспечения консистентности данных между ними используется **SAGA паттерн** и **Transactional Outbox паттерн**.

Менеджмент зависимостей для каждого из сервисов осуществляется с помощью **Poetry**.

## Технологии

- **FastAPI**: фреймворк для разработки API.
- **gRPC**: протокол для эффективного взаимодействия между сервисами.
- **Redis**: используется для кэширования и очередей сообщений.
- **PostgreSQL**: реляционная база данных для хранения данных о событиях и оценках.
- **SQLAlchemy**: ORM для взаимодействия с базой данных.
- **Poetry**: инструмент для управления зависимостями и упаковки в Python.

## Установка

Чтобы развернуть проект на своем компьютере, выполните следующие шаги:

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/vladislav-ppv/gRPC-test-task
   ```
2. Перейдите в директорию проекта:
    ```bash
    cd gRPC-test-task
    ```

4. В модулях score_maker, line_provider и arq_worker создайте текстовые файлы с именем .env.

5. Заполните эти файлы, ориентируясь на .env_example, который вы найдете в каждом из модулей.

6. Убедитесь, что у вас установлен Docker Compose. Если он не установлен, следуйте официальной инструкции.

7. Соберите и запустите все контейнеры:

    ```bash
    docker compose up --build -d
    ```

7.Чтобы просматривать логи, используйте команду:
    ```bash
    docker compose logs -f
    ```
    
8. В новой вкладке терминала или API клиента (например, Postman) создайте GET запрос к следующему адресу:

    ```bash
    http://localhost:8002/events
    ```
Если вы получите ответ с кодом 200 OK, значит все работает корректно, вы великолепны.

9. Для просмотра автоматически сгенерированной документации API, откройте в браузере:

    ```bash
    http://localhost:8002/docs
    ```

### Особенности
Микросервисная архитектура: Каждый сервис имеет свою собственную базу данных.
Транзакционная консистентность: Используется паттерн SAGA с Transactional Outbox для синхронизации данных между сервисами.
Автоматическая документация: API автоматически документируется с помощью FastAPI и доступна по адресу http://localhost:8002/docs.
### Пример запросов
GET /events: Получение списка доступных событий.

POST /events/{event_id}/score: Отправка оценки для события.
