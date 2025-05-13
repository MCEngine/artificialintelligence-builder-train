# Use the official Python 3.11 image as base
FROM mcr.microsoft.com/devcontainers/python:3.11

# Install PyTorch (CPU version by default, change if you want CUDA)
RUN pip install --upgrade pip && \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Optional: Install requirements.txt if it exists
COPY requirements.txt /workspace/requirements.txt
RUN pip install -r /workspace/requirements.txt || true

# Install useful tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /workspace

# Use non-root user for security
RUN useradd -ms /bin/bash devcontainer
USER devcontainer

# Default shell
CMD ["/bin/bash"]
