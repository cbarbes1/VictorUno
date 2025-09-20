# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---- Build wheel (keeps final image smaller)
FROM base AS builder
COPY pyproject.toml README.md /app/
COPY src /app/src
RUN python -m pip install --upgrade pip build && python -m build

# ---- Runtime image
FROM base AS runtime
# Create non-root user
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} app && useradd -m -u ${UID} -g ${GID} app

# Copy built wheel & install
COPY --from=builder /app/dist/*.whl /tmp/
RUN pip install /tmp/*.whl && rm -rf /tmp/*.whl

USER app
WORKDIR /home/app

# Default: talk to host’s Ollama
ENV OLLAMA_HOST=http://host.docker.internal:11434 \
    OLLAMA_MODEL=llama3.1:8b

EXPOSE 8000

# Use the console_script we declared in pyproject.toml
CMD ["langgraph-agent"]
