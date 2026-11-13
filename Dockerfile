FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir poetry==2.5.1

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main --no-interaction

COPY models/ ./models/
COPY repository/ ./repository/
COPY services/ ./services/
COPY terminal/ ./terminal/
COPY app.py ./
COPY templates/ ./templates/
COPY static/ ./static/

RUN mkdir -p /app/dados && \
    useradd --create-home imersos && \
    chown -R imersos:imersos /app/dados

USER imersos

EXPOSE 10000

CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-10000} app:app"]