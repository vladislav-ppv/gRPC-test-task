FROM python:3.10.15-slim

WORKDIR /app/arq_worker
# Install Poetry and project dependencies
COPY ./arq_worker/pyproject.toml /app/arq_worker
RUN pip install poetry && poetry install --no-root

# Set the working directory inside the container
# Copy only the necessary files and directories to the container
COPY ./arq_worker /app/arq_worker

# Set the command to run the Celery worker
CMD ["poetry", "run", "arq", "arq_app.WorkerSettings"]