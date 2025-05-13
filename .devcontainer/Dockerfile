FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /workspace

# Install venv
RUN python -m venv /workspace/.venv

# Activate venv and install requirements
RUN /workspace/.venv/bin/pip install --upgrade pip
