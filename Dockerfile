FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN mkdir /task_conrol

WORKDIR /task_conrol

RUN pip install --upgrade pip
RUN pip install poetry
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

RUN apt-get update && apt-get install -y docker-compose

CMD ["sh", "-c", "docker-compose.yaml up && ./docker_script/app.sh"]


