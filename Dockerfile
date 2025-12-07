FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPYCACHEPREFIX=/tmp/pycache

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

COPY pyproject.toml .

RUN uv sync


FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /app /app

COPY ./src /app/src

ENV PYTHONPATH=/app

WORKDIR /app/src

ENV PATH="/app/.venv/bin:${PATH}"
