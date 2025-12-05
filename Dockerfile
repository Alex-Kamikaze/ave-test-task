FROM python:3.12.11-alpine3.22

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk add --no-cache shadow && \
    groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /service
COPY . /service

RUN chown -R appuser:appuser /service
RUN mkdir -p /home/appuser && chown appuser:appuser /home/appuser

USER appuser

RUN uv sync 
