FROM python:3.12-slim

WORKDIR /app

# Install system audio dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependencies
COPY requirements.txt .

# Install dependencies into system python
RUN uv pip install --system -r requirements.txt

# Copy source code
COPY main.py .

# Command to run the agent in production
CMD ["python", "main.py", "start"]
