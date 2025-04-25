# EN 🇺🇸 gRPCTestTask

## Description

`gRPCTestTask` is a system for receiving user ratings for specific events. The system consists of two independent microservices:

- **line-provider**: a service that provides information about events.
- **score-maker**: a service that receives user ratings for these events.

Both services operate independently, each with its own database. To ensure data consistency between them, the **SAGA pattern** and **Transactional Outbox pattern** are used.

Dependency management for each service is handled using **Poetry**.

## Technologies

- **FastAPI**: a framework for developing APIs.
- **gRPC**: a protocol for efficient communication between services.
- **Redis**: used for caching and message queues.
- **PostgreSQL**: a relational database for storing event and rating data.
- **SQLAlchemy**: ORM for interacting with the database.
- **Poetry**: a tool for dependency management and packaging in Python.

## Installation

To run the project on your local machine, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/vladislav-ppv/gRPC-test-task
   ```
2. Navigate to the project directory:
    ```bash
    cd gRPC-test-task
    ```

4. In the score_maker, line_provider, and arq_worker modules, create text files named .env.

5. Fill in these files using the .env_example provided in each module as a reference.

6. Make sure Docker Compose is installed. If not, follow the official installation guide.

7. Build and run all containers:

    ```bash
    docker compose up --build -d
    ```

7. To view logs, use the command:
    ```bash
    docker compose logs -f
    ```
    
8. In a new terminal tab or API client (e.g., Postman), send a GET request to the following address:

    ```bash
    http://localhost:8002/events
    ```
If you receive a 200 OK response, everything is working correctly — you’re awesome.

9.	To view the automatically generated API documentation, open in your browser:

    ```bash
    http://localhost:8002/docs
    ```

### Features
Microservice architecture: Each service has its own database.
Transactional consistency: The SAGA pattern with Transactional Outbox is used to synchronize data between services.
Automatic documentation: The API is automatically documented using FastAPI and available at http://localhost:8002/docs.
### Request Examples
GET /events: Retrieve a list of available events.

POST /events/{event_id}/score: Submit a rating for an event.

# RU 🇷🇺 gRPCTestTask

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
