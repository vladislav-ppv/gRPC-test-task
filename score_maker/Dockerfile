FROM python:3.10-slim

WORKDIR /src

COPY pyproject.toml poetry.lock* /src/

# Установка Poetry
RUN pip install poetry

# Установка зависимостей
RUN poetry install --no-dev

COPY .. /src/

CMD ["poetry", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
