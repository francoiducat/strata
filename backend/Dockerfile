FROM python:3.12-slim

# Python runtime hygiene
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps
RUN apt-get update \
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false

WORKDIR /app

# Install dependencies first (cache-friendly)
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --no-root

# Copy application
COPY app ./app
COPY alembic ./alembic
COPY alembic/alembic.ini ./alembic.ini
COPY .env .

# SQLite runtime directory
RUN mkdir -p /app/.data

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
