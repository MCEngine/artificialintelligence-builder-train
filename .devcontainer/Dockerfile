FROM python:3.11-slim

# Install dependencies (git, venv support)
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /workspace

# Install virtual environment
RUN python -m venv /workspace/.venv && \
    /workspace/.venv/bin/pip install --upgrade pip
