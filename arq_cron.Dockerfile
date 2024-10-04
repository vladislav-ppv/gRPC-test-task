FROM python:3.10.15-slim

# Set the working directory inside the container
WORKDIR /app
# Copy only the necessary files and directories to the container
COPY ./arq_cron /app

# Install Poetry and project dependencies


COPY ./arq_cron/pyproject.toml .
RUN pip install poetry && poetry install --no-root

# Set the command to run the arq worker
CMD ["poetry", "run", "python", "arq_app.py", "-l", "info"]