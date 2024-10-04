FROM python:3.10-slim

WORKDIR /score_maker

COPY pyproject.toml /score_maker/

RUN pip install poetry

RUN poetry install --no-dev

COPY . /score_maker/

CMD ["poetry", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
