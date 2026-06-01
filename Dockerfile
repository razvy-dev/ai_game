# Use the official Astral uv image
FROM astral-sh/uv:python3.12-alpine AS builder

WORKDIR /app

# Enable bytecode compilation for faster execution
ENV UV_COMPILE_BYTECODE=1

# Copy project configuration files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv sync (compiles and locks everything to /app/.venv)
RUN uv sync --frozen --no-dev --no-install-project

# Final minimal execution stage
FROM python:3.12-alpine

WORKDIR /app

# Install system runtime dependencies for postgres
RUN apk add --no-cache libpq

# Copy the virtual environment and your app code from the builder stage
COPY --from=builder /app/.venv /app/.venv
COPY . .

# Set the path to use the virtual environment's executables automatically
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# Run Uvicorn (installed via your pyproject.toml)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]