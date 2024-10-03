#FROM python:3.10.15-slim
#
#WORKDIR /app
#
#ADD .. /app
#
#RUN pip install poetry
#RUN poetry install
#
#CMD ["poetry", "run", "celery", "-A", "celery_app", "worker", "-Q", "score_queue", "-l", "info"]

FROM python:3.10.15-slim

# Set the working directory inside the container
WORKDIR /app
# Copy only the necessary files and directories to the container
COPY ./celery_worker /app

# Install Poetry and project dependencies



RUN pip install poetry
RUN poetry install --no-root

# Set the command to run the Celery worker
CMD ["poetry", "run", "celery", "-A", "celery_app", "worker", "-l", "info"]