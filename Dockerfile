
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY models/ ./models/
COPY repository/ ./repository/
COPY services/ ./services/
COPY terminal/ ./terminal/
COPY web_server.py ./web_server.py

RUN mkdir -p /app/dados && \
    useradd --create-home imersos && \
    chown -R imersos:imersos /app/dados

USER imersos

EXPOSE 10000

CMD ["python", "web_server.py"]
