FROM python:3.12.11-alpine3.22

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk add --no-cache shadow && \
    groupadd -r appuser && useradd -r -g appuser appuser
RUN apk add curl
WORKDIR /service
COPY . /service

RUN chown -R appuser:appuser /service
RUN mkdir -p /home/appuser && chown appuser:appuser /home/appuser

USER appuser

ENV UV_COMPILE_BYTECODE=1

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl --fail http://localhost:8000/healthcheck || exit 1

RUN uv sync 
