# Use a lightweight Python image
FROM python:3.12-slim AS base

# Set environment variable to prevent bytecode and enable logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory in the container
WORKDIR /workspaces/fin-statement-processor

# Install system dependencies (add other later if needed, like tesseract/poppler)
RUN apt-get update && apt-get install -y \
    build-essential \
    bash \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./

# Development stage - used by devcontainer
FROM base AS development

# Accept build argument to control dev dependency install
ARG INSTALL_DEV=false

# Install Python dependencies
RUN pip install --upgrade pip && \
    if [ "$INSTALL_DEV" = "true" ]; then \
        pip install -r requirements-dev.txt; \
    else \
        pip install -r requirements.txt; \
    fi

# Don't copy files in dev stage - devcontainer will mount them
# This preserves git repository and other development files

# Production stage
FROM development AS production

# Copy the rest of your code for production builds
COPY . .

# Default command - interactive shell (for dev container or override via compose)
CMD ["bash", "-c", "while true; do sleep 60; done"]
