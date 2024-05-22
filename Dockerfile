FROM docker.io/python:3.11-slim-bookworm

RUN apt-get update
RUN apt-get -y install gcc python3-dev

RUN pip install poetry

WORKDIR /app

RUN mkdir "data"

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install

COPY app app
COPY scripts scripts
COPY alembic alembic
COPY alembic.ini .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]