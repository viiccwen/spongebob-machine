# Use Python 3.11 slim as base image
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files (including README.md which is referenced in pyproject.toml)
COPY pyproject.toml README.md ./

# Install dependencies using uv
RUN uv sync --no-dev

# Copy application code
COPY . .

# Set Python path to include src
ENV PYTHONPATH=/app/src

# Run the bot
CMD ["uv", "run", "main.py"]
