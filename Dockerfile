FROM python:3.12-slim

WORKDIR /app

# 1. Bring in uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. Cache your pyproject dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# 3. Copy the codebase
COPY . .

EXPOSE 8000

# 4. Run directly from the backend root using standard Python module paths
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]