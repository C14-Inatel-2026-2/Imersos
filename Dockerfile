
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Copia os módulos necessários da aplicação
COPY models/ ./models/
COPY repository/ ./repository/
COPY services/ ./services/
COPY terminal/ ./terminal/

# Prepara o diretório de persistência
RUN mkdir -p /app/dados && \
    useradd --create-home imersos && \
    chown -R imersos:imersos /app/dados

# Executa sem privilégios de administrador
USER imersos

CMD ["python", "-m", "terminal.app"]
