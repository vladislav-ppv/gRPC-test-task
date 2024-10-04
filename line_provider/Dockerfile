FROM python:3.10-slim

WORKDIR /app/line_provider

COPY pyproject.toml /app/line_provider/

RUN pip install poetry

RUN poetry install --no-dev


COPY . /app/line_provider/

ENV PYTHONPATH=/app
CMD ["poetry", "run", "python", "grpc_server.py"]